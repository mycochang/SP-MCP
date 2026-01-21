# Security Vulnerability Report: SP-MCP (Super Productivity MCP Bridge)

**Date:** January 18, 2026
**Target:** `plugin.js`, `mcp_server.py`
**Reviewer:** Gemini CLI Security Agent

## Executive Summary

The SP-MCP bridge facilitates communication between an MCP client and Super Productivity via a shared file system. While functional, this architecture introduces significant security risks, particularly regarding file system access and resource management. The most critical vulnerability allows for arbitrary file writes on the host system.

## 1. Vulnerability Findings

### 1.1 Arbitrary File Write (Path Traversal) - CRITICAL
**Location:** `plugin.js` -> `writeCommandResponse` function.
**Description:** The function uses the `command.id` directly from the input JSON to construct the output filename. No validation is performed to ensure the ID does not contain path separators.
**Impact:** An attacker (or malicious local script) can provide an ID like `../../.bashrc` to escape the `plugin_responses` directory. This allows overwriting sensitive system files with arbitrary JSON data, potentially leading to code execution or system corruption.
**Proof of Concept:**
```json
{
  "action": "getTasks",
  "id": "../../malicious_file.txt"
}
```

### 1.2 No Authentication / Implicit Trust - HIGH
**Location:** Architecture-wide (`plugin_commands` directory).
**Description:** The system relies on "local user trust." It assumes that only the legitimate `mcp_server.py` will write to the command directory.
**Impact:** Any malicious software running on the user's machine (even with low privileges) can write a JSON file to this directory to trigger any action the plugin supports (creating tasks, modifying projects, opening dialogs).

### 1.3 Denial of Service (DoS) - MEDIUM
**Location:** `plugin.js` -> `processNewCommands` function.
**Description:** The plugin reads and parses *all* files in the command directory every 2 seconds. There is no limit on the number of files processed in a single cycle.
**Impact:** A flood of files (e.g., 5,000 text files) can cause the Electron main thread to hang while reading/parsing, rendering the Super Productivity application unresponsive (UI Freeze).

### 1.4 Action Injection / Phishing Risk - MEDIUM
**Location:** `plugin.js` -> `openDialog` action.
**Description:** The plugin exposes an API to open arbitrary dialogs within the application.
**Impact:** A malicious actor could trigger a dialog asking for sensitive information (e.g., "Please re-enter your Jira password"), tricking the user into revealing credentials.

### 1.5 Sensitive Data Exposure - LOW
**Location:** `plugin.js` -> `log` function.
**Description:** `debugMode` is enabled by default. Task titles and notes (which may contain sensitive work info) are logged to the console and the internal dashboard.
**Impact:** Other scripts or unauthorized observers with access to the logs could read private data.

## 2. Remediation Recommendations

### 2.1 Fix Path Traversal (Immediate Action Required)
Sanitize the `commandId` using `path.basename()` to strip directory separators.

```javascript
// Recommended Fix for plugin.js
const commandId = path.basename(args[1]); 
```

### 2.2 Limit Command Processing
Implement a batch limit to prevent the event loop from blocking.

```javascript
// Recommended Fix for plugin.js
const commandFiles = files.filter(f => f.endsWith('.json'))
  .slice(0, 10); // Process max 10 files per cycle
```

### 2.3 Harden "Shared File System" Architecture
For a more secure design, consider transitioning from a file-based bus to a **Local WebSocket** connection. This allows:
1.  **Authentication:** Use a pre-shared token generated on app startup.
2.  **Memory-only transport:** Avoids writing sensitive data to disk.

## 3. Conclusion
The current implementation works for a trusted, single-user environment but is fragile against local attacks. Patching the Path Traversal vulnerability is mandatory before production use.
