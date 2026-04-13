---
name: development-standards
description: Governance-repo standards for CLI-native parity, preflight, Context7, MCP consent, and docs-only ownership.
---

# Development Standards

## Scope

- Docs/governance only.
- No product code ownership.
- Preserve explicit sibling-governance boundaries for shared prompts, templates, rollout notes, and governance memory.

## Canonical precedence

1. `.copilot/base-instructions.md`
2. `CLAUDE.md`
3. `.github/copilot-instructions.md`
4. `.github/instructions/*.instructions.md`
5. `.github/skills/development-standards/SKILL.md`
6. `.opencode/skills/development-standards/SKILL.md`
7. `.agent/rules/development-standards.md`

## CLI-native parity

- Critical gate and routing behavior must live in `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`.
- `.github/skills/*/SKILL.md` and `.opencode/skills/*/SKILL.md` reinforce the contract; they are not the sole enforcement layer for Copilot CLI or OpenCode.
- OpenCode command discovery uses `.opencode/commands/`.

## Tasks governance

- Read `tasks/todo.md` and `tasks/lessons.md` before technical work when `tasks/` exists.
- If `tasks/` is missing, create both files before technical work and preserve the canonical top blocks.
- `tasks/lessons.md` must preserve the exact canonical top block.
- New lessons must be appended as dated entries below the template.
- Historical lessons must never be replaced by placeholders.
- `tasks/todo.md` must track the current non-trivial work with objective, execution plan, expected evidence, and status/result.

## Context7 documentation policy (mandatory)

- Use Context7 before implementation, refactor, and review decisions.

## MCP credential discovery and connection consent (mandatory)

- Before connecting to any MCP server, request user confirmation and list the credential source(s) to be used (redacted; never print secret values).
- Discovery must cover workspace/project files, OpenCode config, `.copilot/mcp-config.json`, VS Code `profiles/*/mcp.json`, `~/.gemini/antigravity/mcp_config.json`, and referenced environment variables such as `CONTEXT7_API_KEY`.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.
