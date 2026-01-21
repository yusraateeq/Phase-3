import json
import logging
from typing import Any, List, Optional
from uuid import UUID

from openai import AsyncOpenAI
from sqlmodel import Session

from core.config import settings
from ai.mcp_server import list_tasks, add_task, update_task_status, search_tasks

# Configure logging
logger = logging.getLogger(__name__)

import enum
from datetime import datetime

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, enum.Enum):
            return obj.value
        return super().default(obj)

class SmartAgent:
    def __init__(self, session: Session, user_id: UUID):
        self.session = session
        self.user_id = str(user_id)
        
        # Initialize OpenAI Client
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        self.model = settings.OPENAI_MODEL

        # Define available tools (Manual MCP mapping for in-process usage)
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List my tasks, optionally filtering by status (completed/pending).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of tasks to return"},
                            "status": {"type": "string", "enum": ["all", "completed", "pending"]}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to my todo list.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The task title"},
                            "description": {"type": "string", "description": "Optional details"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"]}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task_status",
                    "description": "Mark a task as completed or pending.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The UUID or the exact Title of the task"},
                            "is_completed": {"type": "boolean", "description": "True for completed, False for pending"}
                        },
                        "required": ["task_id", "is_completed"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_tasks",
                    "description": "Search for tasks by keyword.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search text"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Edit an existing task (title, description, priority, etc).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The UUID or the exact Title of the task"},
                            "title": {"type": "string", "description": "New title"},
                            "description": {"type": "string", "description": "New description"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                            "is_completed": {"type": "boolean"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task from the list.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The UUID or the exact Title of the task to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    async def run(self, user_message: str, chat_history: List[dict] = None) -> str:
        """
        Run the agent loop with model fallback for 429 errors.
        """
        messages = [
            {"role": "system", "content": "You are a helpful Todo AI assistant. You can manage tasks directly (Add, List, Update, Delete). Perform requested actions immediately if the user is clear. If a UUID is not available, you can use the exact Task Title instead. Only ask for confirmation or clarify if the request is truly ambiguous."}
        ]
        
        if chat_history:
            for msg in chat_history:
                messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})

        # First Call
        try:
            response_message = await self._call_llm(messages, tools=self.tools)
            
            # If no tool calls, just return the text
            if not response_message.tool_calls:
                return response_message.content or "I didn't understand that."
            
            # Handle Tool Calls
            messages.append(response_message) # Extend conversation with assistant's intent
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                tool_output = await self._execute_tool(function_name, arguments)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(tool_output, cls=EnhancedJSONEncoder)
                })
            
            # Second Call (Get final answer based on tool outputs)
            final_response = await self._call_llm(messages)
            return final_response.content

        except Exception as e:
            logger.error(f"SmartAgent Error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    async def _call_llm(self, messages: List[dict], tools: Optional[List[dict]] = None):
        """Helper to call LLM with fallback for 429 errors."""
        models = [
            self.model,
            "google/gemini-2.0-flash-exp:free",
            "google/gemini-flash-1.5:free",
            "google/gemini-flash-1.5-8b:free",
            "meta-llama/llama-3.1-8b-instruct:free",
            "meta-llama/llama-3.2-3b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "mistralai/pixtral-12b:free",
            "deepseek/deepseek-r1:free",
            "qwen/qwen-2-7b-instruct:free",
            "gryphe/mythomist-7b:free",
            "openchat/openchat-7b:free",
        ]
        
        last_error = None
        for model_name in models:
            try:
                logger.info(f"Calling LLM with model: {model_name}")
                kwargs = {
                    "model": model_name,
                    "messages": messages,
                }
                if tools:
                    kwargs["tools"] = tools
                    kwargs["tool_choice"] = "auto"
                
                response = await self.client.chat.completions.create(**kwargs)
                return response.choices[0].message
            except Exception as e:
                last_error = e
                # If it's a rate limit (429), not found (404), or other transient provider error, try next model
                error_str = str(e).lower()
                transient_errors = ["429", "rate_limit", "404", "not found", "502", "503", "timeout", "connection"]
                if any(err in error_str for err in transient_errors):
                    logger.warning(f"Model {model_name} failed with error {e}, trying next...")
                    continue
                # For other errors, re-raise
                raise e
        
        raise last_error

    async def _execute_tool(self, name: str, args: dict) -> Any:
        """Execute the mapped internal functions mimicking MCP behavior."""
        logger.info(f"Executing tool {name} with args {args}")
        
        # Inject user_id automatically since we are in the backend context
        if "user_id" not in args:
            args["user_id"] = self.user_id

        try:
            if name == "list_tasks":
                # Filter out 'user_id' if function doesn't need it (our MCP definitions do need it)
                return list_tasks(**args)
            elif name == "add_task":
                return add_task(**args)
            elif name == "update_task_status":
                # update_task_status signature is (task_id, is_completed) - no user_id needed
                if "user_id" in args: del args["user_id"] 
                return update_task_status(**args)
            elif name == "search_tasks":
                return search_tasks(**args)
            elif name == "update_task":
                if "user_id" in args: del args["user_id"]
                from ai.mcp_server import update_task
                return update_task(**args)
            elif name == "delete_task":
                if "user_id" in args: del args["user_id"]
                from ai.mcp_server import delete_task
                return delete_task(**args)
            else:
                return {"error": "Unknown tool"}
        except Exception as e:
            return {"error": str(e)}
