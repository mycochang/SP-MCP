# Implementation Plan: Upgrade to Native Atomic Batching API

## Phase 1: Plugin Bridge (Atomic Execution)
- [ ] Task: Replace the sequential loop in `plugin.js` with a native atomic dispatch.
    - [ ] Sub-task: Audit `PluginAPI` for `batchUpdate` or `dispatchAction` capabilities that support `tempId` mapping.
    - [ ] Sub-task: Refactor the `executeBatchOperation` function to construct and fire a single Redux action or batch request.
    - [ ] Sub-task: Build and package the updated `plugin.zip`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Plugin Bridge (Atomic Execution)' (Protocol in workflow.md)

## Phase 2: Data Translation & Payload Support
- [ ] Task: Ensure the payload structure from `mcp_server.py` matches the new batch interface.
    - [ ] Sub-task: Update the input schema for `atomic_batch` in `mcp_server.py` to document `tempId` mapping for the LLM.
    - [ ] Sub-task: Write Tests verifying that the MCP server correctly validates the new batch schema.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Data Translation & Payload Support' (Protocol in workflow.md)

## Phase 3: Validation (Parent/Child Linking)
- [ ] Task: Prove the agent can create a parent and subtask simultaneously.
    - [ ] Sub-task: Create a test script demonstrating the creation of a parent and child task in the exact same payload.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Validation (Parent/Child Linking)' (Protocol in workflow.md)