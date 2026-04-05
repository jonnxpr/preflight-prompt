# Mandatory Rules Enforcement Sweep

**Status:** completed
**Created:** 2026-04-03
**Scope:** Cross-repo (preflight-prompt owns orchestration; touches all 10 repos)

## Objective

Audit ~60 mandatory rules across all instruction surfaces, identify gaps where rules are declared but not enforced or inconsistently propagated, then implement a 9-item remediation sweep (R1, R3-R10) ensuring every mandatory rule is consistently declared across all instruction surfaces and has the strongest feasible enforcement mechanism.

## Context & Constraints

- The audit covered 7 workspaces, 5 governance repos, 4 product repos, and 18 global skills.
- R2 was removed after discovering all 3 meuagendamento subproject AGENTS.md files already existed and were more mature than the template.
- R3 was re-scoped: verify-precedence.py already existed in 4/5 repos; only partner-governance was missing it.
- `~/.config/opencode/` is NOT git-tracked — R1 changes are local filesystem only.
- meuagendamento `.github/workflows/` is gitignored — R8 workflow exists on disk but cannot be committed.
- 3 divergent audit-compliance.py versions (531-697 lines each) required independent expansion for R9.
- Partner hub (`projetos/`) is non-git; hub-wide plans go in partner-governance.
- All changes must be compatible with Copilot VS Code, Copilot CLI, Antigravity, and OpenCode.

### 8 Non-Negotiable Guardrails

1. `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` remain native enforcement surfaces.
2. Skills remain reinforcement only, not sole rule source.
3. `scripts/discover-git-repo.ps1` remains base for owner resolution.
4. Repo owner wins over workspace hub.
5. `*-governance` repos remain versioned memory, not product code owners.
6. `preflight-prompt` remains canonical reusable governance source, not operational owner.
7. `validate-fast/full` must be repo-local, using real wrappers.
8. "Writer unico" (S3 canonical writer) only applies to explicitly shared surfaces.

## Execution Steps

### R1 — Global Principles in `~/.config/opencode/AGENTS.md` (completed)

Added 3 new principles at lines 97-99:
- Factual integrity (never invent facts/APIs/versions)
- Context7 and official docs (prefer when available)
- Dual-gate closure (code review + cross-validation as separate mandatory gates)

### R4 — Missing Instruction Files (completed)

- Created `caradhras-poc/.github/instructions/context7.instructions.md` (15 lines)
- Created `HelenSantosPortfolio/.github/instructions/speckit.instructions.md` (17 lines)

### R6 — Tasks-Governance Formatting Normalization (completed)

Normalized 8 files across 4 governance repos to identical 6-bullet format using meuagendamento's stronger wording ("exact canonical top blocks required by `PRE-FLIGHT.md`"):
- 4x `.copilot/base-instructions.md`
- 4x `.agent/rules/development-standards.md`

### R5 — preflight.instructions.md Expansion (completed)

Normalized all 4 `preflight.instructions.md` files to the expanded 6-bullet format:
- meuagendamento-governance: expanded 3 dense bullets to 6
- Other 3 governance repos: inserted 6 bullets (were missing this section)

### R3 — verify-precedence.py Propagation (completed)

- Created `verify-precedence.py` (108 lines) + `precedence-matrix.md` (21 lines) in partner-governance
- Registered precedence audit in 4 AGENTS.md files (partner-governance, meuagendamento, Portfolio, HelenSantosPortfolio)

### R7 — Commit-Message Hook (completed)

- Created `scripts/commit-msg` (Python, 95 lines) with Conventional Commits + PT-BR validation
- Created `scripts/install-commit-msg-hook.ps1` (PowerShell, 95 lines) covering 13 repos

### R8 — Preflight Enforcement CI Workflow (completed)

- Created `preflight-enforcement.yml` in meuagendamento (gitignored — cannot be committed) and caradhras-poc
- Verbatim copy of Portfolio's existing 23-line workflow

### R9 — audit-compliance.py Skill Routing Expansion (completed)

- Expanded `check_skill_routing` from 1-3 skills to 18/18 in all 3 audit-compliance.py files
- Each version uses workspace-aware expected skill lists

### R10 — Cross-Repo Mandatory Rules Orchestrator (completed)

- Created `validate-mandatory-rules.py` (215 lines) in preflight-prompt
- Orchestrates local audit scripts across repos with `--strict` mode

## Acceptance Criteria

- [x] All 9 R-items implemented (R1, R3-R10)
- [x] All 10 repos committed locally
- [x] `audit-compliance.py` passes in meuagendamento, caradhras-poc, preflight-prompt
- [x] `audit-self.py --strict` passes in partner-governance
- [x] `validate-mandatory-rules.py --skip-local-audits` passes from preflight-prompt (0 findings)
- [x] All 10 repos pushed to remote
- [x] Partner-governance mirror sync verified (if applicable)

## Decisions & Alternatives

| # | Decision | Choice | Alternative Considered |
|---|----------|--------|----------------------|
| D1 | R2 scope | **REMOVED** — subproject AGENTS.md files already exist | Create from template (would overwrite mature files) |
| D2 | R3 scope | **Only partner-governance** + register in 4 AGENTS.md | Create in all 5 repos (4 already had it) |
| D3 | R6 wording | **Meuagendamento wording** with explicit PRE-FLIGHT.md ref + 6 bullets | Weaker "preserve canonical blocks" wording from other 3 |
| D4 | R1 Context7 | **"Prefer when available"** | Hard mandate (would block when MCP is down) |
| D5 | R9 approach | **Expand independently** with workspace-awareness | Unify to single version (would lose workspace specifics) |
| D6 | R10 scope | **Cross-repo orchestrator** of local audit scripts | Monolithic validator replacing local scripts |
| D7 | R4 variant | **Meuagendamento variant** for caradhras-poc; **Portfolio variant** for HelenSantosPortfolio | Identical template for both (would miss workspace context) |
