# Mirror Caveman Skills Into Per-Tool Folders

**Status:** completed
**Created:** 2026-04-20
**Scope:** global skill surfaces under `$HOME`: `~/.config/opencode/skills`, `~/.copilot/skills`, `~/.agent/skills`, using `~/.agents/skills` as the freshly installed Caveman source

## Objective

Espelhar as 6 skills Caveman instaladas em `~/.agents/skills` para as superficies globais por ferramenta (`~/.config/opencode/skills`, `~/.copilot/skills`, `~/.agent/skills`) para obter discoverability/paridade mais estrita com o estate atual, sem alterar o snippet always-on ja aplicado.

## Context & Constraints

- O usuario pediu explicitamente a etapa 2: mirror para os folders por ferramenta.
- A instalacao oficial via `npx skills add JuliusBrussee/caveman -y` ja ocorreu e deixou os assets em `~/.agents/skills`.
- O always-on ja esta garantido nas superficies nativas; esta etapa e de paridade/discoverability, nao de enforcement.
- Preferir o menor batch seguro: copiar somente as 6 skills Caveman.
- Nao commitar nem pushar.

## Execution Steps

1. Persistir este plano e registrar a rodada no `tasks/todo.md`.
2. Confirmar que `~/.agents/skills/{caveman,caveman-commit,caveman-compress,caveman-help,caveman-review,compress}` existem e sao a fonte desta rodada.
3. Copiar essas 6 skills para `~/.config/opencode/skills`, `~/.copilot/skills` e `~/.agent/skills` preservando os nomes de pasta.
4. Validar discoverability por tool folder e via `npx skills ls -g --json`.
5. Atualizar `tasks/todo.md` e este plano com as evidencias finais.

## Acceptance Criteria

- As 6 skills Caveman existem sob `~/.config/opencode/skills`, `~/.copilot/skills` e `~/.agent/skills`.
- Os `SKILL.md` mirrored preservam frontmatter e conteudo tecnico da fonte `~/.agents/skills`.
- A validacao final mostra discoverability nos folders por ferramenta sem quebrar os audits existentes.

## Decisions & Alternatives

- Fonte escolhida: `~/.agents/skills`, por ser o resultado direto da instalacao oficial desta maquina.
- Estrategia escolhida: copiar o conjunto Caveman inteiro em vez de links manuais ad hoc, para manter previsibilidade e leitura simples.
- Rejeitado: editar manualmente conteudo das skills mirrored nesta rodada; o objetivo e espelho fiel.

## Execution Outcome Append (2026-04-20)

- As 6 skills Caveman foram copiadas com sucesso de `~/.agents/skills` para `~/.config/opencode/skills`, `~/.copilot/skills` e `~/.agent/skills`.
- Evidencia direta por folder:
  - `~/.config/opencode/skills/{caveman,caveman-commit,caveman-compress,caveman-help,caveman-review,compress}/SKILL.md` encontrados.
  - `~/.copilot/skills/{caveman,caveman-commit,caveman-compress,caveman-help,caveman-review,compress}/SKILL.md` encontrados.
  - `~/.agent/skills/{caveman,caveman-commit,caveman-compress,caveman-help,caveman-review,compress}/SKILL.md` encontrados.
- Evidencia por `skills` CLI:
  - `npx skills ls -g -a opencode --json` passou a listar as 6 skills Caveman com `agents: ["OpenCode", "GitHub Copilot"]`.
  - `npx skills ls -g -a github-copilot --json` passou a listar as 6 skills Caveman com `agents: ["GitHub Copilot", "OpenCode"]`.
- O registry do `skills` CLI continua apontando `path` para `~/.agents/skills/*`, mas a discoverability por folder agora tambem esta materializada nos 3 targets per-tool.
