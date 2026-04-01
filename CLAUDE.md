# CLAUDE.md - Workflow Orchestration (Preflight Prompt)

Canonical precedence: `.copilot/base-instructions.md` -> `CLAUDE.md` -> `.github/copilot-instructions.md`.

## Workflow orchestration

- Plan first for non-trivial docs/governance work.
- Re-plan when evidence changes.
- Prefer the smallest safe change that preserves repository teaching content.
- Keep this repository scoped to docs/governance only.
- Read `PRE-FLIGHT-PROMPT.md` before editing the reusable prompt architecture or teaching content.
- Run `python ./tools/governance/audit-compliance.py` and `python ./tools/governance/verify-precedence.py` after baseline changes.

## Tasks governance (mandatory)

- Read `tasks/todo.md` and `tasks/lessons.md` before technical work.
- If `tasks/` is missing, create `tasks/todo.md` and `tasks/lessons.md` before technical work and preserve the canonical top blocks.
- Keep the plan updated during execution.
- `tasks/lessons.md` must preserve the exact canonical top block.
- New lessons must be appended as dated entries below the template.
- Historical lessons must never be replaced by placeholders.
- `tasks/todo.md` must track the current non-trivial work with objective, execution plan, expected evidence, and status/result.

## CLI-native parity note

- `PRE-FLIGHT.md` is not, by itself, a native Copilot CLI enforcement surface.
- Critical gate and routing behavior must live in `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`.
- `.github/skills/*/SKILL.md` and `.opencode/skills/*/SKILL.md` support the workflow; they are not the sole enforcement layer.
- OpenCode command discovery uses `.opencode/commands/`.

## Context7 documentation policy (mandatory)

- Use Context7 before implementation, refactor, and review work.

## MCP credential discovery and connection consent (mandatory)

- Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).
- Discovery must cover workspace/project files, OpenCode config, `.copilot/mcp-config.json`, VS Code `profiles/*/mcp.json`, `~/.gemini/antigravity/mcp_config.json`, and referenced environment variables such as `CONTEXT7_API_KEY`.
- Treat GitHub Copilot CLI as a first-class runtime alongside OpenCode, Copilot VS Code, and Gemini/Antigravity.

## Governance automation (mandatory)

- Secret scan: `./tools/governance/scan-secrets.ps1`
- Instruction sync: `python ./tools/governance/sync-instructions.py`
- Compliance audit: `python ./tools/governance/audit-compliance.py`
- Precedence audit: `python ./tools/governance/verify-precedence.py`

## Mandatory multi-agent orchestration skill

- For non-trivial docs/governance work, apply `orchestrate-multi-agents` before implementation and keep the `Template DAG 100% compliance`.
- Owners/tasks may be reduced when not applicable, but mandatory gates cannot be removed.
- For non-trivial tasks, instantiate the `Template DAG 100% compliance` from `orchestrate-multi-agents`; owners/tasks may be reduced only when not applicable, but mandatory gates cannot be removed.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.
