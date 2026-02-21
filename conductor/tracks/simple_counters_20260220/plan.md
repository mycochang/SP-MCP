# Implementation Plan: Implement Native SimpleCounters API

## Phase 1: Upstream Analysis & UI Verification
- [ ] Task: Audit Super Productivity upstream repository for SimpleCounter mechanisms.
    - [ ] Sub-task: Analyze `plugin-bridge.service.ts` for exposed `PluginAPI` counter methods.
    - [ ] Sub-task: Analyze `simple-counter.model.ts` for expected data structures.
    - [ ] Sub-task: Investigate UI rendering logic for top-bar simple counters.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Upstream Analysis & UI Verification' (Protocol in workflow.md)

## Phase 2: Bridge Implementation (JavaScript)
- [ ] Task: Refactor `updateCounter` in `plugin.js` to use native API methods.
    - [ ] Sub-task: Remove the fake JSON-based counter stub.
    - [ ] Sub-task: Map `update_counter` requests to native `setCounter` or `incrementCounter` methods.
    - [ ] Sub-task: Build and package the updated `plugin.zip`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Bridge Implementation (JavaScript)' (Protocol in workflow.md)

## Phase 3: Python Schema Updates
- [ ] Task: Ensure `mcp_server.py` exposes correct types and schemas for LLM interaction.
    - [ ] Sub-task: Update `update_counter` tool definitions with documented `counter_id` mappings (e.g., 'daily-pushups').
    - [ ] Sub-task: Write Tests for the updated schema.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Python Schema Updates' (Protocol in workflow.md)