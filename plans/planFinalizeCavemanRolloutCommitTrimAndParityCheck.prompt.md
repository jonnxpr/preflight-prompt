# Finalize Caveman Rollout Commit Trim And Parity Check

**Status:** active
**Created:** 2026-04-20
**Scope:** `preflight-prompt`, managed git owners under `/media/jonathan/Dados1/Documentos`, and selected global skill folders under `$HOME`

## Objective

Fechar a rodada Caveman com tres acoes solicitadas pelo usuario: confirmar a paridade final apos restart, remover apenas duplicacoes legacy de Caveman que sejam claramente redundantes e criar commits nos repositorios donos das mudancas repo-owned.

## Context & Constraints

- O usuario pediu explicitamente: commit das mudancas repo-owned, parity check adicional e trim de superficies legacy duplicadas.
- Superficies globais sob `$HOME` nao pertencem a um git repo; mudancas nelas permanecem locais.
- A duplicacao Caveman relevante desta rodada esta entre `~/.agents/skills` e mirrors per-tool em `~/.config/opencode/skills`, `~/.copilot/skills`, `~/.agent/skills`.
- O pedido de trim deve ser conservador: remover apenas o que for claramente redundante e sem quebrar a discoverability recentemente validada.
- Nao tocar em mudancas alheias do usuario.

## Execution Steps

1. Persistir este plano e registrar a rodada final em `tasks/todo.md`.
2. Resolver ownership Git dos repositorios afetados e inspecionar status/diff/log para preparar commits seguros.
3. Determinar a superficie legacy duplicada que pode ser removida sem perder a discoverability validada; aplicar o menor trim seguro.
4. Revalidar parity/discoverability apos o trim.
5. Criar commits por repo dono usando mensagens Conventional Commits em pt-BR.
6. Atualizar `tasks/todo.md` e este plano com evidencias finais e limites locais/globais.

## Acceptance Criteria

- Parity check final continua verde apos o trim.
- Apenas superficies legacy Caveman claramente redundantes sao removidas.
- Cada repo dono recebe commit separado e coerente com seu escopo.
- Nenhuma mudanca fora de repo e commitada.

## Decisions & Alternatives

- Owner da memoria desta rodada: `preflight-prompt`.
- Estrategia de commit: um commit no repo `preflight-prompt` e commits separados nos demais repositorios apenas se houver mudancas repo-owned neles.
- Estrategia de trim: remover primeiro apenas o alias redundante `compress`, preservando `caveman-compress` como canonical, e abortar qualquer trim maior se isso degradar a discoverability observada.

## Execution Outcome Append (2026-04-20)

- Ownership Git resolvido para 7 repositorios afetados: `preflight-prompt`, `meuagendamento-workspace`, `portfolio`, `helenSantosPortfolio`, `meuagendamento-governance`, `portfolio-governance`, `helen-santos-portfolio-governance`.
- Trim conservador aplicado com sucesso: alias redundante `compress` removido de `~/.agents/skills`, `~/.config/opencode/skills`, `~/.copilot/skills` e `~/.agent/skills`.
- Revalidacao apos trim permaneceu verde:
  - `caveman`, `caveman-commit`, `caveman-compress`, `caveman-help` e `caveman-review` continuam presentes nos folders por ferramenta.
  - `compress` deixou de existir nos 4 targets globais.
  - `npx skills ls -g -a opencode --json` e `npx skills ls -g -a github-copilot --json` continuam listando as 5 skills Caveman canonical com metadata de agent.
