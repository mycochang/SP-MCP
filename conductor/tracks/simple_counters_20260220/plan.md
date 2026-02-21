# Implementation Plan: Implement Native SimpleCounters API

## Phase 1: Upstream Analysis & UI Verification
- [x] Task: Audit Super Productivity upstream repository for SimpleCounter mechanisms. [48a12c4]
    - [x] Sub-task: Analyze `plugin-bridge.service.ts` for exposed `PluginAPI` counter methods.
    - [x] Sub-task: Analyze `simple-counter.model.ts` for expected data structures.
    - [x] Sub-task: Investigate UI rendering logic for top-bar simple counters.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Upstream Analysis & UI Verification' (Protocol in workflow.md) [checkpoint: f53da79]

## Phase 2: Bridge Implementation (JavaScript)
- [x] Task: Refactor `updateCounter` in `plugin.js` to use native API methods. [93c4424]
    - [x] Sub-task: Remove the fake JSON-based counter stub.
    - [x] Sub-task: Map `update_counter` requests to native `setCounter` or `incrementCounter` methods.
    - [x] Sub-task: Build and package the updated `plugin.zip`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Bridge Implementation (JavaScript)' (Protocol in workflow.md) [checkpoint: e5dc342]

## Phase 3: Python Schema Updates
- [x] Task: Ensure `mcp_server.py` exposes correct types and schemas for LLM interaction. [b395f1f]
    - [x] Sub-task: Update `update_counter` tool definitions with documented `counter_id` mappings (e.g., 'daily-pushups').
    - [x] Sub-task: Write Tests for the updated schema.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Python Schema Updates' (Protocol in workflow.md) [checkpoint: 5c7ad50]