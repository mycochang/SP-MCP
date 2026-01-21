# Security Review Prompt: SP-MCP (Super Productivity MCP Bridge)

## Role & Goal

You are a Senior Security Engineer and Application Security Specialist. Your goal is to perform a comprehensive security review of the SP-MCP codebase (`plugin.js`, `mcp_server.py`, and related infrastructure).

## Context

This project acts as a bridge between an MCP (Model Context Protocol) client (like Claude/OpenCode) and the Super Productivity desktop application. It uses a "Shared File System" architecture:

1.  **Python Server (`mcp_server.py`)**: Receives JSON-RPC commands, writes them to `~/.local/share/super-productivity-mcp/plugin_commands/`.
2.  **Plugin (`plugin.js`)**: Running inside the Electron App, watches that directory, executes commands (Node.js + Internal API), and writes responses back.

## Scope of Review

Please analyze the codebase for the following risks:

### 1. Remote Code Execution (RCE) & Injection

- **Node.js execution:** The plugin uses `PluginAPI.executeNodeScript`. Is the input passed to this function strictly sanitized? Can a malicious command file inject arbitrary JavaScript?
- **Path Traversal:** Can a command file manipulate file paths (e.g., `../../`) to read/write files outside the intended sandbox?
- **Command Injection:** Are any shell commands executed? If so, are arguments escaped?

### 2. Authorization & Access Control

- **Authentication:** Is there _any_ verification of who is writing to the `plugin_commands` directory? (Currently assumes local user trust).
- **Scope Creep:** Does the plugin expose methods (like `downloadFile` or `executeNodeScript`) that are too powerful for a task management assistant?
- **Privilege Escalation:** Can the plugin modify the App's configuration to weaken security (e.g., disabling other checks)?

### 3. Data Privacy

- **Leakage:** Does the logging (`debugMode`) write sensitive task data (tokens, notes) to plain text logs?
- **Validation:** Are inputs (Task Titles, Notes) validated before being inserted into the database?

### 4. Denial of Service (DoS)

- **Resource Exhaustion:** Can a flood of command files crash the plugin or the app?
- **File Descriptors:** Are file handles properly closed?

## Deliverables

1.  **Vulnerability Report:** A list of identified risks ranked by severity (Critical, High, Medium, Low).
2.  **Code Hardening Suggestions:** Specific code snippets to patch vulnerabilities (e.g., "Add `path.normalize()` here", "Sanitize `args[0]`").
3.  **Architecture Review:** Is the "Shared File System" approach secure enough for a single-user desktop environment?

## How to Execute

- Read `plugin.js`.
- Read `mcp_server.py`.
- Read `manifest.json`.
- Simulate attack vectors (e.g., "What if I write a JSON file with `action: 'executeNodeScript'` and payload `rm -rf /`?").
