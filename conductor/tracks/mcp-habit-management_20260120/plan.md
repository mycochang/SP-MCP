# Implementation Plan - Implement MCP Habit Management

## Phase 1: API Integration & Tooling [checkpoint: 9d1804e]
- [x] Task: Create a reproduction/exploration script `tests/explore_habits_api.js` to verify `PluginAPI` methods.
    - [x] Mock `addHabit`, `checkHabit`, `updateHabit`, and `getAllSimpleCounters` in `test_harness.js`.
    - [x] Verify that `plugin.js` can correctly dispatch these commands.
- [x] Task: Implement Habit tools in `mcp_server.py`.
    - [x] Add `add_habit`, `check_habit`, `update_habit`, `list_habits` to `list_tools`.
    - [x] Implement the handler logic to send commands to the plugin.
- [x] Task: Implement Command Handlers in `plugin.js`.
    - [x] Add cases for `addHabit`, `checkHabit`, `updateHabit`, `getAllSimpleCounters`.
    - [x] Ensure they call the corresponding `PluginAPI` methods.
- [x] Task: Conductor - User Manual Verification 'Phase 1: API Integration & Tooling' (Protocol in workflow.md)

## Phase 2: Workflow & Validation
- [x] Task: Update `mcp_server.py` tool descriptions to enforce the "Verify First" workflow.
    - [x] Update `add_habit` description to explicitly state: "ALWAYS use list_habits to check for duplicates before creating a new habit."
- [x] Task: Create a comprehensive test `tests/test_habit_workflow.js`.
    - [x] Simulate the flow: List -> Check Existence -> Add (if missing) or Skip.
    - [x] Verify `check_habit` increments the counter.
- [x] Task: Re-zip `plugin.zip` with the new changes.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Workflow & Validation' (Protocol in workflow.md)

## Phase 3: Cleanup
- [ ] Task: Remove exploration scripts.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Cleanup' (Protocol in workflow.md)
