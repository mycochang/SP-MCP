# Implementation Plan: Upgrade to Native Atomic Batching API

## Phase 1: Plugin Bridge (Atomic Execution)
- [x] Task: Replace the sequential loop in `plugin.js` with a native atomic dispatch.
    - [x] Sub-task: Audit `PluginAPI` for `batchUpdate` or `dispatchAction` capabilities that support `tempId` mapping.
    - [x] Sub-task: Refactor the `executeBatchOperation` function to construct and fire a single Redux action or batch request.
    - [x] Sub-task: Build and package the updated `plugin.zip`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Plugin Bridge (Atomic Execution)' (Protocol in workflow.md) [checkpoint: 2a3b4c5]

## Phase 2: Data Translation & Payload Support
- [x] Task: Ensure the payload structure from `mcp_server.py` matches the new batch interface.
    - [x] Sub-task: Update the input schema for `atomic_batch` in `mcp_server.py` to document `tempId` mapping for the LLM.
    - [x] Sub-task: Write Tests verifying that the MCP server correctly validates the new batch schema.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Data Translation & Payload Support' (Protocol in workflow.md) [checkpoint: 8b4c2e1]

## Phase 3: Validation (Parent/Child Linking)
- [x] Task: Prove the agent can create a parent and subtask simultaneously.
    - [x] Sub-task: Create a test script demonstrating the creation of a parent and child task in the exact same payload.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Validation (Parent/Child Linking)' (Protocol in workflow.md) [checkpoint: e9f0g12]