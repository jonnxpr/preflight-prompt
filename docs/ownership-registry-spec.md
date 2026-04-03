# Ownership/Orchestration Registry — Schema Specification

> Registry files are advisory routing aids only. They do not override, extend,
> or replace any native instruction surface (AGENTS.md, CLAUDE.md, .github/*, skills).

## Purpose

An ownership registry answers three questions without ambiguity:
1. Who owns each instruction/governance surface in this ecosystem?
2. Which orchestration mode (S0-S4) is appropriate for each change type?
3. Which validate-fast/full command sequence applies to each repo?

## Where Files Live

| File                                                  | Purpose                        |
|-------------------------------------------------------|--------------------------------|
| `preflight-prompt/docs/ownership-registry-spec.md`    | This schema — canonical        |
| `<ecosystem>-governance/docs/ownership-registry.md`   | Per-ecosystem instance         |

**Never** in: a product repo, a workspace hub root, or any file agents load as an instruction surface.

## Schema

```yaml
# ownership-registry.md — Advisory only. Last updated: YYYY-MM-DD
ecosystem: <name>             # e.g., partner, meuagendamento, caradhras
hub_path: <path>              # e.g., projetos/ (may be non-git)
governance_repo: <path>       # e.g., partner-governance/

instruction_surfaces:
  - surface: <relative-file>  # e.g., .copilot/base-instructions.md
    owner: <who>              # hub | child-repo | governance-repo | preflight-prompt
    writable_by: [<mode>]     # S0|S1|S2|S3|S4 — which modes may write this surface
    notes: <string>           # optional

repos:
  - path: <relative-path>             # e.g., backend/
    name: <name>
    stack: <java-gradle|java-maven|angular|react|node|static>
    jdk: <11|21|25|null>              # null if not Java; must match jdk-env.ps1 output
    orchestration_default: <S0|S1|S2|S3|S4>
    validate_fast: <command>          # exact command — must exist on disk
    validate_full: <command>          # exact command — must exist on disk
    owner_file: <path>                # e.g., backend/AGENTS.md — agents must read before acting

change_type_routing:
  - type: <change-type>       # e.g., governance-surface|java-logic|frontend-ui|cross-repo-contract
    mode: <S0|S1|S2|S3|S4>
    notes: <string>
```

## Constraints

- `writable_by` for `preflight-prompt`-owned surfaces must contain only `S3`.
- `owner_file` must point to a file that exists; schema validator will error on missing paths.
- `validate_fast` and `validate_full` must reference commands that exist on disk.
- `jdk` must match the actual output of `scripts/jdk-env.ps1` for the repo — never inferred.
- A registry file that causes `audit-self.py --strict` to fail must not be merged.

## Reference Instance (Partner ecosystem excerpt)

```yaml
ecosystem: partner
hub_path: workspace/ambiente-partner/projetos
governance_repo: workspace/ambiente-partner/partner-governance

instruction_surfaces:
  - surface: .copilot/base-instructions.md
    owner: hub
    writable_by: [S0, S3]
  - surface: CLAUDE.md
    owner: hub
    writable_by: [S0, S3]
  - surface: .github/copilot-instructions.md
    owner: hub
    writable_by: [S0, S3]
  - surface: .github/instructions/*.instructions.md
    owner: hub
    writable_by: [S0, S3]
  - surface: .opencode/skills/development-standards/SKILL.md
    owner: hub
    writable_by: [S0, S3]

repos:
  - path: integrador/
    name: integrador
    stack: java-gradle
    jdk: 21
    orchestration_default: S0
    validate_fast: "../scripts/jdk-env.ps1 && ../scripts/gradlew-jdk.ps1 . checkstyleMain checkstyleTest --no-daemon --console plain"
    validate_full: "../scripts/jdk-env.ps1 && ../scripts/gradlew-jdk.ps1 . test --no-daemon --console plain"
    owner_file: integrador/AGENTS.md

  - path: backoffice/
    name: backoffice
    stack: react
    jdk: null
    orchestration_default: S0
    validate_fast: "npm run lint"
    validate_full: "npm run lint && npm test"
    owner_file: backoffice/AGENTS.md

change_type_routing:
  - type: governance-surface
    mode: S3
    notes: preflight-prompt is canonical writer; hub and governance repo are rollout targets
  - type: java-logic-single-repo
    mode: S0
  - type: java-logic-multi-repo
    mode: S2
    notes: repos are independent; full parallelism allowed
  - type: frontend-ui
    mode: S0
  - type: cross-repo-contract
    mode: S1
    notes: define contract first, then open backend + frontend lanes in parallel
```
