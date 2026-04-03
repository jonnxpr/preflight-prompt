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

## Plan persistence (mandatory)

- When a non-trivial plan is finalized (S1+ orchestration mode or 3+ steps), save it to `plans/` in the owning repo as `plan-${camelCaseName}.prompt.md`.
- `plans/` captures rationale, context, constraints, and alternatives (the "why"). `tasks/todo.md` captures status tracking and checkboxes (the "what/when").
- Agents must read active plans from `plans/` before starting related work.
- After execution starts, plans are append-only. Mark status as `completed` when the corresponding `tasks/todo.md` objective is completed with evidence.
- For non-git hubs, plans go in the versioned governance sibling (e.g., `partner-governance/plans/`).

## CLI-native parity note

- Shared CLI-native enforcement and command-discovery rules follow `AGENTS.md` and `.github/copilot-instructions.md`.

## Context7 documentation policy (mandatory)

- Use Context7 before implementation, refactor, and review work.

## MCP credential discovery and connection consent (mandatory)

- Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).
- Discovery must cover workspace/project files, OpenCode config, `.copilot/mcp-config.json`, VS Code `profiles/*/mcp.json`, `~/.gemini/antigravity/mcp_config.json`, and referenced environment variables such as `CONTEXT7_API_KEY`.
- Treat GitHub Copilot CLI as a first-class runtime alongside OpenCode, Copilot VS Code, and Gemini/Antigravity.

## Governance automation (mandatory)

- Run the local governance commands documented in `AGENTS.md` and `.github/copilot-instructions.md`.

## Mandatory multi-agent orchestration skill

- For non-trivial docs/governance work, apply `orchestrate-multi-agents` and keep the `Template DAG 100% compliance`.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.

## Orchestration Reference

- Operational matrix, modes, and parallelization rules: see `docs/orchestration-matrix.md`
- Orchestration templates (S0-S4): see `docs/orchestration-templates.md`
- validate-fast/full commands per ecosystem: see `docs/validate-catalog.md`
- Ownership registry schema: see `docs/ownership-registry-spec.md`
- Implementation roadmap: see `docs/implementation-roadmap.md`
