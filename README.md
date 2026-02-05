# SP-MCP

Bridge between the amazing [Super Productivity](https://github.com/johannesjo/super-productivity/) app and MCP (Model Context Protocol) servers.

This MCP server and plugin allow AI agents (via Claude Desktop, OpenCode, etc.) to directly interact with Super Productivity. Create tasks, manage projects, organize tags, and query your workload using natural language.

> **Disclaimer:** This extension has been primarily developed and tested with **OpenCode CLI** and **Gemini CLI**. While it includes standard configuration for Claude Desktop, it has not been verified on that platform.
>
> **Note:** Always backup your Super Productivity data before using this extension.

## Run it yourself

### Prerequisites
- **Super Productivity** (Tested on [v17.0.1](https://github.com/johannesjo/super-productivity/commit/a51b2c5))
- **Python** (Developed on **v3.13.11**)
- **uv** (Recommended) or `pip`

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/SP-MCP.git
cd SP-MCP
```

### 2. Install Dependencies

**Using uv (Recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### 3. Connect to your AI Client

#### Option A: OpenCode CLI (Tested & Recommended)
Add the following to your `~/.config/opencode/opencode.json` inside the `mcp` object:

```json
"super-productivity": {
  "enabled": true,
  "type": "local",
  "command": [
    "uv",
    "run",
    "--directory",
    "/absolute/path/to/SP-MCP",
    "mcp_server.py"
  ]
}
```

#### Option B: Claude Desktop (Untested)
Edit your config file:
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Add this inside the `mcpServers` object:

```json
"super-productivity": {
  "command": "uv",
  "args": [
    "run",
    "--directory",
    "/absolute/path/to/SP-MCP",
    "mcp_server.py"
  ]
}
```
*(Replace `/absolute/path/to/SP-MCP` with the output of `pwd` from Step 1)*

### 4. Install the Plugin
1. Open **Super Productivity**.
2. Go to **Settings** → **Plugins**.
3. Click **Upload Plugin**.
4. Select the `plugin.js` file from the `SP-MCP` directory (or `plugin.zip` if provided).
5. **Restart** Super Productivity.

## Demo

https://github.com/user-attachments/assets/cc118173-023f-48cb-8213-427027e475af

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

## Features

- **Task Management:** Create, update, complete, and query tasks.
- **Organization:** Manage Projects and Tags.
- **Natural Language:** Supports Super Productivity's syntax (e.g., `#tag`, `+project`, time estimates).
- **Dashboard:** Real-time statistics and connection status (via plugin UI).
- **File-Based Sync:** Uses local file watching for low-latency communication.

## Troubleshooting

### Plugin Not Loading
- Check Super Productivity version (14.0.0+ required).
- Verify plugin permissions include `nodeExecution` (if prompted).

### Commands Not Working
- Verify both the Plugin (in Super Productivity) and the MCP Server (in your AI client) are running.
- Check file permissions on the communication directories:
    - Linux: `~/.local/share/super-productivity-mcp/`
    - macOS: `~/Library/Application Support/super-productivity-mcp/`
    - Windows: `%APPDATA%\super-productivity-mcp\`
