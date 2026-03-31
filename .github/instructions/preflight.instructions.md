---
name: Preflight Gate
description: Mandatory preflight gate for governance repositories
applyTo: "**"
---

# Hard preflight gate

- Read the mandatory files for the active context before technical output.
- Start the response with `Preflight OK: <file1>, <file2>, ...`.
- If preflight is incomplete, reply only `BLOCKED: preflight incompleto` and one objective next action.
- Keep this repository scoped to docs/governance only and do not treat it as the owner of product code.
- Critical gate and routing behavior must also live in `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.
