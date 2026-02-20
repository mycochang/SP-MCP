import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mcp_server import SuperProductivityMCPServer
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_observe_context():
    server = SuperProductivityMCPServer()
    with patch.object(server, 'send_command', new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"success": True, "active_task": "test"}
        result = await server.observe_context({})
        assert result['success'] is True
        assert result['active_task'] == 'test'
        mock_send.assert_called_once_with('observeContext')
    
@pytest.mark.asyncio
async def test_get_workload_metrics():
    server = SuperProductivityMCPServer()
    with patch.object(server, 'send_command', new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"success": True, "metrics": {}}
        result = await server.get_workload_metrics({})
        assert result['success'] is True
        assert 'metrics' in result
        mock_send.assert_called_once_with('getWorkloadMetrics')