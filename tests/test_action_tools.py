import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mcp_server import SuperProductivityMCPServer
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_atomic_batch():
    server = SuperProductivityMCPServer()
    with patch.object(server, 'send_command', new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"success": True, "results": [{"success": True}, {"success": True}]}
        
        operations = [
            {"action": "addTask", "data": {"title": "Task 1"}},
            {"action": "updateTask", "taskId": "123", "data": {"title": "Updated Task"}}
        ]
        
        result = await server.atomic_batch({"operations": operations})
        
        assert result['success'] is True
        assert len(result['results']) == 2
        mock_send.assert_called_once_with('batchOperation', operations=operations)

@pytest.mark.asyncio
async def test_update_counter():
    server = SuperProductivityMCPServer()
    with patch.object(server, 'send_command', new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"success": True}
        
        result = await server.update_counter({"counter_id": "focus_score", "value": 10})
        
        assert result['success'] is True
        mock_send.assert_called_once_with('updateCounter', counterId='focus_score', value=10)