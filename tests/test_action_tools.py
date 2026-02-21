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
        mock_send.return_value = {"success": True, "createdTaskIds": {"temp1": "123", "temp2": "456"}}
        
        operations = [
            {"type": "create", "tempId": "temp1", "data": {"title": "Parent Task"}},
            {"type": "create", "tempId": "temp2", "data": {"title": "Subtask", "parentId": "temp1"}}
        ]
        
        result = await server.atomic_batch({"project_id": "test_proj", "operations": operations})
        
        assert result['success'] is True
        mock_send.assert_called_once_with('batchOperation', projectId='test_proj', operations=operations)

@pytest.mark.asyncio
async def test_update_counter():
    server = SuperProductivityMCPServer()
    with patch.object(server, 'send_command', new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"success": True}
        
        result = await server.update_counter({"counter_id": "focus_score", "value": 10})
        
        assert result['success'] is True
        mock_send.assert_called_once_with('updateCounter', counterId='focus_score', value=10)