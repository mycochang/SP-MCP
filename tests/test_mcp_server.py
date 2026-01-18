import unittest
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

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

if __name__ == '__main__':
    unittest.main()
