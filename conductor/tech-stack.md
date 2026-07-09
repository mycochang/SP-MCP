# Tech Stack - SP-MCP

## Core Technologies
- **Python 3.8+**: Used for the MCP Server implementation, leveraging the `mcp` Python SDK for tool definition and execution.
- **JavaScript (Node.js)**: Used for the Super Productivity plugin logic, specifically for file system watching and interacting with the `PluginAPI`.
- **HTML5/CSS3**: Used for the Dashboard UI, adhering to Material Design principles.

## Integration & Communication
- **Model Context Protocol (MCP)**: The standard protocol used to expose Super Productivity tools to AI clients like Claude Desktop.
- **File-Based Message Bus**: Asynchronous communication between the Python server and the Node.js plugin via `plugin_commands/` and `plugin_responses/` directories in the local application data path.

## Development & Runtime Environment
- **Super Productivity Plugin API**: The internal API provided by Super Productivity for task, project, and tag manipulation.
- **Cross-Platform Support**: Built to run on Windows (`%APPDATA%`), Linux (`~/.local/share`), and macOS (`~/Library/Application Support`).
