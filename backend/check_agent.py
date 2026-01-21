import sys
import os
import asyncio
from uuid import uuid4

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from core.config import settings
    print(f"OPENAI_API_KEY set? : {bool(settings.OPENAI_API_KEY)}")
    if settings.OPENAI_API_KEY:
        print(f"OPENAI_API_KEY length: {len(settings.OPENAI_API_KEY)}")

    from ai.mcp_server import list_tasks
    print(f"Imported list_tasks: {list_tasks}")
    print(f"Type of list_tasks: {type(list_tasks)}")

    # Try calling list_tasks directly (mocking DB needed? No, it creates its own session)
    # But it fails if DB connection fails.
    # We just want to check if it's callable.
    
    try:
        # Mocking UUID user_id
        uid = str(uuid4())
        print("Attempting to call list_tasks...")
        # passing random user_id might return empty list, that's fine.
        result = list_tasks(user_id=uid)
        print(f"list_tasks result: {result}")
    except Exception as e:
        print(f"Error calling list_tasks: {e}")

    from ai.smart_agent import SmartAgent
    print("Successfully imported SmartAgent")

except Exception as e:
    print(f"Setup Error: {e}")
    import traceback
    traceback.print_exc()
