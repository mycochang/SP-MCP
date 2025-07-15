# SP-MCP

Bridge between Super Productivity and MCP (Model Context Protocol) servers for Claude Desktop integration.

## Overview

This plugin allows Claude Desktop to directly interact with Super Productivity through the MCP protocol. You can create tasks, update existing tasks, manage projects and tags, and get information from Super Productivity using natural language in Claude.

## Requirements

- Super Productivity 14.0.0 or higher
- Claude Desktop
- Python 3.8 or higher

## Installation

### Automatic Setup

**Windows:**
1. Download this folder
2. Run `setup.bat` as Administrator
3. Follow the prompts

**Linux/Mac:**
1. Download this folder
2. Run `chmod +x setup.sh && ./setup.sh`
3. Follow the prompts

The setup scripts will preserve any existing MCP servers in your Claude Desktop configuration.

You'll still have to install the plugin.zip manually in Super Productivity in settings->plugins.

Once that's done, restart claude (and Super Prod for good measure) and you should be able to access your files

### Manual Setup

1. **Install Python dependencies:**
   ```bash
   pip install mcp
   ```

2. **Set up MCP server:**
   Copy `mcp_server.py` to your data directory:
   - Windows: `%APPDATA%\super-productivity-mcp\`
   - Linux: `~/.local/share/super-productivity-mcp/`
   - macOS: `~/Library/Application Support/super-productivity-mcp/`

3. **Configure Claude Desktop:**
   Edit Claude's config file and add to `mcpServers`:
   ```json
   "super-productivity": {
     "command": "python3",
     "args": ["/path/to/mcp_server.py"]
   }
   ```

4. **Install the plugin:**
   - Open Super Productivity → Settings → Plugins
   - Click "Upload Plugin"
   - Select `plugin.js`

5. **Restart Claude Desktop**

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

## Dashboard

Access the SP-MCP dashboard from the menu. The dashboard shows:
- Real-time statistics
- Connection status
- Activity logs
- Settings (polling frequency: default 2 seconds)

## File Structure

```
SP-MCP/
├── plugin.js              # Super Productivity plugin
├── mcp_server.py          # MCP server for Claude Desktop
├── index.html             # Dashboard UI
├── manifest.json          # Plugin manifest
├── setup.bat             # Windows setup script
├── setup.sh              # Linux/Mac setup script
├── merge_config.py       # Config merger
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Communication

The plugin uses file-based communication through:
- Windows: `%APPDATA%\super-productivity-mcp\`
- Linux: `~/.local/share/super-productivity-mcp/`
- macOS: `~/Library/Application Support/super-productivity-mcp/`

Commands are exchanged through `plugin_commands/` and `plugin_responses/` directories.

## Troubleshooting

### Plugin Not Loading
- Check Super Productivity version (14.0.0+ required)
- Verify plugin permissions include `nodeExecution`

### MCP Server Not Connecting
- Ensure Python and `mcp` package are installed
- Check Claude Desktop config file syntax
- Restart Claude Desktop after configuration changes

### Commands Not Working
- Verify both plugin and MCP server are running
- Check file permissions on communication directories
- Check `mcp_server.log` in the data directory

## Tag and Project Syntax

- `#tagname` - Assigns tag "tagname"
- `+projectname` - Assigns to project "projectname"

Example: `"Finish the report #urgent +client-work"`

## Security

- All communication happens locally
- No data sent to external servers
- File-based IPC for security