---
name: Preflight Gate
description: Mandatory preflight gate for governance repositories
applyTo: "**"
---

# Hard preflight gate

- Read the mandatory files for the active context before technical output.
- Read `tasks/todo.md` and `tasks/lessons.md` before technical work when `tasks/` exists.
- If `tasks/` is missing, create both files before technical work using the exact canonical top blocks required by `PRE-FLIGHT.md`.
- `tasks/lessons.md` must preserve the exact canonical lessons top block.
- New lessons must be appended as dated entries below it.
- Historical lessons must never be replaced by placeholders.
- `tasks/todo.md` must preserve the exact canonical task-plan top block and track the current non-trivial work with objective, execution plan, expected evidence, and status/result.
- Start the response with `Preflight OK: <file1>, <file2>, ...`.
- If preflight is incomplete, reply only `BLOCKED: preflight incompleto` and one objective next action.
- Keep this repository scoped to docs/governance only and do not treat it as the owner of product code.
- Critical gate and routing behavior must also live in `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`.
- Run `python3 tools/governance/audit-compliance.py` before marking governance work complete.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.
