# Product Guidelines

## 1. Technical Design Principle
- **Strongly Typed APIs:** The MCP server code must prioritize strict JSON/RPC structures. Each endpoint and tool definition must be robustly type-checked (e.g., using TypedDict or Pydantic where applicable) and clearly documented. This ensures reliable serialization and deserialization between the AI agent and the Super Productivity environment.

## 2. Error Handling
- **AI-Friendly Errors:** The system must not silently fail. When unexpected inputs or logic errors occur, return explicit, descriptive error messages designed specifically for an AI to parse. The error should explain *why* it failed and provide actionable hints so the AI can correct its parameters and retry.

## 3. Documentation Strategy
- **Balanced Approach:** 
  - **Code Level:** Strive for self-documenting code with clear function names, explicit type hints, and necessary inline comments.
  - **External Level:** Maintain clear markdown files, cheat sheets (like the Super Productivity Cheat Sheet), and README instructions for setup and usage. External docs should focus on "how to use" and "how it works."

## 4. Operational Guardrails
- **Data Safety:** Never execute destructive or bulk actions without a clear mechanism for atomic updates or rollback. 
- **Context Preservation:** Ensure the AI is guided to "Observe" before it "Acts," enforcing a read-first workflow to prevent blind modifications to a user's task list.