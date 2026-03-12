# SP-MCP (Advanced OpenCode Fork)

**Welcome to the Advanced Community Fork of SP-MCP.** 

This repository is a heavily expanded, highly diverged fork of the original SP-MCP project. While the original was built purely as a basic Claude Desktop login, this fork has been transformed into a fully-featured, robust, and experimental bridge designed primarily for **OpenCode integration**, automated subagent workflows, native psych/productivity profiling, and complex local UI integrations.

This MCP server acts as a bridge between the amazing [Super Productivity](https://github.com/johannesjo/super-productivity/) app and Model Context Protocol (MCP) clients.

> **Note:** Make sure to backup your Super Productivity data before using in case of data loss. We've provided a `plugin.zip` for convenience, but feel free to build your own from the source files.

## Features (Advanced Fork)

*   **Core Management:** Create and update tasks, manage projects, tags, and context.
*   **OpenCode Optimized:** Native compatibility with OpenCode CLI, skills, and subagents.
*   **Native Modals:** `open_dialog` tool to render native HTML/CSS interactive modals directly inside the Super Productivity UI.
*   **Productivity Psych Audits:** Built-in `get_productivity_audit` to calculate burnout metrics and task friction without bloating LLM context windows.
*   **SimpleCounters API:** Read and update native habit tracking and counters.
*   **OS-Level Notifications:** Trigger native desktop notifications.

## Demo

https://github.com/user-attachments/assets/cc118173-023f-48cb-8213-427027e475af

## Requirements

- Super Productivity 14.0.0 or higher
- Python 3.10+
- OpenCode / Claude Desktop / Any MCP-compatible client
- `uv` (Recommended Python package manager)

## Installation

### Recommended Setup (Using `uv`)

1. **Clone this repo:**
   ```bash
   git clone https://github.com/mycochang/SP-MCP.git
   cd SP-MCP
   ```

2. **Sync Dependencies:**
   ```bash
   uv sync
   ```

3. **Install the plugin in Super Productivity:**
   - Open Super Productivity → Settings → Importer/Exporter → Plugins (or Advanced -> Plugins).
   - Click "Upload Plugin" or paste the contents of `plugin.js`.
   - Alternatively, upload the provided `plugin.zip`.

4. **Configure OpenCode (or Claude Desktop):**
   Add the MCP server to your config file:
   ```json
   "super-productivity": {
     "command": "uv",
     "args": ["run", "/path/to/SP-MCP/mcp_server.py"]
   }
   ```

5. **Restart your client (and Super Productivity).**

### Legacy Automatic Setup (Not Recommended)
The original `setup.sh` and `setup.bat` files are preserved for historical reasons but `uv run mcp_server.py` is the official supported method in this fork.

## Usage

### Creating Tasks
```
"Create a task to review the quarterly budget #finance +work"
```

### Task Management
```
"Show me all my tasks"
"Mark the budget review task as complete"
"Update the task 'Meeting prep' with notes about the agenda"
```

### Project and Tag Management
```
"Create a new project called 'Website Redesign'"
"Show me all projects"
"Get all tags"
```

## Communication Bridge

The plugin uses file-based communication through:
- Windows: `%APPDATA%\super-productivity-mcp\`
- Linux: `~/.local/share/super-productivity-mcp/`
- macOS: `~/Library/Application Support/super-productivity-mcp/`

Commands are exchanged asynchronously through `plugin_commands/` and `plugin_responses/` directories.

## Troubleshooting

### Plugin Not Loading
- Check Super Productivity version (14.0.0+ required)
- Verify plugin permissions include `nodeExecution`
- If you made changes, ensure you bumped the version or re-pasted the new `plugin.js`.

### Commands Not Working / Sync Failures
- Run `uv run debug_bridge.py` to send a diagnostic ping.
- Verify both the plugin and MCP server are looking at the exact same directory paths.
- Check `mcp_server.log` in the local share directory.

---
*MIT License. Copyright (c) 2025 organicmoron, Copyright (c) 2026 Mike Chang.*
