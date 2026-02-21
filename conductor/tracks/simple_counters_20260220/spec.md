# Specification: Implement Native SimpleCounters API

## Overview
The current `update_counter` implementation in `plugin.js` is a fake stub that just saves to a JSON file. This track will replace that stub with true integration into Super Productivity's native SimpleCounter system, allowing counters to appear in the user's top navigation bar.

## Core Goal
Ensure that when an AI agent updates a counter (e.g., "focus_score"), the value is natively registered in Super Productivity, rendered in the UI, and synchronized via the app's native sync engine.

## Functional Requirements
1. **Upstream Analysis:** Analyze `plugin-bridge.service.ts` and `simple-counter.model.ts` in the upstream Super Productivity repo to understand the exact structure and requirements for `setCounter`, `incrementCounter`, and `getAllCounters`.
2. **UI Verification:** Investigate how Super Productivity renders SimpleCounters to ensure the data we inject meets the UI's expectations (e.g., specific ID formats or required initial states).
3. **Bridge Implementation:** Rewrite the `updateCounter` (and add any missing counter methods) in `plugin.js` to use the true native `PluginAPI` methods.
4. **Python Schema Update:** Update `mcp_server.py` to expose the correct string mapping for `counter_id` so the LLM understands how to target specific counters.

## Non-Functional Requirements
- **Native Persistence:** All counter data must be stored and synced exclusively via Super Productivity's native mechanisms. No local fallback files should be used to prevent split-brain state.
- **Strict Typing:** Ensure the Python schema clearly defines acceptable inputs for the counter values.

## Acceptance Criteria
- Calling `update_counter` from the LLM natively updates the corresponding SimpleCounter in Super Productivity.
- The updated counter is visibly rendered in the Super Productivity UI (e.g., top navigation bar).