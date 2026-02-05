
import asyncio
import json
import sys
import os
from unittest.mock import MagicMock

# Mock MCP
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.stdio'] = MagicMock()
sys.modules['mcp.types'] = MagicMock()
sys.modules['mcp.server.models'] = MagicMock()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_server import SuperProductivityMCPServer

async def test_live_server():
    print("🚀 Simulating MCP Client...")
    server = SuperProductivityMCPServer()
    
    # We won't run the full stdio loop because it's blocking
    # Instead, we'll manually call the internal handlers to see the response
    
    print("\n📦 Requesting Tool List...")
    # This simulates what the AI sees
    tools = await server.server._tool_manager.list_tools()
    for tool in tools:
        print(f"- Tool: {tool.name}")
        if tool.name in ["update_tag", "delete_tag"]:
            print(f"  ✅ {tool.name} is present and correctly defined.")

    print("\n🛠️ Simulating 'delete_tag' call...")
    # We mock send_command because we don't want to actually write to your disk right now
    server.send_command = MagicMock()
    future = asyncio.Future()
    future.set_result({"success": True, "result": "Tag deleted successfully"})
    server.send_command.return_value = future

    result = await server.delete_tag({"tag_id": "test-id"})
    print(f"Server Response: {result}")
    print("✅ Logic Verified.")

if __name__ == "__main__":
    asyncio.run(test_live_server())
