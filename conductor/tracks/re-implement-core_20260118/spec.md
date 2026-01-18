# Specification - Re-implement Core Features & Board Support

## Overview
This track focuses on re-implementing tag management (update/delete) and board creation functionality following the recent project reset. We will use a TDD approach to ensure stability and verify action strings against the Super Productivity internal API.

## Requirements

### 1. Tag Management
- **Update Tag:** Support updating tag title, color, and icon. Correctly handle the `theme` object mapping to prevent accidental overrides of other theme settings.
- **Delete Tag:** Implement formal support for deleting tags using the `PluginAPI.deleteTag` method (falling back to `dispatchAction` if necessary, with verified action strings).

### 2. Board Management
- **Create Board:** Resolve the "Action Denied" error. Verify the exact NgRx action type string for `[Boards] Add Board`. Ensure the plugin dispatches the payload in the format expected by the host application.

### 3. Verification
- All new features must have 90% test coverage.
- Regression tests for the Path Traversal security fix must be maintained.

## Technical Details
- **Server:** Python `mcp_server.py`
- **Plugin:** JavaScript `plugin.js`
- **IPC:** JSON-based file message bus.
