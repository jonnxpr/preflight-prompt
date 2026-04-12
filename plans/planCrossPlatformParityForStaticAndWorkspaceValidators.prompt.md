# Cross-Platform Parity For Static And Workspace Validators

**Status:** completed
**Created:** 2026-04-12
**Scope:** `meuagendamento-workspace`, `portfolio`, and `helenSantosPortfolio`

## Objective

Close the practical Windows/Linux parity gaps identified in validator entrypoints and static-site local startup flows, using the smallest safe cross-repo change set.

## Context & Constraints

- Governance audits are already green; this plan targets real execution surfaces instead of documentation-only parity.
- `meuagendamento-workspace` has PowerShell validators that currently assume fixed Python command names.
- `portfolio` and `helenSantosPortfolio` have `validate.ps1` but no matching Linux `validate.sh` wrapper.
- `portfolio` and `helenSantosPortfolio` currently depend on `python -m http.server` for `npm start`; this is not reliably cross-platform.
- Keep changes minimal, do not add unnecessary dependencies, and do not commit unless explicitly requested.

## Execution Steps

1. Add a PowerShell Python launcher resolver to the affected validator scripts and route Python invocations through it.
2. Add repo-local `scripts/validate.sh` wrappers for `portfolio` and `helenSantosPortfolio` matching the existing `validate.ps1` behavior.
3. Replace Python-based local static serving in both static sites with a small built-in Node server script.
4. Update package manifests and user-facing README command references that depend on the local server entrypoint.
5. Run validation/build checks and review the diffs for regressions.

## Acceptance Criteria

- PowerShell validation entrypoints work with `py -3`, `python3`, or `python` without hardcoded Windows/Linux assumptions.
- `portfolio` and `helenSantosPortfolio` expose both `validate.ps1` and `validate.sh` with equivalent fast/full behavior.
- `npm start` in both static sites no longer requires Python.
- Local verification passes for the updated wrappers and static-site builds.

## Decisions & Alternatives

- Chosen: use a small built-in Node HTTP server instead of adding a new npm dependency.
- Chosen: keep Python in governance scripts where already required, but make PowerShell resolution launcher-agnostic.
- Rejected: docs-only parity, because the current issue is in real execution surfaces.

## Execution Outcome

- Completed on 2026-04-12.
- `meuagendamento-workspace` now resolves Python launchers in `scripts/validate.ps1` and `scripts/smoke-workspace.ps1`, and `pwsh -NoProfile -File scripts/smoke-workspace.ps1` completed successfully.
- `portfolio` and `helenSantosPortfolio` now expose both `scripts/validate.ps1` and `scripts/validate.sh`, and both PowerShell and bash fast validators passed.
- Both static sites now use `scripts/start-static.mjs` for `npm start`, removing the local Python dependency while preserving the same localhost workflow.
- Final evidence also includes successful `npm run build` in both static sites and server smoke checks returning `200` for `/` and `404` for a missing asset path.
