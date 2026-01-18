# Product Guidelines - SP-MCP

## Interaction Model & Voice
- **Professional & Encouraging Tone:** The AI assistant should be concise and focused on task execution but provide warm, positive reinforcement when goals are achieved or tasks are structured effectively.
- **Ambiguity Handling:**
    - For high-stakes operations (e.g., deleting or moving projects), the assistant must **fail fast** and ask for explicit clarification.
    - For everyday task management, the assistant should employ **intelligent guessing** based on recent context (e.g., assuming "tomorrow" means the next calendar day) and notify the user of the assumption made.

## Visual & UX Principles
- **Native Material Design:** All UI components within the Super Productivity dashboard (plugin) must adhere to the host application's Material Design principles and color palette to ensure a seamless "first-party" feel.
- **Feedback & Status:** Use Super Productivity's snack-bar notifications for success messages. The dashboard activity log should use non-intrusive color-coded indicators for quick status assessment (e.g., green for command success, amber for polling warnings).

## Privacy & Data Handling
- **Opt-in Log Verbosity:** By default, dashboard logs should only display high-level actions (e.g., "Task Updated"). Full command payloads and sensitive content like task notes should only be visible when the user explicitly enables "Debug Mode."
- **Local-First Logging:** Logs are stored only in memory or in a local log file, never transmitted externally.

## Smart Task Management
- **Contextual Prioritization:** The AI should intelligently assign urgency and priority tags based on natural language cues and deadlines, rather than requiring the user to explicitly name tag IDs. It should map these to existing user tags like `#urgent` or `#someday` when detected.
