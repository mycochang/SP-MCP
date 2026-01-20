# Implementation Plan - Fix Incomplete Project Listing

## Phase 1: Reproduction and Analysis [checkpoint: 3f33e4e]
- [x] Task: Create a reproduction test case in `tests/reproduce_project_list.js` that mimics the issue.
    - [x] Create a script that initializes `PluginAPI` mock (or uses the real one if possible in test harness).
    - [x] Simulate "Active" projects with 0 tasks.
    - [x] Simulate "Active" projects with >0 tasks.
    - [x] Assert that `getAllProjects` returns ALL of them.
- [x] Task: Run the reproduction script to confirm failure (RED state).
- [x] Task: Analyze `plugin.js` `getAllProjects` implementation to identify the filtering logic causing the omission.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Reproduction and Analysis' (Protocol in workflow.md)

## Phase 2: Fix Implementation
- [ ] Task: Modify `plugin.js` to ensure `getAllProjects` retrieves all active projects, regardless of task count.
    - [ ] Remove or adjust any filtering that depends on `tasks.length > 0`.
    - [ ] Ensure `PluginAPI.getAllProjects` maps correctly to the internal SP store.
- [ ] Task: Verify the fix with the reproduction script (GREEN state).
- [ ] Task: Run existing tests to ensure no regressions.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Fix Implementation' (Protocol in workflow.md)

## Phase 3: Final Polish & Cleanup
- [ ] Task: Refactor `plugin.js` if necessary for clarity.
- [ ] Task: Remove reproduction scripts if they are not converted to permanent tests.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Polish & Cleanup' (Protocol in workflow.md)
