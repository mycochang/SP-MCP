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

---

## Skill: The Time-Boxed Arc

**Goal:** Execute a complex user goal with strict time-boxing, ensuring the human explicitly "clocks in" to the task before the agent begins work. This prevents "Time Blindness" and "Scope Creep."

**Tools Required:**
- `create_task`
- `create_subtask`
- `update_task` (for scope updates and post-mortems)
- `show_notification`

**Procedure:**

1.  **Scope & Estimate (The "Bid"):**
    - **Trigger:** User provides a goal (e.g., "Refactor the login logic").
    - **Action:** Analyze the request. Calculate a complexity estimate.
    - **Rule:** **You must propose a Time Estimate (in minutes/hours) before creating any task.**

2.  **The "Ritual" Setup:**
    - Call `create_task`:
        - `title`: The goal (e.g., "Refactor Login Logic").
        - `time_estimate`: The calculated bid (converted to ms).
        - `#tag`: Add `#AgentArc` or `#DeepWork` if available.
    - Call `create_subtask`:
        - `title`: **"▶️ CLICK START TIMER"** (Visual cue for the user).
        - `parent_id`: The ID of the main task.
    - **Wait State:** Inform the user: *"I have set up the task '[Task Name]' with a [Time] estimate. Please click the timer on that task in Super Productivity, then tell me 'Go'."*

3.  **Scope Defense (During Execution):**
    - **Trigger:** User adds a new request *during* the arc.
    - **Check:** Does this new request fit within the *current* `time_estimate`?
    - **If YES:** Proceed.
    - **If NO:** Stop.
        - **Refusal:** *"That is out of scope for our current [Time] session."*
        - **Offer:** *"I can 1) Add 15m to the current task, or 2) Create a new 'Later' task."*

4.  **The "Reflection" Loop (Post-Mortem):**
    - **Trigger:** User signals completion ("We are done").
    - **Action:**
        - Call `get_tasks` to retrieve the *actual* `timeSpent`.
        - Calculate Variance: `(timeSpent - timeEstimate) / timeEstimate`.
    - **Artifact:** Update the **Task Notes** with a "Velocity Report":
        ```markdown
        ### Agent Reflection
        - **Estimated:** 30m
        - **Actual:** 45m
        - **Variance:** +50%
        - **Learning:** Underestimated complexity of [Specific Detail].
        ```

## Skill: Fibonacci Inbox Triage

**Goal:** Rapidly estimate and categorize vague inbox tasks using relative Fibonacci sizing, translating them into strict time estimates for Super Productivity without tag pollution. Maps mental models directly to agile point systems.

**Tools Required:** `get_tasks`, `update_task`, `ask_user` (or interactive CLI prompts)

**The Fibonacci Time Matrix (No Tags):**
* **1 Point:** 15 minutes (900,000 ms) - Quick Win
* **2 Points:** 30 minutes (1,800,000 ms) - Short Task
* **3 Points:** 1 hour (3,600,000 ms) - Standard Task
* **5 Points:** 2 hours (7,200,000 ms) - Deep Work
* **8 Points:** 4 hours (14,400,000 ms) - Half Day
* **13+ Points:** Epic (8+ hours / 28,800,000+ ms) - *Requires breakdown*

**Procedure:**
1. **Observe (The Inbox):** Call `get_tasks(include_done=false)`. Filter for tasks where `timeEstimate == 0` AND `parentId == null`.
2. **Orient & Question:** Present the vague tasks to the user one by one or in a batch. Ask them to assign a Fibonacci point value (1, 2, 3, 5, 8, 13).
3. **Act (The Translation):** 
    * **If 1-8 Points:** Convert the points to milliseconds using the matrix above. Call `update_task` to set the `timeEstimate`. Do *not* add tags unless explicitly requested by the user. The time estimate itself is the single source of truth for task sizing.
    * **If 13+ Points:** Warn the user that the task is too large to estimate accurately. Immediately propose breaking it down. Ask the user for 2-3 specific sub-steps, create them as subtasks using `create_task(parent_id=...)`, and ask for Fibonacci points for the new subtasks.

---

## Skill: Pavlovian Time Tracker Nudge

**Goal:** Provide positive, philosophical reinforcement to encourage the user to build the habit of clicking the play button on their active tasks, preventing "dark" un-tracked time.

**Tools Required:** `get_tasks` (to observe state), `show_notification` (to act)

**Procedure:**
1. **Observe:** Whenever the agent is engaged for a standard prompt, silently call `get_tasks(include_done=false)`.
2. **Orient:** Identify the task the user is currently working on (e.g., the one they just asked you about, or the most recently created/updated active task). Check if its `timeSpent` is 0 or if there is an active session running (if the API exposes active status).
3. **Act (The Nudge):** If the user is actively working with the agent but hasn't tracked time, use the `show_notification` tool to send an OS-level audio/visual ping.
4. **The Message:** The notification MUST be positive, spiritual, or philosophical (e.g., Stoic, Taoist).
   * **Example:** "Nature does not hurry, yet everything is accomplished. Don't forget to start your timer." - Lao Tzu
   * **Example:** "The impediment to action advances action. Click play on your task." - Marcus Aurelius

---

## Skill: Weekly Productivity Audit (The "How did you know" Skill)

**Goal:** Act as a data-driven mirror for the user. Analyze the task database to reveal hidden psychological patterns, estimation biases, and workflow bottlenecks, and optionally save the findings to global memory.

**Tools Required:** `get_productivity_audit`, `memory_create_entities` (optional)

**Procedure:**
1. **Fetch:** Call the `get_productivity_audit` tool. This securely performs all mathematical analysis inside the Python MCP server without exploding the LLM token context.
2. **Synthesize & Report:** Present the statistical findings to the user as a "Psychological Profile". Focus on actionable insights:
   * *Did they overestimate?* (e.g., Time Spent / Estimated < 1.0). Tell them they have more free time than they think.
   * *Are old tasks rotting?* (e.g., Procrastination Window > 14 days). Suggest a backlog purge.
   * *Do notes help?* (e.g., Positive Clarity Premium). Reinforce the habit of writing 1-sentence descriptions before starting work.
3. **Persist (The Memory Graph):** Call the `memory_create_entities` tool from the global memory server to save the metrics as an Entity of type `Productivity_Audit` (e.g. `{"name": "Audit_2026_W08", "entityType": "Audit", "observations": ["Procrastination window: 14 days", "Estimation Accuracy: 0.81"]}`). This allows cross-domain agents to read the user's burnout or velocity metrics next week.

---

## [Gemini-Only] Skill: Inbox Triage & Staking (The OODA Pipeline)

**Goal:** Transform vague phone-dumps into actionable, frictionless tasks to prevent the 14-Day Decay.

**Tools Required:**
- `get_workload_metrics`
- `get_tasks`
- `get_tags`
- `update_task`

**Procedure:**

1.  **Observe (The Inbox):**
    - Call `get_workload_metrics()`. If `pendingTasks > 30`, bias heavily towards moving items to the Backlog or a "Someday" tag during orientation.
    - Call `get_tasks(include_done=false)`. Filter for tasks where `timeEstimate == 0` AND (`notes == null` or `notes == ""`). These are the "Vague Dumps".

2.  **Orient (The Stake):**
    - For each vague task, analyze the title and propose a "Stake" (Difficulty).
    - **Prompt to User:** "I see '[Task Title]'. Is this a 15m #quick-win, a 60m deep-work session, or does it need Refinement?"

3.  **Act (Refinement):**
    - **Time Staking:** If the user provides an estimate (e.g., "15m"), call `update_task(task_id=..., time_estimate=X)`. 
      - **CRITICAL:** Ensure X is converted to milliseconds (e.g., 15 minutes = 900,000 ms).
    - **Clarity Premium:** If the user says it needs refinement, ask for 2-3 bullet points. Call `update_task(task_id=..., notes=bullets)` to secure the +17% Clarity Premium.
    - **Decay Prevention:** If the task was created >14 days ago, suggest moving it to `#someday`.
      - **To apply #someday:** Call `get_tags()` to find the ID for "Someday". Call `update_task(task_id=..., tag_ids=["<Someday_Tag_ID>"])`.

---

## Skill: Autonomous Calendar Triage (Cross-Domain)

**Goal:** Prevent scheduling overwhelm by continuously balancing Super Productivity task workloads against Google Calendar meeting realities. Automate the backlog deferral process.

**Tools Required:** `google-workspace_get_events` (from google_workspace_mcp), `get_tasks` (from SP-MCP), `atomic_batch` (from SP-MCP)

**Procedure:**
1. **Observe (The Reality Check):**
    - Call `google-workspace_get_events(time_min="today 00:00:00", time_max="today 23:59:59")`. Sum the total duration of today's meetings.
    - Call `get_tasks(include_done=false)`. Filter for tasks scheduled for today or active in the current project context. Sum their `timeEstimate` values.
2. **Orient (The Math):**
    - Calculate Total Load: `(Meeting Hours) + (Task Estimates)`.
    - If Total Load > 8 hours (or the user's defined workday limit): Identify low-priority tasks, un-estimated tasks, or tasks lacking the `#urgent` tag that can be deferred to reduce the load below the threshold.
3. **Act (The Triage):**
    - Construct an `atomic_batch` payload to defer the overflow tasks.
    - To defer: Apply a `#someday` tag, move them to a backlog project, or clear their scheduling parameters.
    - Summarize the actions taken to the user: *"You have 4 hours of meetings and 6 hours of tasks. You are over capacity. I am moving 2 hours of low-priority tasks to the backlog."*

---

## Skill: The Oracle (Witty Motivation)

**Goal:** Provide a highly contextual, witty, or philosophical quote via a native UI modal to motivate the user based on their current workload.

**Tools Required:** `get_workload_metrics`, `observe_context`, `open_dialog`

**Procedure:**
1. **Observe:** Call `get_workload_metrics()` and `observe_context()` to understand the user's current situation (e.g., are they drowning in 100 pending tasks? Are they looking at a specific deep-work project?).
2. **Synthesize:** Based on the context, select or generate a witty, punchy, or stoic quote. (e.g., if overwhelmed: "You can do anything, but not everything." If inactive: "Action is the foundational key to all success.")
3. **Act:** Call `open_dialog` with beautifully formatted HTML to display the quote directly in Super Productivity.
   *Example HTML:* 
   ```html
   <div style="text-align:center; padding:20px;">
     <h2 style="color:#a05db1;">🔮 The Oracle Says...</h2>
     <p style="font-size:1.5em; font-style:italic;">"Your quote here."</p>
     <p><strong>- Author</strong></p>
   </div>
   ```
