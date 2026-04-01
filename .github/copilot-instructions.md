# Copilot Root Instructions - Preflight Prompt

## Required loading order

1. `.copilot/base-instructions.md`
2. `CLAUDE.md`
3. `.github/copilot-instructions.md`
4. `.github/instructions/*.instructions.md`
5. `.github/skills/development-standards/SKILL.md`
6. `.opencode/skills/development-standards/SKILL.md`
7. `.agent/rules/development-standards.md`

## Hard preflight gate (mandatory)

- Read every mandatory file for the active context before technical output.
- Start the response with `Preflight OK: <file1>, <file2>, ...`.
- If preflight is incomplete, reply only `BLOCKED: preflight incompleto` and one objective next action.

## Scope

- This repository is the canonical home for the reusable preflight-prompt docs/governance surface and its local governance toolkit.
- Docs/governance only.
- No product code ownership.
- Keep sibling-governance boundaries explicit.

## CLI-native parity note

- `PRE-FLIGHT.md` is not, by itself, a native Copilot CLI enforcement surface.
- Critical gate and routing behavior must also live in `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`.
- `.github/skills/*/SKILL.md` and `.opencode/skills/*/SKILL.md` reinforce the contract; they are not the sole enforcement layer.
- OpenCode command discovery uses `.opencode/commands/`.
- Treat GitHub Copilot CLI as a first-class runtime alongside OpenCode, Copilot VS Code, and Gemini/Antigravity.

## Tasks governance (mandatory)

- Read `tasks/todo.md` and `tasks/lessons.md` before technical work when `tasks/` exists.
- If `tasks/` is missing, create both files before technical work and preserve the canonical top blocks.
- `tasks/lessons.md` must preserve the exact canonical top block.
- New lessons must be appended as dated entries below the template.
- Historical lessons must never be replaced by placeholders.
- `tasks/todo.md` must track the current non-trivial work with objective, execution plan, expected evidence, and status/result.

## Context7 documentation policy (mandatory)

- Use Context7 before implementation, refactor, and review work.

## MCP credential discovery and connection consent (mandatory)

- Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).
- Discovery must cover workspace/project files, OpenCode config, `.copilot/mcp-config.json`, VS Code `profiles/*/mcp.json`, `~/.gemini/antigravity/mcp_config.json`, and referenced environment variables such as `CONTEXT7_API_KEY`.

## Mandatory multi-agent orchestration skill

- For non-trivial docs/governance work, apply `orchestrate-multi-agents` before implementation and keep the `Template DAG 100% compliance`.
- Owners/tasks may be reduced when not applicable, but mandatory gates cannot be removed.
- For non-trivial tasks, instantiate the `Template DAG 100% compliance` from `orchestrate-multi-agents`; owners/tasks may be reduced only when not applicable, but mandatory gates cannot be removed.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.
