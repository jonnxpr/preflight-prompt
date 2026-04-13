---
trigger: always_on
---

# Development Standards Rule

## Scope

- Docs/governance only.
- No product code ownership.
- Preserve explicit sibling-governance boundaries and repo-local ownership elsewhere.

## Always-on rules

- Follow the canonical precedence `.copilot/base-instructions.md` -> `CLAUDE.md` -> `.github/copilot-instructions.md`.
- Keep critical gate and routing behavior in native instruction surfaces, not only in skill files.
- Treat `.github/skills/*/SKILL.md` and `.opencode/skills/*/SKILL.md` as reinforcement layers.
- OpenCode command discovery uses `.opencode/commands/`.
- Read `tasks/todo.md` and `tasks/lessons.md` before technical work when they exist.
- If `tasks/` is missing, create both files before technical work and preserve the canonical top blocks.
- `tasks/lessons.md` must preserve the exact canonical top block.
- New lessons must be appended as dated entries below the template.
- Historical lessons must never be replaced by placeholders.
- `tasks/todo.md` must track the current non-trivial work with objective, execution plan, expected evidence, and status/result.
- Use Context7 before implementation, refactor, and review decisions.
- Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.
