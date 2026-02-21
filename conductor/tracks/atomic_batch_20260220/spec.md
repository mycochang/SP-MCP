# Specification: Upgrade to Native Atomic Batching API

## Overview
Refactor the `atomic_batch` tool to utilize Super Productivity's true transactional state mutation capabilities (e.g., native `PluginAPI.batchUpdate` or direct Redux `dispatchAction`). Currently, `plugin.js` executes batch operations via a sequential `for` loop of individual `addTask` or `updateTask` calls, which is not truly atomic and causes race conditions or UI flickering during massive agent triage operations.

## Functional Requirements
1. **Plugin Bridge (Atomic Execution):** Replace the sequential loop in `plugin.js` with a single, atomic dispatch to Super Productivity's store.
2. **Data Translation (tempId Support):** Ensure the payload structure coming from `mcp_server.py` supports mapping operations (e.g., creating a parent task and a subtask simultaneously using temporary IDs).
3. **MCP Server Refactor:** Ensure the `atomic_batch` tool in `mcp_server.py` accurately describes the supported batching interface to the LLM.

## Non-Functional Requirements
- **True Atomicity:** If one operation in the batch fails validation before dispatch, the entire batch must fail without modifying the Super Productivity database.
- **Performance:** Massive triage operations (e.g., creating 20 tasks) must occur in a single UI render cycle.

## Acceptance Criteria
- The agent can create a parent task and a subtask simultaneously in a single `atomic_batch` call using `tempId` linking.
- A test script proves that a batch operation executes as a single transaction rather than a sequence of individual API calls.