# Specification - Restore Skills

## Problem
The `activate_skill` tool returns an empty list.
User confirmed: "did we totally fuck our skills via implementation of the conductor?" -> "yeah" (confirming the need to fix).

## Solution
1. Identify the source of truth for `activate_skill`.
2. Ensure the `prompts/` directory is correctly mapped or configured.
3. If `activate_skill` relies on a specific `skills.json` or similar, recreate it.

## Success Criteria
- Running `activate_skill` lists:
    - `security-review`
    - `bug-board-action-denied`
    - `feature-update-task-tags`
    - etc.
- Activating a skill returns its content.
