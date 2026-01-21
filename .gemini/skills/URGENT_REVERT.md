# 🚨 URGENT: Revert Recommendation & Crash Analysis

**Status:** The current `sp-mcp-bridge` plugin architecture is causing **Critical Renderer Freezes** on the user's CachyOS (Linux) system.

**The Trigger:**
Pressing "D" (Mark Task Done) instantly freezes the UI.

**The Cause:**
The `taskComplete` hook (and likely others) performs an `await` on `sendEventToMCP`. This tries to execute a Node.js script via `PluginAPI.executeNodeScript` to write a JSON file.

- **Hypothesis:** The IPC call to the main process or the file I/O is blocking the UI thread, or entering a race condition with the App's native "Done" logic (Sound + Animation + DB Update).

**Recommendation for Next Build:**

1.  **DISABLE ALL HOOKS:** Comment out `registerHook` calls in `plugin.js`.
    - _Why:_ Passive polling (Python side) is safe. Active pushing (Plugin side) is lethal right now.
2.  **Revert to "Read-Only" Plugin:** The plugin should only _respond_ to commands, never _initiate_ actions.
3.  **Investigate Async:** If hooks are needed, they must not use `await`. They should be "Fire and Forget" with a `catch` block that does not bubble up errors to the App.

**Immediate Action:**
We are instructing the user to disable the plugin entirely. Please produce a stable "v0.1-safe" build that removes all event listeners.
