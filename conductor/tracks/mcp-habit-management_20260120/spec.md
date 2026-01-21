# Specification: Implement MCP Habit Management

## 1. Overview
The Super Productivity Plugin API has been updated to include native support for Habits (specialized `SimpleCounter` entities). This track aims to expose these capabilities to the MCP server, allowing the AI to programmatically create, check (increment), update, and list habits.

A key workflow requirement is to **always verify** if a habit exists before attempting to add it, preventing duplicates.

## 2. Functional Requirements
- **FR1 - Create Habit:** Implement `add_habit` tool that wraps `PluginAPI.addHabit`.
- **FR2 - Check Habit:** Implement `check_habit` tool that wraps `PluginAPI.checkHabit`.
- **FR3 - Update Habit:** Implement `update_habit` tool that wraps `PluginAPI.updateHabit`.
- **FR4 - List Habits:** Implement `list_habits` tool that wraps `PluginAPI.getAllSimpleCounters`.
    - **Note:** This tool should return all counters to provide full visibility.
- **FR5 - Existence Verification:** The AI workflow for "Add Habit" MUST first call `list_habits` to check for existing habits with the same title to avoid duplicates.

## 3. Non-Functional Requirements
- **NFR1 - Compatibility:** Must strictly adhere to the signatures defined in `HANDOFF_TO_MCP.md`.
- **NFR2 - Robustness:** Tools must handle potential API failures gracefully (e.g., if the plugin is outdated or the API is missing).

## 4. Acceptance Criteria
- [ ] **AC1:** `add_habit` successfully creates a new habit in Super Productivity.
- [ ] **AC2:** `check_habit` successfully increments the count for a specific habit.
- [ ] **AC3:** `update_habit` successfully modifies a habit's configuration (e.g., title or min streak).
- [ ] **AC4:** `list_habits` returns a list of all simple counters/habits.
- [ ] **AC5:** Attempting to add a duplicate habit (same title) is flagged or prevented by the workflow (verified via test).

## 5. Out of Scope
- `delete_habit` (Manual operation only).
- `addSimpleCounter` (We are focusing on the high-level "Habit" abstraction for now).
