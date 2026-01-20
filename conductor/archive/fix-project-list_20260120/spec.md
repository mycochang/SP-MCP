# Specification: Fix Incomplete Project Listing in `get_projects`

## 1. Overview
The `get_projects` tool in the MCP server is reliably returning some projects but failing to list others. User observation indicates that missing projects might be:
1.  Recently created.
2.  Projects that initially had no tasks (and remained invisible even after tasks were added).

This track aims to investigate the root cause of this inconsistency within the `PluginAPI.getAllProjects()` integration and implement a fix to ensure *all* active projects are retrievable.

## 2. Functional Requirements
- **FR1 - Complete Project Retrieval:** The `get_projects` tool MUST return all active projects in Super Productivity, regardless of whether they have tasks or when they were created.
- **FR2 - Zero-Task Visibility:** Projects with zero tasks MUST be included in the returned list.
- **FR3 - Immediate Consistency:** Newly created projects MUST be visible in subsequent `get_projects` calls without requiring a restart or significant delay.

## 3. Non-Functional Requirements
- **NFR1 - Performance:** The fix should not significantly degrade the performance of the `get_projects` call.
- **NFR2 - Stability:** The solution must not introduce regressions in other project-related operations (e.g., creating tasks in those projects).

## 4. Acceptance Criteria
- [ ] **AC1:** A newly created project (via UI or MCP) appears in the `get_projects` list immediately.
- [ ] **AC2:** A project with 0 tasks appears in the `get_projects` list.
- [ ] **AC3:** A project with 1+ tasks appears in the `get_projects` list.
- [ ] **AC4:** The `get_projects` tool output matches the list of projects visible in the Super Productivity UI.

## 5. Out of Scope
- Fixing issues related to "Archived" projects (unless they are incorrectly appearing as active).
- Changes to the underlying Super Productivity internal API (we are limited to the exposed `PluginAPI` or finding workarounds).
