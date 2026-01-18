# Implementation Plan - Add Tag Assignment to update_task

## Phase 1: Verification & Test Setup
- [x] Task: Verify `updateTask` capability
- [x] Task: Set up TDD for `tag_ids`
    - [x] Add a failing test case to `tests/test_mcp_server.py` that checks for `tag_ids` in the `update_task` tool definition.
    - [x] Add a failing test case to `tests/run_tests.js` that checks if `plugin.js` logs/handles the tag update explicitly.

## Phase 2: Implementation
- [x] Task: Implement `tag_ids` in `mcp_server.py`
- [x] Task: Hardening `plugin.js` (Optional but recommended)
    - [x] Update `updateTask` handler to explicitly log tag changes (for visibility).
    - [x] Verify Node.js tests pass.
- [~] Task: Conductor - User Manual Verification 'Phase 2: Implementation' (Protocol in workflow.md)

## Phase 3: Final Verification
- [x] Task: Manual Integration Test [checkpoint: fa2ae7b]
    - [x] Test via Gemini CLI / OpenCode to ensure tags are actually updated in Super Productivity.
    - [x] Confirm no regression in other update fields (title, notes).