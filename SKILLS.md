# Super Productivity MCP Agent Skills

This document defines standard workflows and skills for AI agents interacting with the Super Productivity MCP server.

## Skill: Summarize Workload (Contextual Grouping)

**Goal:** Retrieve all tasks and organize them by their Projects and Tags to provide a high-level overview of the current workload.

**Tools Required:**
- `get_projects`
- `get_tags`
- `get_tasks`

**Procedure:**

1.  **Fetch Context Data:**
    - Call `get_projects` to retrieve all available projects.
    - Call `get_tags` to retrieve all available tags.
    - Call `get_tasks` to retrieve the complete task list.

2.  **Correlate & Group:**
    - **Project Map:** Create a mapping of `projectId` to `project.title`.
    - **Tag Map:** Create a mapping of `tagId` to `tag.title`.
    - **Group by Project:** Iterate through all tasks. Assign each task to its corresponding Project based on `projectId`. If `projectId` is missing, group under "Unassigned".
    - **Group by Tag:** Iterate through all tasks. For each ID in `task.tagIds`, assign the task to the corresponding Tag group.

3.  **Synthesize Response:**
    - Present the user with two distinct views:
        1.  **Tasks by Project:** A list of projects with their associated active tasks.
        2.  **Tasks by Tag:** A list of tags with their associated active tasks.
    - *Optional:* Flag tasks that appear in "Urgent" or "High Priority" tags.

---

## Skill: Clean Up Old Tasks

**Goal:** Identify and archive tasks that have been completed for a long time.

**Tools Required:**
- `get_tasks`
- `complete_and_archive_task` (Note: SP-MCP currently supports marking as done/archiving via update, but not hard deletion)

**Procedure:**
1. Call `get_tasks` with `include_done=true`.
2. Filter for tasks where `isDone` is `true`.
3. (Agent Decision) Based on user criteria (e.g., "older than 2 weeks"), identify candidates.
4. Report candidates to user for confirmation.
5. (On Confirmation) Since tasks are already "done", ensure they are moved to the archive list or hidden from main view (implementation depends on SP internal logic).

---

## Meta-Skill: Designing New Agentic Workflows ("The Specialist Pattern")

**Goal:** Standardize the creation of high-performance, hybrid Human/AI workflows by leveraging specialized subagents. Use this pattern when you need to automate a complex task without cluttering the main context or slowing down the interaction.

### The 5-Step Workflow Creation Process

#### 1. Define the Intent
*   **Trigger:** What starts this workflow? (e.g., "I'm stuck," "Check Taiga")
*   **Agent Role:** What does the specialist do? (e.g., Planner, Curator, Researcher)
*   **Human Role:** What is the approval step? (e.g., Review Plan, Select Items)
*   **Outcome:** What is the tangible result in Super Productivity?

#### 2. Create the Track
*   Define the implementation task in Super Productivity to track progress.

#### 3. Architect the Agent ("The Who")
*   **Pattern:** **Main Agent as Router, Subagent as Worker.**
*   **Model Choice:** Use **Gemini 1.5 Flash** (or equivalent fast/cheap model) for the subagent.
    *   *Why?* Low latency (~0.1s), zero context overhead (fresh start), high throughput.
*   **Configuration:** Create `~/.config/opencode/agents/[specialist].json`. Limit tools to *only* what is needed (Principle of Least Privilege).

#### 4. Codify the Skill ("The How")
*   **Location:** Add to `instructions.md` or `AGENTS.md`.
*   **The "Secret Sauce" Prompt:**
    *   **Explicit Context Passing:** The Main Agent MUST read relevant data (e.g., Task Description, Project Files) *first* and pass it in the prompt. Do not assume the subagent knows what "this task" means.
    *   **Structured Output:** Instruct the subagent to return JSON or a Markdown list for easy parsing.

#### 5. Execute & Iterate ("The Loop")
*   **The Hybrid Handshake:** The subagent should rarely write to the database directly. It should return a *proposal*.
*   **Main Agent Responsibility:** Present the proposal to the human -> Get Approval -> Execute the Write.

### Key Design Principles (Learnings)
1.  **Zero Context Overhead:** Subagents spawn fresh. This keeps them fast and focused.
2.  **Explicit Context:** If the subagent needs to know the "Task Notes", the Main Agent must fetch and inject them.
3.  **No "Ghost Writes":** Always ask for confirmation before creating or deleting data based on a subagent's logic.
