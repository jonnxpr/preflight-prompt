# PRE-FLIGHT - Preflight Prompt

Hard gate before any technical answer.

## Mandatory checklist

1. Read `README.md`.
2. Read `PRE-FLIGHT-PROMPT.md` before editing the reusable prompt architecture or teaching content.
3. Read `.copilot/base-instructions.md`.
4. Read `CLAUDE.md`.
5. Read `.github/copilot-instructions.md`.
6. Read applicable `.github/instructions/*.instructions.md`.
7. Read `.agent/rules/development-standards.md`.
8. If `tasks/` exists, read `tasks/todo.md` and `tasks/lessons.md` fully; if `tasks/` is missing, create both with the canonical templates before technical work.
9. Use Context7 before implementation, refactor, or review.
10. Keep this repository scoped to docs/governance only.
11. Keep sibling-governance ownership explicit: this repository owns shared governance memory, templates, prompts, rollout notes, and docs/governance surfaces only.
12. Do not treat this repository as the owner of product code, releases, repo-local `.specify/`, or repo-local `specs/` in other repositories.
13. Critical gate and routing behavior must live in `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`; `.github/skills/*/SKILL.md` and `.opencode/skills/*/SKILL.md` reinforce but do not replace those CLI-native enforcement surfaces.
14. Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).
15. Read `.github/copilot-commit-message-instructions.md` for commit creation or commit-message generation.

## Proof line format (mandatory)

Start the response with exactly:

- `Preflight OK: <file1>, <file2>, ...`

## Failure behavior (mandatory)

If preflight is incomplete, reply only:

- `BLOCKED: preflight incompleto`

Then include one single objective next action to unblock.

## Context7 documentation policy (mandatory)

- Use Context7 before implementation, refactor, and review work.

## MCP credential discovery and connection consent (mandatory)

- Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).
- Discovery must cover workspace/project files, OpenCode config, `.copilot/mcp-config.json`, VS Code `profiles/*/mcp.json`, `~/.gemini/antigravity/mcp_config.json`, and referenced environment variables such as `CONTEXT7_API_KEY`; treat GitHub Copilot CLI as a first-class runtime alongside OpenCode, Copilot VS Code, and Gemini/Antigravity.

## Tasks governance (mandatory)

- Read `tasks/todo.md` and `tasks/lessons.md` before technical work when `tasks/` exists; if `tasks/` is missing, create both files before technical work and preserve the canonical top blocks.
- Keep `tasks/todo.md` updated with objective, execution plan, expected evidence, and status/result; append dated lessons below the canonical template and never replace historical content with placeholders.

## Governance automation (mandatory)

- Secret scan: `./tools/governance/scan-secrets.ps1`; instruction sync: `python ./tools/governance/sync-instructions.py`; compliance audit: `python ./tools/governance/audit-compliance.py`; precedence audit: `python ./tools/governance/verify-precedence.py`

## Mandatory multi-agent orchestration skill

- For non-trivial docs/governance work, apply `orchestrate-multi-agents` before implementation and keep the `Template DAG 100% compliance`; owners/tasks may be reduced only when not applicable, but mandatory gates cannot be removed.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
