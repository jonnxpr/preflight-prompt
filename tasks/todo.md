# Task Plan

Registre aqui as tarefas nao triviais em execucao neste repositorio ou workspace.

- Objetivo:
- Plano de execucao:
- Evidencias esperadas:
- Status/Resultado:

## Phase 0 — Orchestration Productivity Planning Package (2026-04-02)

- Objetivo: Deliver 5-piece orchestration documentation package to `docs/` as canonical advisory layer over existing multi-workspace architecture. Thin orchestration layer only — never overrides native instruction surfaces.
- Plano de execucao:
  1. Write `docs/orchestration-matrix.md` (Piece 1 — operational matrix with S0-S4 modes)
  2. Write `docs/ownership-registry-spec.md` (Piece 2 — registry schema with reference instance)
  3. Write `docs/validate-catalog.md` (Piece 3 — validate-fast/full commands per ecosystem)
  4. Write `docs/orchestration-templates.md` (Piece 4 — S0-S4 templates with DAG compliance)
  5. Write `docs/implementation-roadmap.md` (Piece 5 — phased rollout plan)
  6. Append additive reference block to `CLAUDE.md`
  7. Update `tasks/todo.md` (this file)
  8. Run validation gates (`verify-precedence.py` + `audit-compliance.py`)
  9. Review `git diff` to confirm only additive changes
- Evidencias esperadas: All 5 docs exist in `docs/`, `CLAUDE.md` has reference block, governance audits pass with no regression, git diff shows only additions.
- Status/Resultado:
  - [x] Piece 1: `docs/orchestration-matrix.md` — DONE
  - [x] Piece 2: `docs/ownership-registry-spec.md` — DONE (with `--console plain` fix)
  - [x] Piece 3: `docs/validate-catalog.md` — DONE (corrected v2 with 7 ecosystem fixes)
  - [x] Piece 4: `docs/orchestration-templates.md` — DONE (corrected v2 with DAG compliance)
  - [x] Piece 5: `docs/implementation-roadmap.md` — DONE
  - [x] `CLAUDE.md` reference block — DONE
  - [x] `tasks/todo.md` update — DONE
  - [x] Validation gates — DONE (score 100/100, 0 precedence findings)
  - [x] Git diff review — DONE

## Phase 1 — Per-hub validate.ps1 wrappers (2026-04-02)

- Objetivo: Create `validate.ps1` wrapper scripts for all 5 ecosystems. One command replaces catalog lookup per task.
- Plano de execucao:
  1. Explore existing scripts/tools in all 5 ecosystems
  2. Write `projetos/scripts/validate.ps1` (Partner hub — governance + 14 Java repos + backoffice)
  3. Write `meuagendamento/scripts/validate.ps1` (root governance + backend/frontend/landingPage)
  4. Write `caradhras-poc/scripts/validate.ps1` (root governance + backend/frontend)
  5. Write `Portfolio/scripts/validate.ps1` (governance + metadata sync + build)
  6. Write `HelenSantosPortfolio/scripts/validate.ps1` (same pattern as Portfolio)
  7. Smoke-test all `validate.ps1 -Mode fast` across all 5 ecosystems
  8. Update `tasks/todo.md` (this file)
- Evidencias esperadas: All 5 scripts exist, parse clean, and `validate.ps1 -Mode fast` exits 0 in each ecosystem.
- Status/Resultado:
  - [x] Ecosystem exploration — DONE (all scripts/tools/params mapped)
  - [x] Partner hub `validate.ps1` — DONE (hub governance + 14 Java checkstyle + backoffice lint)
  - [x] MeuAgendamento `validate.ps1` — DONE (root governance + smoke-workspace + backend mvn + frontend lint)
  - [x] Caradhras `validate.ps1` — DONE (root governance + backend mvn validate)
  - [x] Portfolio `validate.ps1` — DONE (verify-precedence + verify-metadata-sync)
  - [x] HelenSantosPortfolio `validate.ps1` — DONE (same pattern as Portfolio)
  - [x] Smoke-test fast mode — ALL 5 PASSED (Partner: 14 Java + backoffice + hub governance)
  - [x] `tasks/todo.md` update — DONE

## 2026-04-03 — Consolidar aprendizados no PRE-FLIGHT-PROMPT

- Objetivo: Atualizar `PRE-FLIGHT-PROMPT.md` com os aprendizados aplicados durante o rollout completo das 5 fases, as 2 rodadas de review e as correções finais em 10 repositorios.
- Plano de execucao:
  1. Ler o contexto obrigatorio do repositorio (`README.md`, instrucoes raiz, regras locais e `tasks/`)
  2. Comparar o prompt atual com os aprendizados efetivamente aplicados no rollout
  3. Adicionar regras novas e criterios de aceite para cobrir ownership, verificacao de superficie real, classificacao de validate-fast/full, robustez PowerShell, mirror discipline e completude de orquestracao
  4. Validar com `audit-compliance.py` e `verify-precedence.py`
- Evidencias esperadas: `PRE-FLIGHT-PROMPT.md` atualizado com regras consolidadas, `audit-compliance.py = 100`, `verify-precedence.py = 0`.
- Status/Resultado:
  - [x] Preflight local completo — DONE
 - [x] Prompt consolidado com aprendizados do rollout e das reviews — DONE
 - [x] `python tools/governance/audit-compliance.py` — 100
 - [x] `python tools/governance/verify-precedence.py` — 0

## 2026-04-10 — Consolidar aprendizados de replicacao de ambiente no PRE-FLIGHT-PROMPT

- Objetivo: Atualizar `PRE-FLIGHT-PROMPT.md` para incorporar os aprendizados do pacote `D:\arquiteturaLinux`, incluindo replicacao dinamica de ambiente, credenciais portaveis, historico sanitizado, fluxo GUI/CLI, idempotencia forte, verificacao final consolidada e loop autonomo de revisao/correcao.
- Plano de execucao:
  1. Ler integralmente o prompt e as instrucoes obrigatorias do repositorio
  2. Inserir regras novas para replicacao de ambiente e operacao zero-interacao
  3. Atualizar plano de execucao e criterios de aceite do prompt
  4. Validar com `audit-compliance.py` e `verify-precedence.py`
- Evidencias esperadas: `PRE-FLIGHT-PROMPT.md` atualizado, audits locais verdes, novas regras cobrindo a arquitetura dinamica e operacional aprendida com `D:\arquiteturaLinux`.
- Status/Resultado:
  - [x] Preflight completo — DONE
  - [x] Prompt atualizado — DONE
  - [x] `python tools/governance/audit-compliance.py` — 100
  - [x] `python tools/governance/verify-precedence.py` — 0
