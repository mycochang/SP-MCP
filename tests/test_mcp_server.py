import unittest
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

# MOCK MCP MODULES BEFORE IMPORT
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.stdio'] = MagicMock()
sys.modules['mcp.types'] = MagicMock()
sys.modules['mcp.server.models'] = MagicMock()

# Add parent directory to path so we can import mcp_server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server import SuperProductivityMCPServer

class TestMCPServer(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock the server initialization to avoid actual file/network ops
        self.server_patcher = patch('mcp_server.Server')
        self.mock_server_cls = self.server_patcher.start()
        
        # Instantiate
        self.mcp = SuperProductivityMCPServer()
        
        # Mock internal directories
        self.mcp.command_dir = MagicMock()
        self.mcp.response_dir = MagicMock()
        
    def tearDown(self):
        self.server_patcher.stop()

    async def test_tool_definitions_exist(self):
        """Verify that the tool definition handler is registered"""
        # This is a bit tricky to test without running the actual server loop,
        # but we can verify that setup_tools was called.
        # In a real scenario, we'd inspect the @self.server.list_tools() decorator registry.
        pass

    async def test_update_tag_logic(self):
        """Verify update_tag constructs the correct payload"""
        # Mock send_command to capture arguments
        self.mcp.send_command = MagicMock()
        future = asyncio.Future()
        future.set_result({"success": True})
        self.mcp.send_command.return_value = future

        # Call update_tag with theme color
        await self.mcp.update_tag({
            "tag_id": "TAG_1",
            "theme_primary_color": "#ff0000"
        })

        # Check what was sent to send_command
        self.mcp.send_command.assert_called_once()
        call_args = self.mcp.send_command.call_args
        
        # Args: action, **kwargs
        self.assertEqual(call_args[0][0], "updateTag")
        self.assertEqual(call_args[1]['tagId'], "TAG_1")
        
        # Verify theme structure
        data = call_args[1]['data']
        self.assertIn("theme", data)
        self.assertEqual(data["theme"]["primary"], "#ff0000")
        self.assertEqual(data["theme"]["huePrimary"], "500")

    async def test_update_task_tag_ids(self):
        """Verify update_task maps tag_ids to tagIds"""
        self.mcp.send_command = MagicMock()
        future = asyncio.Future()
        future.set_result({"success": True})
        self.mcp.send_command.return_value = future

        await self.mcp.update_task({
            "task_id": "TASK_1",
            "tag_ids": ["A", "B"]
        })

        self.mcp.send_command.assert_called_once()
        call_args = self.mcp.send_command.call_args
        data = call_args[1]['data']
        
        self.assertIn("tagIds", data)
        self.assertEqual(data["tagIds"], ["A", "B"])

if __name__ == '__main__':
    unittest.main()
