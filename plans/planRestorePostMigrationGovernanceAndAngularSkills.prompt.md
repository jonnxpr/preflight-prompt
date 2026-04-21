# Restore Post Migration Governance And Angular Skills

**Status:** abandoned
**Created:** 2026-04-12
**Scope:** `~/.config/opencode`, `~/.copilot`, `~/.agent`, `/media/jonathan/Dados/angular-skills/skills`, e todas as superficies repo-locais de instructions/skills/governance sob `/media/jonathan/Dados/Documentos`

## Objective

Restaurar todas as superficies de instructions, skills e governance que ficaram incompletas, desalinhadas ou degradadas pela migracao de `Documentos` para `/media/jonathan/Dados`, usando como referencias a historia Git dos owners e a arvore canonica de Angular skills em `/media/jonathan/Dados/angular-skills/skills`.

## Context & Constraints

- O usuario quer a arquitetura novamente consistente e completa em todas as ferramentas e workspaces.
- As Angular skills devem ser sincronizadas a partir de `/media/jonathan/Dados/angular-skills/skills`, incluindo o conteudo interno de cada skill.
- Superficies live fora de Git (`~/.config/opencode`, `~/.copilot`, `~/.agent`) tambem precisam ficar consistentes.
- A raiz canonica continua sendo `/media/jonathan/Dados/Documentos`; `/home/jonathan/Documentos` deve permanecer vazio.
- O escopo inclui restaurar conteudos incompletos e corrigir drift de permissoes/modos em arquivos de instructions/skills/governance quando necessario.
- Nenhum conteudo deve ser perdido; recuperacoes devem se apoiar em historia Git, referencias canonicas ou mirrors equivalentes.

## Execution Steps

1. Inventariar todas as superficies Angular e de governance/instructions/skills relevantes nas areas globais e repo-locais.
2. Localizar drift remanescente da migracao, incluindo referencias antigas de path, arquivos faltantes/incompletos e permissoes indevidas.
3. Sincronizar todas as Angular skills a partir da arvore canonica em `/media/jonathan/Dados/angular-skills/skills` para os destinos globais e repo-locais aplicaveis.
4. Restaurar e corrigir as demais superficies de instructions/skills/governance usando a historia Git dos owners e os mirrors canonicos adequados.
5. Rodar auditorias e verificacoes finais nos owners afetados e garantir worktrees limpos.
6. Commitar e pushar as mudancas em todos os repositorios afetados.

## Acceptance Criteria

- Todas as Angular skills globais e repo-locais aplicaveis refletem exatamente a referencia em `/media/jonathan/Dados/angular-skills/skills`.
- Superficies live de instructions/skills/governance nao ficam com drift remanescente da migracao em caminhos, conteudos ou permissoes indevidas.
- Auditorias relevantes dos owners afetados encerram sem findings acionaveis.
- Todos os repositorios alterados ficam com `working tree clean`, `main` sincronizada com `origin/main`.
- `/home/jonathan/Documentos` permanece vazio e toda a arquitetura ativa permanece sob `/media/jonathan/Dados`.

## Decisions & Alternatives

- Owner da memoria: `preflight-prompt`, por ser o repositorio de governanca cross-workspace ja usado na migracao anterior.
- Fonte canonica Angular: arvore completa de `/media/jonathan/Dados/angular-skills/skills`, nao apenas arquivos `SKILL.md` isolados.
- Restauracoes de governance/instructions fora da arvore Angular devem priorizar o owner Git da superficie e nao improvisar conteudo novo sem referencia verificavel.

## Execution Outcome Append (2026-04-13)

- A causa raiz final dos findings `missing_final_gate` estava na propria fonte canonica Angular (`/media/jonathan/Dados/angular-skills/skills`), nao nos espelhos repo-locais.
- O repositorio `angular-skills` foi confirmado como owner da fonte de verdade e recebeu a menor correcao segura: adicao do bloco `## Mandatory final code review, cross-validation, and factual integrity` nas 10 `angular-*/SKILL.md`.
- Depois disso, os espelhos Angular foram resincronizados para os owners repo-locais de `meuagendamento-workspace` e `frontend`, e tambem para os espelhos globais locais em `~/.config/opencode`, `~/.copilot` e `~/.agent`.
- Evidencias fechadas desta etapa:
  - `meuagendamento-workspace`: `python3 tools/governance/audit-compliance.py` = `100`
  - `meuagendamento-workspace`: `python3 tools/governance/verify-precedence.py` = `0`
  - `frontend`: `python3 tools/governance/audit-compliance.py` = `100`
  - `frontend`: `python3 tools/governance/verify-precedence.py` = `0`
- O criterio de aceitacao relativo a auditorias verdes e alinhamento Angular foi atingido.
- O criterio de commit/push continua pendente apenas porque esta sessao ainda nao recebeu solicitacao explicita para commitar.

## Closure Note Append (2026-04-21)

- O plano foi encerrado como `abandoned` para remover falso estado `in_progress`.
- A restauracao tecnica e a validacao objetiva foram concluídas; o unico passo remanescente era commit/push repo-owned, que nao podia ser executado sem solicitacao explicita do usuario.
- Rodadas globais posteriores de governance audit loop consolidaram essas correcoes, portanto nao restou finding tecnico acionavel ligado a esta etapa.
