# Restore Skills and Prompts

This track focuses on restoring the `activate_skill` functionality and ensuring all prompt-based skills are correctly registered and accessible.

## Goals
- Restore the `activate_skill` tool functionality.
- Verify all existing prompts in `prompts/` are accessible.
- Update documentation to reflect the skill usage.

## Context
The `activate_skill` tool currently reports no available skills. The raw prompt files exist in `prompts/`, but the mechanism to list and load them seems to have been disconnected during the Conductor refactoring.
