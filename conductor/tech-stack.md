# Tech Stack

## Primary Languages
- **Backend:** Python (>=3.13)
- **Plugin Integration:** JavaScript

## Core Frameworks & Libraries
- **Model Context Protocol (MCP):** Using the official `mcp>=1.0.0` Python SDK to expose tools and resources.

## Dependency Management & Tooling
- **Primary:** `uv` (recommended for fast syncing and execution)
- **Fallback:** `pip` (`requirements.txt`)

## Execution Environment
- The MCP server is executed as a local subprocess by the AI client (e.g., OpenCode CLI, Claude Desktop).
- It interacts with the local file system to sync state with the Super Productivity desktop app via the companion JavaScript plugin.