# Final Verified Actionable Fixes

**Status:** completed
**Created:** 2026-04-11
**Scope:** `meuagendamento-workspace`, governance sibling repos, `portfolio`, `helenSantosPortfolio`, and `preflight-prompt`

## Objective

Apply the final verified actionable fixes across the requested repositories without committing, covering path drift, governance instruction rewrites, stale Speckit discovery surfaces, tasks lesson normalization, preflight governance path updates, and Linux Sonar token bootstrap parity.

## Context & Constraints

- The request spans multiple owned repositories and governance siblings.
- Changes must be minimal, factual, and limited to the requested files/surfaces.
- No commits.
- Validation should be light but evidence-based where practical.

## Execution Steps

1. Read mandatory preflight/instruction files for each touched repository.
2. Update `meuagendamento-workspace` path, docs, and Sonar token scripts.
3. Rewrite governance-repo instruction files and remove stale local Speckit discovery entrypoints.
4. Normalize the undated lessons in `portfolio` and `helenSantosPortfolio` into canonical dated entries.
5. Update `preflight-prompt` governance scripts and add the missing local skill mirrors.
6. Run focused validation and summarize changed files plus validation evidence.

## Acceptance Criteria

- All requested files are updated or removed.
- Canonical workspace root names and script references point to live Linux paths.
- Governance repos no longer expose broken local Speckit Copilot entrypoints.
- The new Linux Sonar token setup script exists, is executable, and interoperates with the token store.
- Validation completes with no syntax or permission regressions in the touched automation.

## Decisions & Alternatives

- Chosen: copy missing local skill mirrors from the global fallback skills verbatim to preserve parity.
- Chosen: add the minimal setter directly to `sonar-token-store.sh` instead of introducing a second helper file.
- Rejected: broader audit/remediation outside the explicitly requested fixes.

## Execution Outcome

- Completed on 2026-04-12.
- Residual actionable drift from the targeted repositories was closed without commits, including Linux path/runtime normalization, governance-loop mirror cleanup, `python3` standardization, and final repo-local revalidation.
