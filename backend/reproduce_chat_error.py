import sys
import asyncio
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Mock settings
os.environ["OPENAI_API_KEY"] = "sk-proj-..." # We will rely on existing env or mock it if needed
# Actually, we need to import settings to get the real config
sys.path.insert(0, 'src')
from core.config import settings

async def test_agent_error():
    print("Initializing ChatOpenAI...")
    try:
        llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE,
            model=settings.OPENAI_MODEL,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=0
        )
        
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="hi")
        ]
        
        print("Invoking LLM...")
        # Reproduce the exact call pattern from agent.py
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, llm.invoke, messages)
        
        print(f"Response type: {type(response)}")
        print(f"Response content: {response.content}")
        
    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent_error())
