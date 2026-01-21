try:
    import mcp
    print(f"Successfully imported mcp. File: {mcp.__file__}")
    from mcp.server.fastmcp import FastMCP
    print("Successfully imported FastMCP")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
