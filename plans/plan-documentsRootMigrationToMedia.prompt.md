# Documents Root Migration To Media

**Status:** completed
**Created:** 2026-04-12
**Scope:** `/home/jonathan/Documentos`, `/media/jonathan/Dados/Documentos`, `~/.config/opencode`, `~/.copilot`, `~/.agent`, `~/.config/user-dirs.dirs`, e superfícies fonte de verdade nos 7 repositorios/workspaces migrados`

## Objective

Migrar a raiz canonica dos repositorios/workspaces de `Documentos` para `/media/jonathan/Dados/Documentos`, mantendo compatibilidade por symlink em `/home/jonathan/Documentos`, sem perder governanca, roteamento, preflight, trusted folders nem operabilidade dos caminhos existentes.

## Context & Constraints

- O usuario confirmou `/media/jonathan/Dados/Documentos` como raiz canonica final.
- A compatibilidade com o caminho legado deve permanecer via symlink em `/home/jonathan/Documentos`.
- A raiz antiga contem apenas 7 diretorios de trabalho, o que favorece um unico symlink raiz apos o move.
- `preflight-prompt` atua como repo dono da memoria desta migracao cross-repo; historicos append-only (`plans/**`, `tasks/lessons.md`, relatorios gerados) nao devem ser reescritos apenas para normalizar paths antigos.
- Mudancas fora de repos Git (`~/.config/opencode`, `~/.copilot`, `~/.agent`, VS Code user config) sao locais e nao commitaveis.
- Nenhuma conexao MCP deve ser aberta sem consentimento explicito do usuario.

## Execution Steps

1. Persistir este plano e registrar a execucao atual em `tasks/todo.md`.
2. Validar novamente a origem e o destino para confirmar que o cutover por symlink raiz unico continua seguro.
3. Mover os 7 diretorios de `/home/jonathan/Documentos/` para `/media/jonathan/Dados/Documentos/` e substituir a raiz antiga por um unico symlink para a nova raiz canonica.
4. Atualizar `~/.config/user-dirs.dirs` e as superfícies globais live (`~/.config/opencode`, `~/.copilot`, `~/.agent`) que ainda apontam para o caminho antigo.
5. Atualizar apenas as superfícies repo-locais fonte de verdade que ainda referenciam `/home/jonathan/Documentos`, preservando historico append-only e artefatos de evidencia.
6. Reexecutar verificacoes/auditorias aplicaveis nos owners alterados e confirmar acesso funcional pelos caminhos canonico e legado.
7. Registrar evidencias finais em `tasks/todo.md`, marcar o plano como concluido e deixar claro o que permaneceu como historico preservado.

## Acceptance Criteria

- `/media/jonathan/Dados/Documentos` contem os 7 diretorios migrados.
- `/home/jonathan/Documentos` e um symlink funcional para `/media/jonathan/Dados/Documentos`.
- Os 7 repositorios/workspaces permanecem acessiveis por ambos os caminhos.
- `~/.config/user-dirs.dirs` e as superfícies globais fonte de verdade relevantes apontam para a nova raiz canonica.
- Os arquivos repo-locais fonte de verdade afetados usam `/media/jonathan/Dados/Documentos` como path canonico quando necessario, mantendo o caminho antigo apenas como compatibilidade/historico.
- As verificacoes finais nao deixam findings acionaveis de governanca ou path drift nas superfícies alteradas.

## Decisions & Alternatives

- Escolhido: mover os 7 diretorios e substituir a raiz antiga inteira por um unico symlink.
- Motivo: a raiz antiga contem apenas os 7 workspaces/repositorios e nao possui outros itens que justifiquem symlinks por projeto.
- Rejeitado: manter `/home/jonathan/Documentos` como diretorio real com um symlink por repo, por ser mais verboso, mais sujeito a drift e menos fiel ao path canonico unico.

## Outcome

- Cutover concluido em 2026-04-12: os 7 diretorios foram movidos para `/media/jonathan/Dados/Documentos` e `/home/jonathan/Documentos` passou a ser um symlink unico de compatibilidade.
- Superfícies globais live atualizadas: `~/.config/user-dirs.dirs`, `~/.config/opencode/**`, `~/.copilot/config.json`, `~/.copilot/skills/**` e `~/.agent/**` relevantes para roteamento/path canonico.
- Superfícies repo-locais fonte de verdade atualizadas nos owners afetados; historicos append-only e evidencias antigas permaneceram preservados por decisao explicita.
- Evidencias finais: `preflight-prompt` compliance = `100`, precedence = `0`, e os tres repositorios irmaos de governanca passaram no `audit-self.py --strict`.
