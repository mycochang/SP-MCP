# Feature Request: Add Tag Assignment to update_task

**Goal:** Allow users/agents to assign tags to tasks using the `update_task` tool.

**Context:**
The current `update_task` tool supports title, notes, is_done, etc., but lacks the ability to modify tags. We need this to organize tasks into the "Psych Flow" quadrants (Urgent/Now/Soon/Later) which are tag-based.

**Requirements:**

1.  **Update Input Schema:** Modify the `update_task` tool definition in `mcp_server.py`.
    - Add an optional `tag_ids` property.
    - Type: `array` of `string`.
    - Description: "List of tag IDs to assign".

2.  **Update Implementation:** Modify the `update_task` method.
    - Check if `tag_ids` is present in `args`.
    - If present, add it to the `updates` dictionary as `tagIds` (camelCase, matching Super Productivity's internal model).

**Example Usage:**

```python
# Agent calls:
update_task(task_id="123", tag_ids=["TAG_URGENT", "TAG_DEEP_WORK"])
```

**Verification:**

- Ensure the JSON payload sent to the plugin command file includes `"tagIds": [...]`.

Please implement this cleanly and commit the changes.
