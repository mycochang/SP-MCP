# Specification: Context-Aware OODA Loop for SP-MCP

## Overview
Refactor the Super Productivity MCP bridge to prioritize context-awareness and safe, atomic execution. This track introduces read-only tools for the AI to 'Observe' the user's active context and historical metrics, followed by strict, safe write tools (Atomic Batching and validated Counter updates) for the 'Act' phase. This is a Counter extension to our plugin.

## Core Goal
Provide the AI with accurate, read-only workload context to observe state, and enforce strict, safe writes via atomic batching.

## Functional Requirements
1. **Read-Only Observation Tools:** Implement tools to fetch the user's current active task, workload metrics, and context without allowing mutation during this phase.
2. **Atomic Batching for Writes:** Create an atomic batch operation tool that accepts multiple actions and executes them safely, preventing partial updates.
3. **Validated Counter Updates:** Implement a write tool specifically for the plugin's Counter extension that validates parameters prior to modification.
4. **Context Injection:** Hidden context injection for AI tasks.

## Non-Functional Requirements
- **Safety:** Read tools must strictly not mutate data.
- **Reliability:** Atomic operations must fully succeed or fail safely without corrupting the local Super Productivity state.
- **Strict Typing:** Ensure strong JSON/RPC typing on all new tools.

## Out of Scope
- Major UI changes to the Super Productivity desktop app.
- Non-atomic standard write tools outside of the new batching parameters.