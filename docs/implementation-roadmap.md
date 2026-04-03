# Implementation Roadmap — Orchestration Productivity Package

> ROI order. Each phase is independently deployable.
> No phase may violate the 8 non-negotiable guardrails from orchestration-matrix.md.
> Guardrails are enforced at consolidation of each phase — not just stated.

---

## Phase 0 — Write the 5 canonical docs (Highest ROI, Minimal Risk)

**ROI**: Immediately usable — agents can load these docs as context from day 1.
**Risk**: Minimal — additive new files only. No existing surface touched except one line in CLAUDE.md.
**Effort**: 1 session (S0, target: preflight-prompt).
**Mode**: S0.

**Deliverables**:
- `preflight-prompt/docs/orchestration-matrix.md`
- `preflight-prompt/docs/ownership-registry-spec.md`
- `preflight-prompt/docs/validate-catalog.md`
- `preflight-prompt/docs/orchestration-templates.md`
- `preflight-prompt/docs/implementation-roadmap.md`
- `preflight-prompt/CLAUDE.md`: one additive reference block at the bottom pointing to `docs/`.

**Guardrails**:
- All 5 files go into `preflight-prompt/docs/` only.
- The `CLAUDE.md` change is strictly additive — no existing rule may be modified or removed.
- `docs/` must not be created in any product repo or workspace hub.

**Evidence**:
- 5 files present under `preflight-prompt/docs/`.
- `audit-compliance.py = 100` and `verify-precedence.py = 0` in preflight-prompt after write.
- `git diff` shows only additive changes.

---

## Phase 1 — Per-hub validate.ps1 wrappers (High ROI, Low Risk)

**ROI**: Agents call one command instead of looking up the catalog per task.
**Risk**: Low — new scripts only, no changes to existing ones.
**Effort**: 2 sessions (Partner hub first, then remaining ecosystems as S2).
**Mode**: S0 for Partner hub; S2 for the remaining 4 ecosystems.

**Deliverables** (priority order):
1. `projetos/scripts/validate.ps1` — fast and full targets, delegates to all governance tools and Java wrappers.
2. `meuagendamento/scripts/validate.ps1` — coordinates root governance tools + nested repo calls.
3. `caradhras-poc/scripts/validate.ps1` — root governance + backend/frontend delegates.
4. `Portfolio/scripts/validate.ps1` — governance tools + `verify-metadata-sync.mjs` + build.
5. `HelenSantosPortfolio/scripts/validate.ps1` — same pattern as Portfolio.

**Script contract** (all scripts):
- Accept `-Mode fast | full` parameter.
- Exit non-zero on any failure; print the failing command.
- Use only workspace-relative paths and existing wrappers.
- Must be non-destructive (read-only validators).

**Guardrails**:
- No hardcoded absolute paths.
- No new logic — orchestration of existing commands only.
- `audit-workspace-baseline.py` must be updated for Partner hub if it checks for expected scripts.

**Evidence**:
- `./scripts/validate.ps1 -Mode fast` exits 0 in each ecosystem.
- `./scripts/validate.ps1 -Mode full` exits 0 in each ecosystem.
- No regression in existing audit baselines.

---

## Phase 2 — Per-ecosystem ownership registry instances (Medium ROI, Medium Risk)

**ROI**: Agents resolve ownership and routing without parsing instruction files.
**Risk**: Medium — new files in governance repos; sync manifests must be updated.
**Effort**: 2–3 sessions (Partner first, then remaining 4 as S2).
**Mode**: S0 for Partner governance; S2 for MeuAgendamento, Caradhras, Portfolio, Helen.

**Deliverables** (priority order):
1. `partner-governance/docs/ownership-registry.md`
2. `meuagendamento-governance/docs/ownership-registry.md`
3. `caradhras-poc-governance/docs/ownership-registry.md`
4. `portfolio-governance/docs/ownership-registry.md`
5. `helen-santos-portfolio-governance/docs/ownership-registry.md`

For each:
- Follow the schema from `preflight-prompt/docs/ownership-registry-spec.md`.
- Update `tools/governance/instruction-sync-manifest.json` to include the new `docs/` file.
- Update `audit-self.py --strict` to validate registry presence and required fields.

**Guardrails**:
- Registry files carry `Advisory only` header — no new rules introduced.
- `writable_by` must not claim S3 authority for surfaces owned by child repos.
- Must not create `docs/` inside any product repo (`backoffice/`, `frontend/`, etc.).
- `audit-self.py --strict = 0` in each governance repo after change.

**Evidence**:
- `docs/ownership-registry.md` present in each governance repo.
- `audit-self.py --strict = 0` per governance repo.
- `verify-precedence.py = 0` in each ecosystem after sync.

---

## Phase 3 — Reference docs from ecosystem CLAUDE.md surfaces (Low Risk, Medium ROI)

**ROI**: Reduces agent prompt overhead — no full doc search needed to find templates.
**Risk**: Low — one additive block per CLAUDE.md.
**Effort**: 0.5 session (S3 mode; preflight-prompt writes first, ecosystems propagate).
**Mode**: S3.

**Deliverable** — additive block appended to each ecosystem's `CLAUDE.md`:

```
## Orchestration Reference

- Operational matrix, modes, and parallelization rules:
  see preflight-prompt/docs/orchestration-matrix.md
- Orchestration templates (S0-S4):
  see preflight-prompt/docs/orchestration-templates.md
- validate-fast/full commands for this ecosystem:
  see preflight-prompt/docs/validate-catalog.md
- Ownership registry for this ecosystem:
  see <ecosystem>-governance/docs/ownership-registry.md (after Phase 2)
```

**Guardrails**:
- Additive block at bottom only — no existing rule modified or removed.
- Must not change hard preflight gate, mandatory load order, or skill routing.
- `verify-precedence.py = 0` after each update.

**Evidence**:
- Block present at bottom of each `CLAUDE.md`.
- `verify-precedence.py = 0` and `audit-compliance.py = 100` per ecosystem.

---

## Phase 4 — Integrate registry validation into audit-workspace-baseline (Long-term, Low Risk)

**ROI**: Drift detection becomes automatic — no manual registry audits needed.
**Risk**: Low — audit-only, no production code impact.
**Effort**: 1 session (S0, target: Partner hub + preflight-prompt).
**Mode**: S0 (Partner hub) + S3 (propagate to preflight-prompt audit-compliance.py).

**Deliverables**:
- `tools/governance/audit-workspace-baseline.py` (Partner hub): add check for `docs/ownership-registry.md` presence in each `*-governance` sibling.
- `audit-self.py --strict` (each governance repo): validate registry schema — required fields present, no missing commands, no orphaned repo entries.
- `preflight-prompt/tools/governance/audit-compliance.py`: port registry presence check so it covers all ecosystems globally.

**Guardrails**:
- Audit scripts must be read-only — no file modification.
- Audit failures are non-blocking warnings until all ecosystems have completed Phase 2.
- Must not break existing `audit-workspace-baseline.py --strict = 0` outcome.

**Evidence**:
- `audit-workspace-baseline.py --strict = 0` with registry checks enabled (or warnings-only mode confirmed).
- Deliberately introducing a missing field in a test registry causes the schema validator to report it.

---

## Summary

| Phase | What                            | Where                        | Risk    | ROI       | Sessions |
|-------|---------------------------------|------------------------------|---------|-----------|----------|
| 0     | Write 5 canonical docs          | preflight-prompt/docs/       | Minimal | Very High | 1        |
| 1     | validate.ps1 per hub            | `<hub>/scripts/`             | Low     | High      | 2        |
| 2     | Ownership registry instances    | `*-governance/docs/`         | Medium  | Medium    | 2–3      |
| 3     | Reference block in CLAUDE.md    | Each ecosystem CLAUDE.md     | Low     | Medium    | 0.5      |
| 4     | Audit registry in baseline      | tools/governance/            | Low     | Long-term | 1        |

**Recommended next action**: Phase 1 — validate.ps1 per hub. Highest immediate value after the docs are in place.
