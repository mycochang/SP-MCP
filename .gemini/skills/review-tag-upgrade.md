# Review Request for SP-MCP Upgrade

**Goal:** Review and merge recent changes to `mcp_server.py` which added `update_tag` and `delete_tag` capabilities.

**Context:**
We extended the MCP server to support full CRUD on Tags to enable an "ADHD Flow" workflow (Urgent/Now/Soon/Later). This required mapping the `theme_primary_color` parameter to the complex `theme` object expected by Super Productivity's internal API.

**Changes to Verify:**

1.  **Tool Definitions:** Are `update_tag` and `delete_tag` correctly defined in the `list_tools` schema?
2.  **Implementation:** Does `update_tag` correctly construct the `theme` object? (It blindly sets `huePrimary: '500'`, which is a safe default, but check if this overwrites user customizations).
3.  **Security:** Is `delete_tag` safe? (It just passes the ID to the plugin).

**Action:**
Please review `mcp_server.py` and confirm the implementation is robust. If approved, commit the changes.
