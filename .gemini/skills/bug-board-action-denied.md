# Bug Report: Board Creation Action Denied

**Context:**
We attempted to extend the MCP plugin to support `create_board` by mapping it to the `[Boards] Add Board` NgRx action. We patched `allowed-plugin-actions.const.ts` to include `addBoard` and rebuilt the app.

**Error:**
When calling `super-productivity_create_board`, the app returned:
`{'success': False, 'error': "Action type '{{type}}' is not allowed", ...}`

**Analysis:**

1.  **Action Whitelisting:** We added `addBoard` to `allowed-plugin-actions.const.ts`.
2.  **Plugin Logic:** We updated `plugin.js` to dispatch `{ type: '[Boards] Add Board', boardCfg: command.data }`.
3.  **The Error Message:** The error `Action type '{{type}}' is not allowed` comes from `plugin-api.ts` (or the bridge) when `isAllowedPluginAction` returns false.

**Hypothesis:**

- The import `import { addBoard } from '../features/boards/store/boards.actions';` might be tree-shaking incorrectly or the action object structure at runtime doesn't match the check.
- Or the rebuild didn't actually apply the changes to the running binary (caching issue?).

**Action Required:**
Investigate why `addBoard` is still considered "disallowed" despite being in the array.
