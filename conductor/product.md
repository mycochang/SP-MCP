# Product Definition - SP-MCP

## Initial Concept
Bridge between the amazing [Super Productivity](https://github.com/johannesjo/super-productivity/) app and MCP (Model Context Protocol) servers for Claude Desktop integration.

## Target Audience
- **Super Productivity Users:** Individuals looking to manage their tasks and projects using natural language through AI clients like Claude.
- **Developers & Power Users:** Users seeking to automate task management workflows and synchronize AI-generated project structures into a local, privacy-focused task manager.

## Core Value Proposition
SP-MCP provides a local, low-latency bridge that brings AI intelligence to personal productivity without compromising the "offline-first" and "privacy-first" nature of Super Productivity.

## Functional Requirements
- **Natural Language Translation:** Sophisticated parsing of natural language time and date references into Super Productivity's internal `@syntax` (e.g., "@fri 3pm").
- **Bidirectional Event Sync:** Real-time (or near-real-time) synchronization where actions in Super Productivity (like completing a task) are reflected back to the MCP client.
- **Task & Project Management:** Full support for creating, reading, and updating tasks, projects, and tags.

## Non-Functional Requirements
- **Performance-First Polling:** The file-based communication must remain highly efficient to ensure zero impact on the Electron application's UI responsiveness.
- **Cross-Platform Parity:** Seamless installation and operation across Windows, macOS, and Linux.
- **Privacy Preservation:** All communication remains on the local file system, adhering to Super Productivity's core privacy values.

## Future Vision
- **Model & Client Agnosticism:** Expanding the bridge to support multiple LLM providers and various MCP-compatible clients.
- **Communication Hardening:** Transitioning from the current file-based polling mechanism to a robust Inter-Process Communication (IPC) layer, such as local WebSockets, for instantaneous synchronization and improved reliability.
