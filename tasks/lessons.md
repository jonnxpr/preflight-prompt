# Lessons

- Registre aqui regras novas, correcoes explicitas e aprendizados reutilizaveis.
- Consulte este arquivo antes de qualquer trabalho tecnico.
- Atualize continuamente quando surgir uma nova licao.

## 2026-03-28 - Precedencia local em nested repos precisa ser explicita

- Contexto: auditorias de precedence em nested repos continuavam falhando mesmo com heranca clara do workspace root.
- Correcao recebida: `AGENTS.md`, `GEMINI.md` e `.github/copilot-instructions.md` locais precisam mencionar `.copilot/base-instructions.md`, `CLAUDE.md` e `.github/copilot-instructions.md` em ordem.
- Regra preventiva: nao confiar apenas em frases genericas como "read the workspace root instruction files first" quando o toolkit valida precedencia por evidencia semantica ordenada.

## 2026-03-28 - OpenCode usa `.opencode/commands/` no plural

- Contexto: repositorios e hubs ainda podiam manter drift com `.opencode/command/`.
- Correcao recebida: slash commands e roteadores do OpenCode devem ficar em `.opencode/commands/`.
- Regra preventiva: validar a surface real de discovery do OpenCode antes de propagar templates upstream.

## 2026-03-28 - Speckit precisa respeitar ownership por repo

- Contexto: workspaces com hub nao-git e nested repos exigem limites claros para `.specify/` e `specs/`.
- Correcao recebida: hubs nao-git podem expor apenas comandos roteadores; `.specify/` e `specs/` pertencem ao repo dono. Quando o root e um git repo real, ele pode ter assets proprios sem contaminar nested repos.
- Regra preventiva: nunca deixar automacao Speckit escrever fora do repo dono nem misturar assets globais e locais.

## 2026-03-28 - Artefatos gerados de governanca costumam ser evidencia, nao fonte de verdade

- Contexto: varios repos filhos estavam versionando relatorios gerados como `tasks/compliance-report.md`, `tasks/precedence-report.md`, `tasks/workspace-baseline-report.md` e `tasks/secret-scan.sarif`.
- Correcao recebida: quando esses arquivos forem apenas evidencia gerada, devem entrar no `.gitignore` e sair do index sem apagar a copia local.
- Regra preventiva: decidir explicitamente quais relatorios sao canonicos e quais sao outputs gerados para evitar drift entre repos.

## 2026-03-28 - Child repo discovery precisa ser worktree-safe

- Contexto: um worktree paralelo pode aparecer com `.git` arquivo e ser confundido com child repo comum durante rollout automatizado.
- Correcao recebida: diferenciar `.git` diretorio de `.git` arquivo e nao aplicar rollout amplo em worktrees por engano.
- Regra preventiva: em scans de child repos, tratar worktrees como caso especial e exigir alvo explicito quando necessario.

## 2026-03-28 - Politica de branch deve ser descoberta antes de commit/push

- Contexto: rollouts de governanca em repos diferentes usam branches operacionais distintos (`feature/*`, `homologation`, `main`).
- Correcao recebida: antes de commitar/pushar, confirmar branch atual, upstream e politica do repo dono.
- Regra preventiva: nunca assumir `main` por padrao em workspaces multi-repo.

## 2026-03-28 - Auditoria global deve incluir baseline de workspace quando existir

- Contexto: compliance e precedence nao cobrem sozinhos alguns contratos globais de hubs multi-repo.
- Correcao recebida: quando existir `audit-workspace-baseline.py` ou equivalente, ele deve rodar junto do toolkit principal e entrar no veredito final.
- Regra preventiva: em pedidos globais de governanca, consolidar evidencia de compliance, precedence e baseline por alvo.
