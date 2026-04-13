---
name: orchestrate-multi-agents
description: Global fallback orchestration skill for complex multi-agent execution with planning, dependency control, and auditable delivery.
license: Complete terms in LICENSE.txt
---

# Skill - orchestrate-multi-agents (global fallback)

Use this skill when the task has two or more of these signals:

- multi-discipline scope
- parallelizable work
- broad refactor or migration risk
- auditability or traceability requirements
- non-trivial constraints around security, performance, or compatibility

## Mandatory flow

1. Define the final objective, constraints, and acceptance criteria.
2. Build an execution plan with tasks, owners, dependencies, and validation steps.
3. If the plan meets the persistence threshold (S1+ or 3+ steps), save it to `plans/plan-${camelCaseName}.prompt.md` in the owning repo before execution begins. Reference the plan file in `tasks/todo.md`.
4. Run independent work in parallel only when required inputs are ready.
5. Consolidate outputs, update the decision log, and verify the Definition of Done.
6. Report risks, leftovers, and next steps clearly.

## Required outputs

- Execution Plan
- `[REDACTED]`
- Definition of Done results
- Decision Log
- Final consolidation with evidence

## When not required

- For trivial single-step work, explicitly state why orchestration is unnecessary.

## Mandatory final code review, cross-validation, and factual integrity

- Complex work is complete only after final review and evidence-based validation across the consolidated result.
