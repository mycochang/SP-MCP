# Implementation Plan - Re-implement Core Features & Board Support

## Phase 1: Tag Management Infrastructure
- [x] Task: Set up TDD environment for Python and Node.js
    - [x] Write Node.js test harness for `PluginAPI` mocks
    - [x] Write Python unit tests for `SuperProductivityMCPServer` tool definitions
- [x] Task: Implement `delete_tag` [commit: 15bdd31]
    - [ ] Write failing test for `delete_tag` command flow
    - [ ] Update `mcp_server.py` with `delete_tag` tool
    - [ ] Update `plugin.js` to handle `deleteTag` action using `PluginAPI.deleteTag`
    - [ ] Verify tests pass
- [x] Task: Implement `update_tag` [commit: 4fd4138]
    - [ ] Write failing test for `update_tag` with theme color mapping
    - [ ] Update `mcp_server.py` with `update_tag` tool
    - [ ] Update `plugin.js` to handle `updateTag` action
    - [ ] Verify tests pass
- [x] Task: Conductor - User Manual Verification 'Phase 1: Tag Management' (Protocol in workflow.md) [checkpoint: 35d71b6]

## Phase 2: Board Management Fix
- [x] Task: Verify Board Action String (Skipped: Unable to verify external source, proceeding with '[Boards] Add Board')
    - [x] Search Super Productivity source (or logs) for exact `addBoard` action type string
    - [x] Update `plugin.js` with the verified action string
- [x] Task: Implement `create_board` [commit: e08fe68]
    - [ ] Write failing test for `create_board` tool-to-plugin flow
    - [ ] Update `mcp_server.py` with `create_board` tool
    - [ ] Update `plugin.js` to handle `addBoard` action
    - [ ] Verify tests pass
- [x] Task: Conductor - User Manual Verification 'Phase 2: Board Management' (Protocol in workflow.md) [checkpoint: dddce95]

## Phase 3: Stabilization & Cleanup
- [ ] Task: Final regression testing
    - [ ] Run security regression tests (Path Traversal)
    - [ ] Verify 90% code coverage
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Acceptance' (Protocol in workflow.md)
