# Lessons Learned

Registre aqui licoes apos correcoes explicitas do usuario para evitar repeticao de erros.

- Data:
- Contexto:
- Correcao recebida:
- Regra preventiva:
- Como validar na proxima vez:

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

## 2026-03-29 - Repositorio irmao de governanca e o padrao mais limpo

- Contexto: workspaces com varios repos ou hubs neutros precisam versionar memoria de governanca sem transformar a raiz operacional em repo de governanca.
- Correcao recebida: preferir um repositorio irmao dedicado (por exemplo `partner-governance/`, `meuagendamento-governance/`) em vez de converter a raiz operacional.
- Regra preventiva: manter ownership explicito - o repo irmao guarda prompts, templates, notas de rollout e memoria de governanca; codigo de produto, assets repo-locais e Speckit repo-local continuam no repo principal ou nos nested repos.

## 2026-03-29 - Repositorio principal precisa apontar para o repositorio irmao de governanca

- Contexto: criar apenas o repositorio irmao nao fecha a arquitetura se o workspace principal continuar sem referencia clara ao novo ownership.
- Correcao recebida: apos criar o repositorio irmao, atualizar `README.md`, `PRE-FLIGHT.md`, `CLAUDE.md`, `AGENTS.md` e `.github/copilot-instructions.md` do workspace principal para apontar para ele.
- Regra preventiva: tratar a referencia ao repositorio irmao como parte obrigatoria do rollout, nao como documentacao opcional de pos-migracao.

## 2026-03-29 - Hub operacional nao-git precisa de espelho versionado no repositorio irmao

- Contexto: no workspace Partner, o hub operacional `projetos/` nao e git, mas sua superficie de governanca precisa historico auditavel.
- Correcao recebida: versionar essa superficie dentro do repositorio irmao de governanca em um caminho de espelho claro, como `mirrors/projetos-hub/`.
- Regra preventiva: quando um hub operacional nao-git receber mudancas em docs/instrucoes/skills/comandos/ferramentas de governanca, sincronizar o espelho versionado no repositorio irmao na mesma rodada.

## 2026-03-29 - Espelho versionado de hub nao-git precisa de script e modo check

- Contexto: sem automacao, o espelho versionado pode ficar desatualizado mesmo com a arquitetura correta.
- Correcao recebida: criar script dedicado de sincronizacao com modo de verificacao (`--check` ou equivalente) para detectar drift sem modificar arquivos.
- Regra preventiva: toda estrategia de espelho versionado para hub nao-git deve nascer com comando de sync e comando de check documentados.

## 2026-03-29 - Wrapper PowerShell ajuda em workspaces Windows-first

- Contexto: mesmo com script principal em Python, a execucao do dia a dia pode ficar melhor com comando nativo do ambiente.
- Correcao recebida: expor um `.ps1` enxuto com acoes `sync` e `check` para o espelho versionado do hub nao-git.
- Regra preventiva: quando o workspace for claramente Windows-first, complementar o script principal com wrapper PowerShell simples e documentado.

## 2026-03-29 - Hook local fecha a melhor garantia pratica do espelho

- Contexto: mesmo com sync/check manuais, ainda existe risco de commit no repo de governanca com espelho desatualizado.
- Correcao recebida: instalar hook local de pre-commit no repo irmao de governanca para executar o check do espelho antes de cada commit.
- Regra preventiva: em estrategia de espelho versionado para hub nao-git, considerar hook local como parte do toolkit padrao quando o objetivo for reduzir drift ao maximo.
