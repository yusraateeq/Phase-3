
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    print("Attempting to import SmartAgent...")
    from src.ai.smart_agent import SmartAgent
    print("Successfully imported SmartAgent")
except Exception as e:
    print(f"Failed to import SmartAgent: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nAttempting to import mcp_server...")
    from src.ai import mcp_server
    print("Successfully imported mcp_server")
except Exception as e:
    print(f"Failed to import mcp_server: {e}")
    import traceback
    traceback.print_exc()
