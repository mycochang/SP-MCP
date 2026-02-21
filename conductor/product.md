# Initial Concept
Provide a seamless, context-rich bridge between the Super Productivity app and MCP servers (like OpenCode CLI and Gemini CLI).

# Product Guide

## 1. Vision & Purpose
The SP-MCP bridge transforms Super Productivity from a standalone application into an AI-accessible powerhouse. The primary goal is to provide **Full Feature Parity** while heavily prioritizing **Data Synchronization & Context** (the "main squeeze"). This enables AI agents to deeply understand a user's workload, past metrics, and active context to help manage tasks, projects, and tags via natural language. 

## 2. Target Audience
- **AI Tool Users / Devs:** Developers leveraging Claude Desktop, OpenCode CLI, or Gemini CLI who want automated task management.
- **SP Power Users:** Users of Super Productivity seeking natural language task input and AI-assisted organization.
- *(Future Roadmap)* **General Productivity Users:** As the tool matures, it aims to support non-technical users managing their daily productivity and workflows.

## 3. Core Features
1. **Task Management:** Seamless creation, updating, completion, and querying of tasks and sub-tasks.
2. **Project/Tag Organization:** Full lifecycle management (creating, reading, assigning) for projects and custom tags.
3. **Workload Analytics:** Providing detailed insights, real-time statistics, and historical metrics to the AI to understand workload distribution.
4. **Executive Function Support:** Acting as a scheduling aid to help mitigate executive function overload by automating triage and prioritization.
5. **Habit & Focus Tracking:** Integrating with native Simple Counters to manage daily habits, focus scores, and custom metrics (e.g., 'Coffee', 'Pomodoros').
6. **ADHD Prioritization:** Leveraging AI to propose 'Smart Triage' and Quadrant Tags (Urgent/Now/Soon/Later) for rapid focus management.

## 4. Operational Philosophy
The server must prioritize context-awareness. It should provide read-only tools for the AI to "Observe" the user's state, followed by strict, safe write tools to "Act." This ensures safe, atomic execution of tasks without accidentally corrupting the user's local Super Productivity data.