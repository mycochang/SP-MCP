import asyncio
import json
from mcp_server import SuperProductivityMCPServer

async def demo():
    print("This is a demonstration script to validate the payload structure for atomic parent/child creation.")
    
    server = SuperProductivityMCPServer()
    
    # We mock the send_command to just print the payload it would send to the plugin
    async def mock_send(action, **kwargs):
        print(f"\\n--- MOCK INTERCEPTED COMMAND: {action} ---")
        print(json.dumps(kwargs, indent=2))
        return {"success": True, "createdTaskIds": {"temp_parent": "actual_id_1", "temp_child": "actual_id_2"}}
        
    server.send_command = mock_send
    
    # The payload an agent would construct to create a nested task structure atomically
    test_args = {
        "project_id": "TEST_PROJECT_ID",
        "operations": [
            {
                "type": "create",
                "tempId": "temp_epic_1",
                "data": {
                    "title": "Epic: Fix the Backend",
                    "timeEstimate": 14400000 # 4 hours
                }
            },
            {
                "type": "create",
                "tempId": "temp_sub_1",
                "data": {
                    "title": "Subtask 1: Write DB migration",
                    "parentId": "temp_epic_1", # Links to the parent tempId!
                    "timeEstimate": 3600000 # 1 hour
                }
            },
            {
                "type": "create",
                "tempId": "temp_sub_2",
                "data": {
                    "title": "Subtask 2: Update models",
                    "parentId": "temp_epic_1",
                    "timeEstimate": 3600000 # 1 hour
                }
            }
        ]
    }
    
    print("\\nSimulating AI Agent calling atomic_batch tool...")
    result = await server.atomic_batch(test_args)
    print(f"\\nResult returned to Agent: {json.dumps(result, indent=2)}")
    
if __name__ == "__main__":
    asyncio.run(demo())
