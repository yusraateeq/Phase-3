"""
Test the chat endpoint to verify it's working
"""
import asyncio
import sys
from pathlib import Path

# Setup path
backend_dir = Path.cwd()
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

async def test_chat_endpoint():
    """Test the SmartAgent directly"""
    from core.config import settings
    from ai.smart_agent import SmartAgent
    from uuid import uuid4
    
    print("Testing SmartAgent...")
    print(f"  OpenAI API Key configured: {'Yes' if settings.OPENAI_API_KEY else 'No'}")
    print(f"  OpenAI API Base: {settings.OPENAI_API_BASE}")
    print(f"  OpenAI Model: {settings.OPENAI_MODEL}")
    
    # Create a test agent
    try:
        agent = SmartAgent(session=None, user_id=uuid4())
        print("[OK] SmartAgent created successfully")
        
        # Try to run a simple message
        print("\nTesting agent with message: 'Hello'")
        response = await agent.run("Hello, can you help me?", chat_history=[])
        print(f"[OK] Got response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_chat_endpoint())
    sys.exit(0 if result else 1)
