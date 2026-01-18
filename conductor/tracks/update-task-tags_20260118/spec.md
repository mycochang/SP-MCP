# Specification - Add Tag Assignment to update_task

## Overview
This track enables users and agents to modify task tags through the `update_task` tool. This is essential for workflows that categorize tasks into productivity quadrants (Urgent/Now/Soon/Later) or project-specific contexts using Super Productivity's tagging system.

## Functional Requirements

### 1. MCP Server Update (`mcp_server.py`)
- **Schema Update:** Add an optional `tag_ids` property to the `update_task` tool's input schema.
    - Type: `array` of `string`.
    - Description: "List of tag IDs to assign to the task. This will replace any existing tags."
- **Logic Update:** In the `update_task` method, detect the presence of `tag_ids` and map it to `tagIds` (camelCase) in the `updates` dictionary before sending the command.

### 2. Plugin Update (`plugin.js`)
- **Verification:** Ensure the `updateTask` handler correctly processes the `tagIds` field.
- **Validation:** Add explicit logging/debug info when `tagIds` are being updated to ensure transparency in the dashboard logs.

## Acceptance Criteria
- Calling `update_task` with `tag_ids: ["A", "B"]` results in a JSON command file with `{ "tagIds": ["A", "B"] }` in the data object.
- The `plugin.js` successfully calls `PluginAPI.updateTask(id, { tagIds: [...] })`.
- Node.js integration tests in `run_tests.js` verify the end-to-end data flow.

## Out of Scope
- Creating new tags on the fly during task update (use `create_tag` first).
- Partial tag merging (this track implements "Replace" logic).
