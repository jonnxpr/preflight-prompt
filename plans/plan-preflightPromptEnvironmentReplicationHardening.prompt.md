# PRE-FLIGHT-PROMPT Environment Replication Hardening

**Status:** completed
**Created:** 2026-04-10
**Scope:** `PRE-FLIGHT-PROMPT.md`

## Objective

Update the reusable preflight prompt so it captures the end-to-end lessons learned from building `D:\arquiteturaLinux`: dynamic environment replication, zero-interaction automation, portable credentials, history sanitization, GUI orchestration, idempotency, conservative status reporting, and final consolidated verification.

## Context & Constraints

- Keep the prompt dynamic-by-default and avoid machine-specific hardcodes.
- Preserve the existing preflight/governance contract and expand it rather than rewriting the whole prompt.
- Ensure the prompt remains reusable across repositories, not tied only to the current machine.
- Reflect the autonomous verify/fix loop now used in governance surfaces.

## Execution Steps

1. Extend `Expected outcome` with environment-replication guarantees.
2. Add explicit non-negotiable rules for dynamic replication, portable credentials, sanitized history, zero-interaction automation, GUI orchestration, strict idempotency, final verification, conservative status reporting, and autonomous verify/fix loops.
3. Add a replication applicability check to the execution plan.
4. Add implementation guidance for environment replication packages.
5. Extend acceptance criteria with environment-replication success conditions.
6. Run repo-local governance audits to confirm no contract drift.

## Acceptance Criteria

- `PRE-FLIGHT-PROMPT.md` explicitly covers environment replication as a first-class scenario.
- The prompt requires dynamic path/user discovery instead of hardcoded machine assumptions.
- The prompt distinguishes required vs optional credentials/integrations.
- The prompt requires idempotent CLI/GUI operational flows and final consolidated verification.
- The prompt encodes the autonomous review/fix loop semantics.

## Decisions & Alternatives

- Chosen: additive updates in the existing prompt structure.
- Rejected: rewriting the prompt from scratch, which would risk losing proven governance content.
