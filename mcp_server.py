#!/usr/bin/env python3
# MCP Server for Super Productivity Integration

import asyncio
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions


class SuperProductivityMCPServer:
    def __init__(self):
        self.server = Server("super-productivity")
        self.setup_directories()
        self.setup_logging()
        self.setup_tools()

    def setup_directories(self):
        if os.name == "nt":  # Windows
            data_dir = os.environ.get("APPDATA", os.path.expanduser("~/AppData/Roaming"))
        else:  # Linux/Mac
            data_dir = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

        self.base_dir = Path(data_dir) / "super-productivity-mcp"
        self.command_dir = self.base_dir / "plugin_commands"
        self.response_dir = self.base_dir / "plugin_responses"

        # Create directories
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.command_dir.mkdir(parents=True, exist_ok=True)
        self.response_dir.mkdir(parents=True, exist_ok=True)

        logging.info(f"MCP Server using directory: {self.base_dir}")
        logging.info(f"Command directory: {self.command_dir}")
        logging.info(f"Response directory: {self.response_dir}")

    def setup_logging(self):
        log_file = self.base_dir / "mcp_server.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stderr)],
        )

    def setup_tools(self):
        """Set up MCP tools"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools"""
            return [
                types.Tool(
                    name="create_task",
                    description="Create a new task in Super Productivity. When users provide natural language with time/date references, convert them to Super Productivity syntax in the title field.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title with Super Productivity syntax. Convert natural language time/date references to @syntax using days/weeks/months from TODAY (e.g., 'tomorrow' -> '@1days', 'Friday at 3pm' -> '@fri 3pm', 'next week' -> '@7days', 'push back a week' -> '@14days' if task was already a week out). Use @Xdays, @Yweeks, or @Zmonths where X/Y/Z is the number from today. Add #tags for urgency/priority and +projects as needed.",
                            },
                            "notes": {
                                "type": "string",
                                "description": "Task notes/description",
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Project ID to assign task to",
                            },
                            "parent_id": {
                                "type": "string",
                                "description": "Parent task ID for subtasks",
                            },
                        },
                        "required": ["title"],
                    },
                ),
                types.Tool(
                    name="get_tasks",
                    description="Get all tasks from Super Productivity",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_done": {
                                "type": "boolean",
                                "description": "Include completed tasks",
                                "default": True,
                            }
                        },
                    },
                ),
                types.Tool(
                    name="get_archived_tasks",
                    description="Get all historically archived tasks from Super Productivity to analyze past performance and metrics.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    },
                ),
                types.Tool(
                    name="update_task",
                    description="Update an existing task. When users provide natural language with time/date references, convert them to Super Productivity syntax in the title field.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "Task ID to update",
                            },
                            "title": {
                                "type": "string",
                                "description": "New task title with Super Productivity syntax. Convert natural language time/date references to @syntax using days/weeks/months from TODAY (e.g., 'push back a week' -> '@14days' if task was already a week out, 'move to next Friday' -> '@5days' if next Friday is 5 days from today, 'reschedule for tomorrow' -> '@1days'). Use @Xdays, @Yweeks, or @Zmonths where X/Y/Z is the number from today. Add #tags for urgency/priority and +projects as needed.",
                            },
                            "notes": {
                                "type": "string",
                                "description": "New task notes",
                            },
                            "is_done": {
                                "type": "boolean",
                                "description": "Mark task as done/undone",
                            },
                            "time_estimate": {
                                "type": "integer",
                                "description": "Time estimate in milliseconds",
                            },
                            "time_spent": {
                                "type": "integer",
                                "description": "Time spent in milliseconds",
                            },
                            "tag_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of tag IDs to assign to the task. This will replace any existing tags.",
                            },
                        },
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="complete_and_archive_task",
                    description="Complete a task (mark as done) in Super Productivity - NOTE: True deletion is not supported",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "Task ID to complete",
                            }
                        },
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="get_projects",
                    description="Get all projects from Super Productivity",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="update_project",
                    description="Update an existing project (e.g., change title, color, or archive it)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_id": {"type": "string", "description": "Project ID to update"},
                            "title": {"type": "string", "description": "New project title"},
                            "description": {"type": "string", "description": "New project description"},
                            "color": {"type": "string", "description": "New project color (hex code)"},
                            "is_archived": {"type": "boolean", "description": "Archive the project (acts like deletion)"}
                        },
                        "required": ["project_id"],
                    },
                ),
                types.Tool(
                    name="get_current_context_tasks",
                    description="Get tasks for the currently focused view/context in Super Productivity",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="reorder_tasks",
                    description="Reorder tasks manually within a specific context",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of task IDs in the new desired order"
                            },
                            "context_id": {
                                "type": "string",
                                "description": "ID of the context (e.g. project ID, tag ID, or 'TODAY')"
                            },
                            "context_type": {
                                "type": "string",
                                "description": "Type of context ('PROJECT', 'TAG', 'TODAY')"
                            }
                        },
                        "required": ["task_ids", "context_id", "context_type"],
                    },
                ),
                types.Tool(
                    name="create_project",
                    description="Create a new project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Project title"},
                            "description": {
                                "type": "string",
                                "description": "Project description",
                            },
                            "color": {
                                "type": "string",
                                "description": "Project color (hex code)",
                            },
                        },
                        "required": ["title"],
                    },
                ),
                types.Tool(
                    name="get_tags",
                    description="Get all tags from Super Productivity",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="create_tag",
                    description="Create a new tag",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Tag title"},
                            "color": {
                                "type": "string",
                                "description": "Tag color (hex code)",
                            },
                        },
                        "required": ["title"],
                    },
                ),
                types.Tool(
                    name="update_tag",
                    description="Update an existing tag",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tag_id": {
                                "type": "string",
                                "description": "Tag ID to update",
                            },
                            "title": {"type": "string", "description": "New tag title"},
                            "color": {
                                "type": "string",
                                "description": "New tag color (hex code)",
                            },
                            "icon": {
                                "type": "string",
                                "description": "Material Icon name (e.g. wb_sunny)",
                            },
                            "theme_primary_color": {
                                "type": "string",
                                "description": "Theme primary color (hex code) - use this to fix background tint",
                            },
                        },
                        "required": ["tag_id"],
                    },
                ),
                types.Tool(
                    name="delete_tag",
                    description="Delete a tag",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tag_id": {
                                "type": "string",
                                "description": "Tag ID to delete",
                            }
                        },
                        "required": ["tag_id"],
                    },
                ),
                types.Tool(
                    name="create_board",
                    description="Create a new Kanban board configuration",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Board title"},
                            "cols": {
                                "type": "integer",
                                "description": "Number of columns",
                            },
                            "panels": {
                                "type": "array",
                                "description": "List of panel configurations",
                                "items": {"type": "object"},
                            },
                        },
                        "required": ["title", "panels"],
                    },
                ),
                types.Tool(
                    name="show_notification",
                    description="Show a notification in Super Productivity",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Notification message",
                            },
                            "type": {
                                "type": "string",
                                "enum": ["success", "info", "warning", "error"],
                                "description": "Notification type",
                                "default": "info",
                            },
                        },
                        "required": ["message"],
                    },
                ),
                types.Tool(
                    name="debug_directories",
                    description="Debug the communication directories and show their status",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="observe_context",
                    description="Read-only tool to fetch the user's active context.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="get_workload_metrics",
                    description="Read-only tool to fetch the user's workload metrics.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="atomic_batch",
                    description="Execute multiple write operations safely in a single batch using the native SP PluginAPI.batchUpdateForProject. This allows creating parent and child tasks simultaneously using tempIds.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_id": {
                                "type": "string", 
                                "description": "The Super Productivity Project ID to apply this batch to. REQUIRED."
                            },
                            "operations": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "enum": ["create", "update", "delete", "reorder"], "description": "Action to perform"},
                                        "tempId": {"type": "string", "description": "Temporary ID for create operations to allow linking subtasks"},
                                        "taskId": {"type": "string", "description": "Existing task ID for update, delete, or reorder"},
                                        "data": {"type": "object", "description": "Data for create operations (title, notes, parentId, timeEstimate)"},
                                        "updates": {"type": "object", "description": "Data for update operations (title, notes, isDone, timeEstimate)"},
                                        "taskIds": {"type": "array", "items": {"type": "string"}, "description": "Array of task IDs for reorder operations"}
                                    },
                                    "required": ["type"]
                                }
                            }
                        },
                        "required": ["project_id", "operations"]
                    },
                ),
                types.Tool(
                    name="get_counters",
                    description="Read-only tool to fetch all simple counters from Super Productivity.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="get_productivity_audit",
                    description="Calculate a psychological and productivity audit based on recent tasks to determine burnout risk, focus fragmentation, and task friction. Runs natively via the plugin.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "days": {
                                "type": "integer",
                                "description": "Number of days to analyze (default: 7)"
                            }
                        }
                    },
                ),
                types.Tool(
                    name="open_dialog",
                    description="Show an interactive native dialog modal in the Super Productivity UI.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "htmlContent": {"type": "string", "description": "HTML content for the modal body"}
                        },
                        "required": ["htmlContent"]
                    },
                ),
                types.Tool(
                    name="update_counter",
                    description="Update a native simple counter with strict validation.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "counter_id": {"type": "string", "description": "ID of the native counter to update (e.g., 'daily-pushups')"},
                            "value": {"type": "integer", "description": "New value for the counter"}
                        },
                        "required": ["counter_id", "value"]
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Handle tool calls"""
            try:
                if name == "create_task":
                    result = await self.create_task(arguments)
                elif name == "get_tasks":
                    result = await self.get_tasks(arguments)
                elif name == "get_archived_tasks":
                    result = await self.get_archived_tasks(arguments)
                elif name == "update_task":
                    result = await self.update_task(arguments)
                elif name == "complete_and_archive_task":
                    result = await self.complete_and_archive_task(arguments)
                elif name == "get_projects":
                    result = await self.get_projects(arguments)
                elif name == "create_project":
                    result = await self.create_project(arguments)
                elif name == "update_project":
                    result = await self.update_project(arguments)
                elif name == "get_current_context_tasks":
                    result = await self.get_current_context_tasks(arguments)
                elif name == "reorder_tasks":
                    result = await self.reorder_tasks(arguments)
                elif name == "get_tags":
                    result = await self.get_tags(arguments)
                elif name == "create_tag":
                    result = await self.create_tag(arguments)
                elif name == "update_tag":
                    result = await self.update_tag(arguments)
                elif name == "delete_tag":
                    result = await self.delete_tag(arguments)
                elif name == "create_board":
                    result = await self.create_board(arguments)
                elif name == "show_notification":
                    result = await self.show_notification(arguments)
                elif name == "debug_directories":
                    result = await self.debug_directories(arguments)
                elif name == "observe_context":
                    result = await self.observe_context(arguments)
                elif name == "get_workload_metrics":
                    result = await self.get_workload_metrics(arguments)
                elif name == "get_counters":
                    result = await self.get_counters(arguments)
                elif name == "atomic_batch":
                    result = await self.atomic_batch(arguments)
                elif name == "get_productivity_audit":
                    result = await self.get_productivity_audit(arguments)
                elif name == "open_dialog":
                    result = await self.open_dialog(arguments)
                elif name == "update_counter":
                    result = await self.update_counter(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [types.TextContent(type="text", text=str(result))]

            except Exception as e:
                logging.error(f"Error in tool {name}: {str(e)}")
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async def send_command(self, action: str, **kwargs) -> Dict[str, Any]:
        """Send a command to Super Productivity plugin"""
        command = {
            "action": action,
            "id": f"{action}_{asyncio.get_event_loop().time()}",
            "timestamp": asyncio.get_event_loop().time(),
            **kwargs,
        }

        # Write command file
        command_file = self.command_dir / f"{command['id']}.json"
        with open(command_file, "w") as f:
            json.dump(command, f, indent=2)

        logging.info(f"Sent command: {action} -> {command_file}")

        # Wait for response (with timeout)
        response_file = self.response_dir / f"{command['id']}_response.json"

        for _ in range(120):  # Wait up to 120 seconds
            if response_file.exists():
                try:
                    with open(response_file, "r") as f:
                        response = json.load(f)

                    # Clean up response file
                    response_file.unlink()

                    logging.info(
                        f"Received response for {action}: {response.get('success', 'unknown')}"
                    )
                    return response

                except Exception as e:
                    logging.error(f"Error reading response file: {e}")
                    break

            await asyncio.sleep(1)

        # Timeout
        logging.warning(f"Timeout waiting for response to {action}")
        return {"success": False, "error": "Timeout waiting for response"}

    def parse_task_syntax(self, title: str) -> tuple:
        """Parse Super Productivity task syntax from title"""
        title_clean = title

        # Extract tags from title (format: #tagname)
        tag_matches = re.findall(r"#(\w+)", title_clean)
        title_clean = re.sub(r"\s*#\w+", "", title_clean).strip()

        # Extract projects from title (format: +projectname)
        project_matches = re.findall(r"\+(\w+)", title_clean)
        title_clean = re.sub(r"\s*\+\w+", "", title_clean).strip()

        # Extract scheduling syntax (format: @fri 4pm, @tomorrow, @2024-01-15, etc.)
        schedule_matches = re.findall(r"@(\w+(?:\s+\d+[ap]m)?)", title_clean, re.IGNORECASE)
        title_clean = re.sub(
            r"\s*@\w+(?:\s+\d+[ap]m)?", "", title_clean, flags=re.IGNORECASE
        ).strip()

        # Extract time estimate/spent syntax (format: 10m/3h, 2h, 30m, etc.)
        time_matches = re.findall(r"(\d+[mh](?:/\d+[mh])?)", title_clean)
        title_clean = re.sub(r"\s*\d+[mh](?:/\d+[mh])?", "", title_clean).strip()

        return title_clean, tag_matches, project_matches, schedule_matches, time_matches

    async def create_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        title = args.get("title", "")

        # Create the task data - Claude should have already converted natural language to SP syntax
        task_data = {
            "title": title,  # Use title as provided by Claude (should already have @syntax)
            "notes": args.get("notes", ""),
            "timeEstimate": args.get("time_estimate", 0),
            "projectId": args.get("project_id"),
            "parentId": args.get("parent_id"),
            "tagIds": [],
        }

        return await self.send_command("addTask", data=task_data)

    async def get_tasks(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get all tasks"""
        return await self.send_command("getTasks")

    async def get_archived_tasks(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get all archived tasks"""
        return await self.send_command("getArchivedTasks")

    async def update_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update a task"""
        task_id = args.get("task_id")
        if not task_id:
            return {"success": False, "error": "task_id is required"}

        updates = {}

        # Handle title - Claude should have already converted natural language to SP syntax
        if "title" in args:
            updates["title"] = args["title"]

        if "notes" in args:
            updates["notes"] = args["notes"]
        if "is_done" in args:
            updates["isDone"] = args["is_done"]
            if args["is_done"]:
                updates["doneOn"] = asyncio.get_event_loop().time() * 1000
            else:
                updates["doneOn"] = None
        if "time_estimate" in args:
            updates["timeEstimate"] = args["time_estimate"]
        if "time_spent" in args:
            updates["timeSpent"] = args["time_spent"]
        if "tag_ids" in args:
            updates["tagIds"] = args["tag_ids"]

        return await self.send_command("updateTask", taskId=task_id, data=updates)

    async def complete_and_archive_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Complete a task (mark as done) - true deletion is not supported"""
        task_id = args.get("task_id")
        if not task_id:
            return {"success": False, "error": "task_id is required"}

        # Mark task as done instead of deleting
        return await self.send_command("setTaskDone", taskId=task_id)

    async def get_projects(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get all projects"""
        return await self.send_command("getAllProjects")

    async def create_project(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project"""
        project_data = {
            "title": args.get("title", ""),
            "description": args.get("description", ""),
            "color": args.get("color", "#2196F3"),
        }

        return await self.send_command("addProject", data=project_data)


    async def update_project(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing project"""
        updates = {}
        if "title" in args:
            updates["title"] = args["title"]
        if "description" in args:
            updates["description"] = args["description"]
        if "color" in args:
            updates["theme"] = {"primary": args["color"]}
        if "is_archived" in args:
            updates["isArchived"] = args["is_archived"]
            
        return await self.send_command("updateProject", data=updates, projectId=args["project_id"])

    async def get_current_context_tasks(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get tasks for current context"""
        return await self.send_command("getCurrentContextTasks")

    async def reorder_tasks(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Reorder tasks"""
        return await self.send_command("reorderTasks", 
                                     taskIds=args["task_ids"], 
                                     contextId=args["context_id"], 
                                     contextType=args["context_type"])

    async def get_tags(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get all tags"""
        return await self.send_command("getAllTags")

    async def create_tag(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new tag"""
        tag_data = {
            "title": args.get("title", ""),
            "color": args.get("color", "#FF9800"),
        }

        return await self.send_command("addTag", data=tag_data)

    async def update_tag(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update a tag"""
        tag_id = args.get("tag_id")
        if not tag_id:
            return {"success": False, "error": "tag_id is required"}

        updates = {}
        if "title" in args:
            updates["title"] = args["title"]
        if "color" in args:
            updates["color"] = args["color"]
        if "icon" in args:
            updates["icon"] = args["icon"]

        # Handle theme updates specially
        if "theme_primary_color" in args:
            updates["theme"] = {
                "primary": args["theme_primary_color"],
                "huePrimary": "500",
                "accent": "#ff4081",
                "hueAccent": "500",
                "warn": "#e11826",
                "hueWarn": "500",
                "isAutoContrast": True,
                "isDisableBackgroundTint": False,
            }

        return await self.send_command("updateTag", tagId=tag_id, data=updates)

    async def delete_tag(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a tag"""
        tag_id = args.get("tag_id")
        return await self.send_command("deleteTag", tagId=tag_id)

    async def create_board(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new board"""
        board_data = {
            "title": args.get("title", ""),
            "cols": args.get("cols", 2),
            "panels": args.get("panels", []),
        }
        return await self.send_command("createBoard", data=board_data)

    async def show_notification(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Show a notification"""
        message = args.get("message", "")
        # Trigger an OS notification
        await self.send_command("notify", title="Super Productivity AI", message=message)
        # Also trigger the visual snackbar
        return await self.send_command("showSnack", message=message, type="INFO")

    async def debug_directories(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "base_directory": str(self.base_dir),
            "command_directory": str(self.command_dir),
            "response_directory": str(self.response_dir),
            "directories_exist": {
                "base": self.base_dir.exists(),
                "commands": self.command_dir.exists(),
                "responses": self.response_dir.exists(),
            },
        }

    async def observe_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Read-only tool to fetch the user's currently active tasks and view context."""
        return await self.send_command("getCurrentContextTasks")

    async def get_workload_metrics(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Read-only tool to fetch the user's workload metrics."""
        return await self.send_command("getWorkloadMetrics")

    async def get_counters(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Read-only tool to fetch all simple counters."""
        return await self.send_command("getCounters")

    async def atomic_batch(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple write operations safely in a single batch using the native API."""
        operations = args.get("operations", [])
        project_id = args.get("project_id")
        if not project_id:
            return {"success": False, "error": "project_id is required for atomic_batch"}
            
        return await self.send_command("batchOperation", projectId=project_id, operations=operations)

    async def get_productivity_audit(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task data and return a statistical summary."""
        import time
        
        resp = await self.get_tasks({})
        if not resp.get("success"):
            return resp
            
        tasks = resp.get("result", [])
        if not tasks:
            return {"success": True, "report": "No tasks found to analyze."}
            
        now = time.time() * 1000
        completed = [t for t in tasks if isinstance(t, dict) and t.get("isDone")]
        incomplete = [t for t in tasks if isinstance(t, dict) and not t.get("isDone")]
        
        comp_rate = len(completed) / len(tasks) * 100 if tasks else 0
        
        with_notes = [t for t in tasks if isinstance(t, dict) and t.get("notes")]
        without_notes = [t for t in tasks if isinstance(t, dict) and not t.get("notes")]
        
        notes_comp_rate = len([t for t in with_notes if t.get("isDone")]) / len(with_notes) * 100 if with_notes else 0
        no_notes_comp_rate = len([t for t in without_notes if t.get("isDone")]) / len(without_notes) * 100 if without_notes else 0
        
        ages = [(now - t.get("created", now)) / 86400000 for t in incomplete if t.get("created")]
        avg_age = sum(ages) / len(ages) if ages else 0
        
        estimated = [t for t in tasks if isinstance(t, dict) and t.get("timeEstimate", 0) > 0 and t.get("timeSpent", 0) > 0]
        ratios = [t.get("timeSpent") / t.get("timeEstimate") for t in estimated]
        avg_ratio = sum(ratios) / len(ratios) if ratios else 0
        
        report = f"Productivity Audit:\n- Completion Rate: {comp_rate:.1f}%\n- Clarity Premium: {(notes_comp_rate - no_notes_comp_rate):.1f}% (Notes {notes_comp_rate:.1f}% vs No Notes {no_notes_comp_rate:.1f}%)\n- Procrastination Window: {avg_age:.1f} days average age of incomplete tasks\n- Estimation Accuracy: {avg_ratio:.2f} (Time Spent / Estimated)\n- Sample Size: {len(tasks)} total tasks ({len(estimated)} with both estimates and spent time)"
        
        return {"success": True, "report": report}

    async def open_dialog(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Show a native modal dialog"""
        content = args.get("htmlContent")
        if not content:
            return {"success": False, "error": "htmlContent is required"}
            
        dialog_cfg = {
            "htmlContent": content
        }
        return await self.send_command("openDialog", dialogConfig=dialog_cfg)

    async def update_counter(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update a plugin counter with strict validation."""
        counter_id = args.get("counter_id")
        value = args.get("value")
        
        if not isinstance(value, int):
            return {"success": False, "error": "Value must be an integer"}
            
        return await self.send_command("updateCounter", counterId=counter_id, value=value)

    async def run(self):
        """Run the MCP server"""
        logging.info("Starting Super Productivity MCP Server...")

        # Initialize server
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="super-productivity",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


async def main():
    """Main entry point"""
    server = SuperProductivityMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
