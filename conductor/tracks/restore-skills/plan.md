# Implementation Plan - Restore Skills

## Phase 1: Investigation & Configuration
- [x] **Analyze `activate_skill` Mechanism:** Tried `.gemini/settings.json`, `.gemini/skills/`, `.gemini/skills.json`. All failed to restore the tool.
- [x] **Inventory Prompts:** All prompts exist in `prompts/`.

## Phase 2: Restoration (Workaround)
- [ ] **Document Manual Activation:** Update `product-guidelines.md` or similar to instruct agents to read `prompts/` directly.
- [ ] **Create "Skill Index":** Maintain `conductor/skills.md` as a registry of available prompts/skills.

## Phase 3: Cleanup
- [ ] **Update Documentation:** Ensure future developers know how to "activate" skills manually.