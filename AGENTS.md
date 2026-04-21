# OpenCode Instructions - Preflight Prompt

Canonical precedence: `.copilot/base-instructions.md` -> `CLAUDE.md` -> `.github/copilot-instructions.md`.

## Caveman Always-On (mandatory)

Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop caveman" / "normal mode".

## Scope

- This repository is the canonical home for the reusable preflight-prompt docs/governance surface and its local governance toolkit.
- Docs/governance only.
- No product code ownership.
- Read `PRE-FLIGHT-PROMPT.md` before editing the reusable prompt architecture or teaching content.
- Run the local governance audits after baseline changes.

## Hard preflight gate (mandatory)

- Read `README.md`, `PRE-FLIGHT-PROMPT.md`, `.copilot/base-instructions.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, applicable `.github/instructions/*.instructions.md`, and `.agent/rules/development-standards.md` before technical output.
- If `tasks/` exists, read `tasks/todo.md` and `tasks/lessons.md`; if `tasks/` is missing, create both first.
- Start the response with `Preflight OK: <file1>, <file2>, ...`.
- If preflight is incomplete, reply only `BLOCKED: preflight incompleto` and one objective next step.
- For commit creation or commit-message generation, read `.github/copilot-commit-message-instructions.md`.

## CLI-native parity note

- `PRE-FLIGHT.md` is governance memory, not the sole native enforcement surface for GitHub Copilot CLI.
- Keep critical gate and routing behavior in `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`; `.github/skills/*/SKILL.md` and `.opencode/skills/*/SKILL.md` only reinforce that contract.
- OpenCode command discovery uses `.opencode/commands/`.

## Tasks governance (mandatory)

- Read `tasks/todo.md` and `tasks/lessons.md` when `tasks/` exists; otherwise create both using the canonical top blocks.
- Preserve those canonical top blocks, append dated lessons without replacing history, and keep `tasks/todo.md` updated with objective, execution plan, expected evidence, and status/result.

## Plan persistence (mandatory)

- When a non-trivial plan is finalized (S1+ orchestration mode or 3+ steps), save it to `plans/` in the owning repo as `plan-${camelCaseName}.prompt.md`.
- `plans/` captures rationale, context, constraints, and alternatives (the "why"). `tasks/todo.md` captures status tracking and checkboxes (the "what/when").
- Agents must read active plans from `plans/` before starting related work.
- After execution starts, plans are append-only. Mark status as `completed` when the corresponding `tasks/todo.md` objective is completed with evidence.
- For non-git hubs, plans go in the versioned governance sibling (e.g., `partner-governance/plans/`).

## Context7 documentation policy (mandatory)

- Use Context7 before implementation, refactor, and review work.

## MCP credential discovery and connection consent (mandatory)

- Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).
- Discovery must cover workspace/project files, OpenCode config, `.copilot/mcp-config.json`, VS Code `profiles/*/mcp.json`, `~/.gemini/antigravity/mcp_config.json`, and referenced environment variables such as `CONTEXT7_API_KEY`.
- Treat GitHub Copilot CLI as a first-class runtime alongside OpenCode, Copilot VS Code, and Gemini/Antigravity.
- If credentials are not found, report exactly: `credentials not found for requested MCP`.

## Skill routing

- Implementation/refactor: `development-standards`.
- Review/PR: `development-standards` + `code-review`.
- GitHub repository, workflow run, pull request, issue, release, or project-status work via `gh`: also load `.github/skills/gh-operations/SKILL.md` or `.opencode/skills/gh-operations/SKILL.md`.

## Governance automation (mandatory)

- Secret scan: `./tools/governance/scan-secrets.sh`; instruction sync: `python3 ./tools/governance/sync-instructions.py`; compliance audit: `python3 ./tools/governance/audit-compliance.py`; precedence audit: `python3 ./tools/governance/verify-precedence.py`

## Mandatory multi-agent orchestration skill

- For non-trivial docs/governance work, apply `orchestrate-multi-agents` before implementation and keep the `Template DAG 100% compliance`; owners/tasks may be reduced only when not applicable, but mandatory gates cannot be removed.

## Integral instruction read (mandatory)

- Read all mandatory files from first line through last line.
- If the runtime returns only partial content, continue chunked reads until EOF.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.

## Commit-message rule (mandatory)

- Apply `.github/copilot-commit-message-instructions.md` for all commits.
- Use Conventional Commits format with PT-BR content.
