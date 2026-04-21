---
name: governance-audit-loop
description: Global fallback governance skill for auditing and hardening instructions, skills, preflight gates, routing, CLI-native parity, and hub mirrors until zero actionable findings remain.
license: Complete terms in LICENSE.txt
---

# Skill - governance-audit-loop

## When to use

- Governance architecture audits
- Instruction, skill, preflight, or routing remediation
- CLI-native parity checks across OpenCode, GitHub Copilot VS Code, GitHub Copilot CLI, and Antigravity
- Hub or mirror consistency fixes

## Autonomous audit loop

Revise tudo que foi feito, garanta que não haja falhas, problemas, brechas ou pontas soltas. Caso encontre problemas corrija. Faça este loop de verificar e corrigir de forma 100% autônoma. A condição de parada para o loop encerrar é restarem zero actionable findings.

Only stop to request user input when there is destructive or irreversible risk, a real source-of-truth conflict, material ambiguity, an unavoidable external dependency block, or `--dry-run`.

## Scope

- `*/workspace/ambiente-partner/projetos` when present
- `*/workspace/ambiente-partner/partner-governance` when present
- `/media/jonathan/Dados2/Documentos/meuagendamento-workspace`
- `/media/jonathan/Dados2/Documentos/meuagendamento-workspace/backend`
- `/media/jonathan/Dados2/Documentos/meuagendamento-workspace/frontend`
- `/media/jonathan/Dados2/Documentos/meuagendamento-workspace/landingPage`
- `/media/jonathan/Dados2/Documentos/meuagendamento-governance`
- `*/caradhras-poc` when present
- `/media/jonathan/Dados2/Documentos/portfolio`
- `/media/jonathan/Dados2/Documentos/portfolio-governance`
- `/media/jonathan/Dados2/Documentos/helenSantosPortfolio`
- `/media/jonathan/Dados2/Documentos/helen-santos-portfolio-governance`
- `/media/jonathan/Dados2/Documentos/preflight-prompt`
- `~/.config/opencode/`
- `~/.copilot/`
- `~/.agent/`

## Mandatory execution model

1. Run Phase 0 deep qualitative inspection first.
2. Run Phase 1 governance scripts where available.
3. Apply fixes autonomously in the smallest safe batch by owner.
4. Re-run inspection and scripts.
5. Repeat until zero actionable findings remain.

## Mandatory final code review, cross-validation, and factual integrity

- Finish only after final code review plus evidence-based cross-validation.
- Validate correctness, readability, compatibility, and governance-surface consistency before marking work complete.
