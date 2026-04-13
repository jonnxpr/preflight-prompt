# Orchestration Matrix — Operational Reference

> Thin orchestration layer over existing native instruction surfaces.
> This document is advisory. All hard rules live in AGENTS.md, CLAUDE.md,
> .github/copilot-instructions.md, and .github/instructions/*.instructions.md.

## Mode Selection

| Mode | Label           | When to Use                                                              | Max Parallelism          |
|------|-----------------|--------------------------------------------------------------------------|--------------------------|
| S0   | Single Lane     | 1 agent, ≤2 steps, known single target, or open contract                 | 1                        |
| S1   | Dual Lane       | Backend + frontend change in same feature, or any 2 parallel repos      | 2                        |
| S2   | Repo Fan-Out    | Same type of change across 3–N independent repos                        | N (no order dependency)  |
| S3   | Canonical Rollout | Change to a shared governance surface, then propagate to N ecosystems  | 1 writer → N rollout     |
| S4   | Full Delivery DAG | New feature with spec, security, QA, and docs                         | architect → impl → sec+qa → docs |

## Mode Selection by Ecosystem

| Ecosystem                                     | Default Mode | Rationale                                                      |
|-----------------------------------------------|--------------|----------------------------------------------------------------|
| Partner hub (projetos/)                        | S0 / S3      | Hub is non-git; tasks are either hub-only or governance propagation |
| Partner child repos (≥3 repos, same change)   | S2           | Repos are independent; max parallelism                          |
| Partner child repos (1–2 repos)               | S0 / S1      | No overhead needed                                              |
| MeuAgendamento root                            | S0 / S3      | Root is governance; nested repos are independent                |
| MeuAgendamento backend + frontend             | S1           | Dual-lane, coordinated but parallel                             |
| Caradhras backend + frontend                  | S1           | Single repo with subfolder lanes (not nested git repos)         |
| Portfolio / HelenSantosPortfolio              | S0           | Single repo, single concern                                     |
| preflight-prompt                              | S3 (writer)  | Always canonical writer; downstream ecosystems are rollout lanes |
| Cross-ecosystem governance change             | S3           | preflight-prompt writes first, then ecosystems propagate        |

## Parallelization Rules

1. **Parallel lanes only when no shared state exists between them.** Two Java repos with independent codebases: parallel. Backend + frontend sharing a contract change: S1 with contract-first gate.
2. **S3 is always sequential: writer first, then fan-out.** Never write canonical and rollout in parallel.
3. **S4 architect lane must close before impl lanes open.** Security and QA lanes may run in parallel after implementation closes.
4. **validate-fast before closing any lane.** validate-full only at S4 consolidation or when explicitly required.
5. **Owner wins.** If a lane's repo has a local AGENTS.md, the lane agent must read it before acting — even if the orchestrator has already read the hub instructions.

## Sequencing Rules

```
S0: [gate] → [impl] → [validate-fast] → done
S1: [gate-both] → [lane-A ∥ lane-B] → [validate-fast-both] → [integration-check] → done
S2: [gate-each] → [lane-1 ∥ lane-2 ∥ … ∥ lane-N] → [validate-fast-each] → [summary] → done
S3: [canonical-gate] → [writer] → [validate-fast-canonical] → [rollout-1 ∥ … ∥ rollout-N] → [drift-check] → done
S4: [spec-gate] → [architect] → [impl-lanes] → [security ∥ qa] → [docs] → [validate-full] → done
```

## Non-Negotiable Guardrails

1. AGENTS.md, CLAUDE.md, .github/copilot-instructions.md, and .github/instructions/*.instructions.md are never overridden by orchestration mode selection.
2. Skills are reinforcement only — not a sole rule source.
3. `scripts/discover-git-repo.ps1` is the base for owner resolution in every lane.
4. Repo owner always wins over workspace hub.
5. `*-governance` repos are versioned memory, not product code owners.
6. `preflight-prompt` is the canonical reusable governance source, not an operational owner.
7. `validate-fast/full` must use repo-local wrappers only — no cross-repo command calls.
8. S3 "canonical writer" applies only to explicitly shared governance surfaces — never invades a child repo's own ownership.
