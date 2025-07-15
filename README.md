# SP-MCP

Bridge between Super Productivity and MCP (Model Context Protocol) servers for Claude Desktop integration.

This MCP and plugin allows Claude Desktop to directly interact with Super Productivity through the MCP protocol. You can create tasks, update existing tasks, manage projects and tags, and get information from Super Productivity using natural language.

[[demo1](https://github.com/user-attachments/assets/a1f9e0fc-8ab1-4de7-ae56-738cd42bd789](https://github-production-user-asset-6210df.s3.amazonaws.com/220924574/466643832-a1f9e0fc-8ab1-4de7-ae56-738cd42bd789.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250715%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250715T182028Z&X-Amz-Expires=300&X-Amz-Signature=7dc5afad4053174a21e5b307c556a26a04a087aedf222d6c1d0e8525095ab941&X-Amz-SignedHeaders=host)](https://github-production-user-asset-6210df.s3.amazonaws.com/220924574/466643832-a1f9e0fc-8ab1-4de7-ae56-738cd42bd789.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250715%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250715T182028Z&X-Amz-Expires=300&X-Amz-Signature=7dc5afad4053174a21e5b307c556a26a04a087aedf222d6c1d0e8525095ab941&X-Amz-SignedHeaders=host)


https://github.com/user-attachments/assets/eb2adb22-e3c5-4f9c-a2b7-64079a5d2a55

## Requirements

- Super Productivity 14.0.0 or higher
- Claude Desktop
- Python 3.8 or higher

## Installation

### Automatic Setup

**Windows:**
1. Clone this repo
2. Run `setup.bat`
3. Follow the prompts

**Linux/Mac UNTESTED:**
1. Clone this repo
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

### Commands Not Working
- Verify both plugin and MCP server are running
- Check file permissions on communication directories
- Check `mcp_server.log` in the data directory
