# Agent Knowledge Base & Guide for Super Productivity MCP

This repository implements a Model Context Protocol (MCP) server for Super Productivity.
**Architecture:** Unlike most MCP servers that talk to a REST API, this server uses a **Local File Bridge** to communicate with a `plugin.js` running inside the Super Productivity Electron app.

## 1. Architecture (Observe)

*   **MCP Server (`mcp_server.py`)**:
    *   Writes JSON commands to `~/.local/share/super-productivity-mcp/plugin_commands/`.
    *   Reads JSON responses from `~/.local/share/super-productivity-mcp/plugin_responses/`.
*   **Plugin (`plugin.js`)**:
    *   Runs inside Super Productivity.
    *   Polls the command directory every 2 seconds.
    *   Executes the command against the App's internal API (`PluginAPI`).
    *   Writes the result to the response directory.

## 2. Sync & Diagnostics (Orient)

**The "Mega Syncing Issue":**
Sync failures usually happen because:
1.  **Deployment Drift:** The `plugin.js` running in the app is older than the one in this repo.
2.  **Bridge Collapse:** The file permissions on `~/.local/share/...` are broken, or the directory path is wrong (OS mismatch).

**Diagnostic Stakes:**
*   **Bridge Check:** Run `python debug_bridge.py` to send a "ping" command. If it times out, the plugin is NOT running or NOT looking at the right directory.
*   **Version Check:** The debug script queries the plugin for its version.

## 3. Development (Act)

### Environment Setup
- **Package Manager:** `uv` is used.
- **Install:** `uv sync`.
- **Run Server:** `uv run mcp_server.py`.

### Updating the Plugin
If you modify `plugin.js`:
1.  **Version Bump:** Update the `VERSION` constant.
2.  **Deploy:** You MUST copy the content of `plugin.js` and paste it into Super Productivity's Settings -> Importer/Exporter -> Plugin (or Advanced -> Plugin).
3.  **Verify:** Run `debug_bridge.py` to confirm the new version is active.

## 4. OODA Loop for Debugging
1.  **Observe:** "It works on NOI but not BASIS."
2.  **Orient:** Run `debug_bridge.py` on *both* machines.
3.  **Decide:**
    *   If Bridge fails on one: Re-paste `plugin.js`.
    *   If Bridge works on both but Data differs: Check SP's internal Sync (WebDAV/Dropbox).
4.  **Act:** Fix the specific component.
