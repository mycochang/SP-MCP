---
name: sp-mcp
description: "Integration guide for the Super Productivity MCP server. Use this skill when managing tasks, projects, tags, or Kanban boards in Super Productivity via the connected MCP server to ensure proper syntax formatting and API usage."
---

# Super Productivity MCP Integration Guide

This skill teaches the agent how to correctly interact with the `super-productivity` MCP server. The most critical part of this integration is formatting the `title` field when creating or updating tasks, as the Super Productivity app natively parses special syntax from the task title string.

## Tool Usage & Syntax Rules

When calling the `create_task` or `update_task` tools, you MUST parse the user's natural language request and format the `title` argument using Super Productivity's native syntax.

### 1. Scheduling & Dates (`@`)
Convert all natural language date/time references into `@` syntax relative to TODAY.
*   **Format:** `@Xdays`, `@Yweeks`, `@Zmonths` or specific days/times.
*   **Examples:**
    *   "tomorrow" -> `@1days`
    *   "next week" -> `@7days`
    *   "in 2 months" -> `@2months`
    *   "Friday at 3pm" -> `@fri 3pm`
*   *Do not* put natural language dates directly in the title. Always convert them.

### 2. Projects (`+`)
Append project assignments to the title using the `+` prefix.
*   **Format:** `+ProjectName` (No spaces in the project name syntax)
*   **Examples:**
    *   "Create a task for the Website Redesign project" -> `title: "Create a task +WebsiteRedesign"`

### 3. Tags (`#`)
Append tags to the title using the `#` prefix.
*   **Format:** `#TagName` (No spaces in the tag name)
*   **Examples:**
    *   "Buy milk (urgent)" -> `title: "Buy milk #urgent"`

### 4. Time Estimates (`time_estimate`)
While SP supports time estimates in the title (e.g., `2h/3h`), the MCP tool `create_task` provides a specific `time_estimate` argument.
*   Pass time estimates in **milliseconds** via the `time_estimate` argument.
*   **Example:** 2 hours = `7200000` milliseconds.

## Example Workflows

### Creating a Task
**User:** "Create a high priority task to review the quarterly budget for the Finance project by next Monday. It should take about 3 hours."

**Agent Action:**
1.  Parse tags: `#highPriority`
2.  Parse project: `+Finance`
3.  Parse schedule: Next Monday -> `@mon` or `@7days` (depending on current day)
4.  Parse time: 3 hours -> `10800000` ms
5.  Call tool:
    ```json
    {
      "title": "Review the quarterly budget @mon #highPriority +Finance",
      "time_estimate": 10800000
    }
    ```

### Updating a Task
If the user wants to push a task back or mark it complete:
*   To mark complete: Use the `complete_and_archive_task` tool with the `task_id`. (Do not try to delete tasks, deletion is not supported via the API).
*   To reschedule: Use `update_task` and modify the title with the new `@` syntax.
*   To replace all tags: Use `update_task` and provide an array of UUIDs to the `tag_ids` argument. Note: This *replaces* existing tags. If the user just wants to add a tag, it's easier to fetch the task, get existing tags, and append the new one.

### Managing Projects & Tags
*   Use `get_projects` and `get_tags` to query existing categories.
*   Use `create_project` (requires `title`, `description`, `color` hex) and `create_tag` to establish new organizational structures.

## Limitations
*   **True deletion is not supported** via the plugin API. If a user asks to delete a task, use `complete_and_archive_task` instead and inform the user.
*   The communication is file-based (polling). Responses usually take 1-3 seconds. Be patient when waiting for tool results.
