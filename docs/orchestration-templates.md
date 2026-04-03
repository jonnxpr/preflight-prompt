# S0-S4 Orchestration Templates

> For use with the `orchestrate-multi-agents` skill.
> All templates comply with the 5-step mandatory flow from `orchestrate-multi-agents`:
>   1. Define objective, constraints, acceptance criteria
>   2. Build execution plan with tasks, owners, dependencies, validation steps
>   3. Run independent work in parallel only when inputs are ready
>   4. Consolidate outputs, update decision log, verify Definition of Done
>   5. Report risks, leftovers, next steps
>
> Owners/tasks may be reduced only when not applicable.
> Mandatory gates (preflight, owner resolution, validate, decision log, DoD, risks) cannot be removed.

---

## Lane Return Format (Standard — required for all modes)

Every lane agent must close its work with this structured block:

```
LANE RESULT: <lane-name>
  repo:          <path>
  status:        PASS | FAIL | SKIP
  validate_fast: PASS | FAIL | SKIPPED
  validate_full: PASS | FAIL | SKIPPED | NOT_APPLICABLE
  files_changed: [<list or "none">]
  evidence:      <1–3 sentences — what was done and what was verified>
  blockers:      <none | description>
```

---

## S0 — Single Lane

**Use when**: 1 agent, ≤2 steps, known single target, or open contract.

```
WAIVER (optional — for tasks with ≤1 step)
  If the task is trivially achievable without orchestration, the
  orchestrator may bypass this template by stating the reason.
  Example: "Orchestration waiver: single-file typo fix, no dependencies,
  no cross-repo impact."
  When a waiver is declared, only validate-fast is required after completion.

---

OBJECTIVE
  task:         <string>
  constraints:  <string — e.g., "minimal change, no new dependencies">
  done_when:    <acceptance criteria — 1–3 bullet points>

INPUTS
  target_repo:  <path>

GATE
  [ ] target repo owner resolved (scripts/discover-git-repo.ps1)
  [ ] preflight read for target_repo (AGENTS.md + .github/copilot-instructions.md at minimum)
  [ ] validate-fast command known (from validate-catalog.md)

LANE: implementer
  agent:   general
  context: [target_repo/AGENTS.md, target_repo/.github/copilot-instructions.md, development-standards]
  tasks:
    1. implement change
    2. run validate-fast
    3. return LANE RESULT

CONSOLIDATE
  [ ] validate-fast passed
  [ ] no unintended files touched outside target_repo
  [ ] LANE RESULT received
  [ ] Decision Log: record key decisions and rationale (may be brief for S0)
  [ ] Definition of Done: verify all acceptance criteria from OBJECTIVE met
  [ ] Risks/Leftovers/Next Steps: document any remaining items or "none"
  [ ] Template DAG 100% compliance confirmed
```

---

## S1 — Dual Lane

**Use when**: backend + frontend change in the same feature, or any 2 parallel repos sharing a contract.

**Subfolder-lane variant** (e.g., Caradhras): when both lanes live inside the same git
repository as subfolders (not nested git repos), `repo_a` and `repo_b` are subfolder
paths within the single repo. Owner resolution applies once at the repo root, and a
single commit may close both lanes.

```
OBJECTIVE
  task:         <string>
  constraints:  <string>
  done_when:    <acceptance criteria — 1–3 bullet points>

INPUTS
  contract:     <API spec or shared interface — must be defined before lanes open>
  repo_a:       <path>   # e.g., backend/ (may be a subfolder in the same repo)
  repo_b:       <path>   # e.g., frontend/ (may be a subfolder in the same repo)

GATE
  [ ] contract defined and agreed before any lane opens (contract-first)
  [ ] owner resolved for both repos
  [ ] preflight read for both repos
  [ ] validate-fast commands known for both repos

LANES (open in parallel after gate closes)
  lane-A: implementer-A
    context: [repo_a owner files, development-standards, contract]
    tasks:
      1. implement against contract
      2. validate-fast repo_a
      3. return LANE RESULT

  lane-B: implementer-B
    context: [repo_b owner files, development-standards, contract]
    tasks:
      1. implement against contract
      2. validate-fast repo_b
      3. return LANE RESULT

CONSOLIDATE
  [ ] validate-fast passed in both lanes
  [ ] contract honored by both sides (integration check)
  [ ] no cross-repo side effects introduced
  [ ] Decision Log: record key decisions, contract choices, and tradeoffs
  [ ] Definition of Done: verify all acceptance criteria from OBJECTIVE met
  [ ] Risks/Leftovers/Next Steps: document integration risks, pending E2E, or "none"
  [ ] Template DAG 100% compliance confirmed
```

---

## S2 — Repo Fan-Out

**Use when**: same type of change across 3–N independent repos
(e.g., governance propagation, dependency bump, Checkstyle config sync, instruction drift fix).

```
OBJECTIVE
  task:         <string>
  constraints:  <string>
  done_when:    <acceptance criteria — 1–3 bullet points>

INPUTS
  change_type:  <governance | dependency | config | refactor>
  repos:        [<path_1>, <path_2>, ..., <path_N>]

GATE
  [ ] orchestrator confirms change is truly independent across all repos
      (no shared state, no ordering dependency between repos)
  [ ] owner resolved for each repo
  [ ] preflight read per repo (may be done inside each lane)
  [ ] validate-fast commands known per repo

LANES (all parallel — no dependency between lanes)
  lane-1 .. lane-N: implementer-per-repo
    context: [repo_N owner files, development-standards]
    tasks:
      1. apply change to repo_N
      2. validate-fast repo_N
      3. return LANE RESULT

CONSOLIDATE (orchestrator)
  [ ] collect LANE RESULT from all lanes
  [ ] confirm no lane introduced cross-repo state
  [ ] produce summary: per-repo status + evidence table
  [ ] Decision Log: record choices made across repos, any repo-specific deviations
  [ ] Definition of Done: verify all acceptance criteria from OBJECTIVE met
  [ ] Risks/Leftovers/Next Steps: list any repos that failed or were skipped
  [ ] Template DAG 100% compliance confirmed
```

---

## S3 — Canonical Rollout

**Use when**: change to a shared governance surface (e.g., preflight-prompt update, global skill change),
followed by propagation to N ecosystems.

```
OBJECTIVE
  task:         <string>
  constraints:  <string — must include: "canonical source writes first, rollout is downstream only">
  done_when:    <acceptance criteria — 1–3 bullet points>

INPUTS
  canonical_change:  <description>
  canonical_source:  <repo>         # always preflight-prompt for global changes
  rollout_targets:   [<ecosystem-1>, ..., <ecosystem-N>]

GATE
  [ ] canonical writer identified (preflight-prompt, or owning governance repo)
  [ ] rollout scope agreed — which ecosystems are in scope
  [ ] NOT parallel — writer lane must close before any rollout lane opens
  [ ] validate-fast commands known for canonical source and all rollout targets

LANE-0: canonical-writer (sequential — must close before fan-out)
  agent:   general
  context: [canonical_source/AGENTS.md, development-standards]
  tasks:
    1. implement canonical change
    2. validate-fast canonical_source
    3. produce rollout artifact (diff, sync manifest delta, or instruction summary)
    4. return LANE RESULT

LANES-1..N: rollout-per-ecosystem (parallel, only after LANE-0 closes)
  agent:   general
  context: [ecosystem_N/AGENTS.md, development-standards, rollout artifact from LANE-0]
  tasks:
    1. apply rollout artifact to ecosystem_N
    2. validate-fast ecosystem_N
    3. confirm no local overrides were lost or silently replaced
    4. return LANE RESULT

CONSOLIDATE
  [ ] validate-fast passed in canonical source and each ecosystem
  [ ] drift check: no ecosystem diverged from canonical intent
  [ ] sync-instructions.py run where applicable (if manifest-driven sync is configured)
  [ ] Decision Log: record canonical-vs-local decisions, any ecosystem-specific adaptations
  [ ] Definition of Done: verify all acceptance criteria from OBJECTIVE met
  [ ] Risks/Leftovers/Next Steps: list ecosystems needing manual follow-up or "none"
  [ ] Template DAG 100% compliance confirmed
```

---

## S4 — Full Delivery DAG

**Use when**: new feature with spec, security implications, QA gate, and release notes.

```
OBJECTIVE
  task:         <string>
  constraints:  <string — must include security and QA scope>
  done_when:    <acceptance criteria — 3–5 bullet points including security + QA>

INPUTS
  feature_spec:     <path to specs/<feature-branch>/>
  repos:            [<list>]
  security_scope:   <description>
  qa_scope:         <description>

GATE
  [ ] feature_spec approved and located at specs/<feature-branch>/
  [ ] architect lane must complete before any impl lane opens
  [ ] security and QA scope defined before impl lanes close
  [ ] validate-fast and validate-full commands known for all repos

LANE-0: architect (sequential — must close before impl lanes open)
  tasks:
    1. review spec
    2. produce ADR (architecture decision record)
    3. define contracts between repos
    4. sign off: impl lanes may open

LANES-1..N: implementers (parallel — open after LANE-0 closes)
  context: [repo owner files, development-standards, contracts from LANE-0]
  tasks:
    1. implement
    2. validate-fast
    3. return LANE RESULT

LANE-SEC: security (parallel with QA — opens after all impl lanes close)
  tasks:
    1. scan-secrets.ps1
    2. static analysis (if configured)
    3. return LANE RESULT

LANE-QA: qa (parallel with security — opens after all impl lanes close)
  tasks:
    1. validate-full all repos
    2. integration check
    3. return LANE RESULT

LANE-DOCS: docs/release (after security + QA close)
  tasks:
    1. update changelog
    2. update release notes
    3. tag if applicable
    4. return LANE RESULT

CONSOLIDATE
  [ ] validate-full passed for all repos
  [ ] security lane: no findings
  [ ] QA lane: all tests green
  [ ] release notes ready
  [ ] no spec drift between implementation and original spec
  [ ] Decision Log: record architecture decisions, contract choices, security findings, QA deviations
  [ ] Definition of Done: verify all acceptance criteria from OBJECTIVE met
  [ ] Risks/Leftovers/Next Steps: production rollout plan, monitoring, or "none"
  [ ] Template DAG 100% compliance confirmed
```
