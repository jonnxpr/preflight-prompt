# Install Caveman v1.6.0 Always On Across All Tools

**Status:** completed
**Created:** 2026-04-20
**Scope:** `preflight-prompt`, managed repositories under `/media/jonathan/Dados1/Documentos`, and active global tool surfaces under `$HOME` (`~/.config/opencode`, `~/.copilot`, `~/.agent`, `~/.gemini/antigravity`)

## Objective

Instalar e alinhar Caveman v1.6.0 nas superficies ativas de skills, instructions e governance, com o snippet always-on oficial ativo desde a primeira mensagem em OpenCode, GitHub Copilot e Gemini/Antigravity, preservando a arquitetura atual e evitando drift entre owners.

## Context & Constraints

- O usuario forneceu o snippet always-on oficial e ele deve ser usado verbatim.
- As decisoes precisam seguir somente fontes oficiais, com suporte de Context7 e README/release do projeto Caveman.
- A raiz operacional correta desta rodada e `/media/jonathan/Dados1/Documentos`; referencias anteriores a `/media/jonathan/Dados/Documentos` sao historicas/legadas.
- `PRE-FLIGHT.md` nao basta sozinho como enforcement; o modo always-on precisa viver nas superficies nativas de rules/system prompt.
- A arquitetura atual ja usa fallbacks globais em `~/.config/opencode`, `~/.copilot` e `~/.agent`; o rollout deve preferir o menor batch seguro compativel com esse modelo.
- Nao commitar nem pushar sem solicitacao explicita do usuario.

## Execution Steps

1. Persistir este plano e registrar o objetivo atual em `tasks/todo.md` e a correcao de raiz em `tasks/lessons.md`.
2. Inventariar os owners ativos, suas superficies nativas de instructions e as superficies globais reais usadas por OpenCode, Copilot e Gemini/Antigravity.
3. Buscar os artefatos oficiais de Caveman v1.6.0 necessarios para a arquitetura local e definir o conjunto minimo correto de sincronizacao.
4. Instalar/sincronizar a familia Caveman nas superficies globais de skills e executar os comandos oficiais de instalacao quando o runtime local suportar sem efeitos colaterais indevidos.
5. Aplicar o snippet always-on oficial nas superficies nativas globais e repo-locais que governam OpenCode, Copilot e Gemini/Antigravity.
6. Validar descoberta, roteamento e governanca; repetir o loop de verificacao/correcao ate restarem zero gaps acionaveis relacionados ao rollout Caveman.
7. Atualizar `tasks/todo.md` e este plano com as evidencias finais e quaisquer observacoes residuais nao acionaveis.

## Acceptance Criteria

- Os assets ou installs oficiais de Caveman v1.6.0 estao presentes nas superficies globais ativas relevantes.
- O snippet always-on oficial aparece verbatim nas superficies nativas que governam OpenCode, Copilot e Gemini/Antigravity nos owners gerenciados.
- Nenhuma referencia de instruction/routing fica quebrada apos o rollout.
- A validacao final comprova descoberta/instalacao das skills e presenca do enforcement always-on nas superficies corretas.
- Nenhum commit/push e realizado.

## Decisions & Alternatives

- Owner escolhido: `preflight-prompt`, porque o escopo e cross-workspace e a memoria/orquestracao compartilhada ja vive neste repositorio.
- Estrategia escolhida: combinar instalacao/sincronizacao oficial das skills com o snippet always-on nas superficies nativas, porque a documentacao oficial indica que o skill sozinho nao garante auto-start.
- Estrategia minima preferida: sincronizar primeiro as superficies globais e as instructions repo-locais nativas; so replicar mirrors locais adicionais de skills se a validacao mostrar necessidade real.
- Rejeitado: depender apenas de `npx skills add` ou apenas do snippet sem assets oficiais da skill, porque isso deixaria parte do objetivo (skill + always-on) incompleto.

## Execution Outcome Append (2026-04-20)

- O snippet always-on oficial do usuario foi aplicado verbatim nas superficies nativas globais: `~/.config/opencode/AGENTS.md`, `~/.copilot/base-instructions.md`, `~/.agent/rules/development-standards.md` e `~/.gemini/antigravity/GEMINI.md`.
- O mesmo snippet foi aplicado nas superficies repo-locais de maior precedencia dos 7 owners ativos sob `/media/jonathan/Dados1/Documentos`: `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.copilot/base-instructions.md` e `.agent/rules/development-standards.md` quando presentes.
- A instalacao oficial foi executada com `npx skills add JuliusBrussee/caveman -y`.
- O `skills` CLI instalou 6 skills globais em `~/.agents/skills/`: `caveman`, `caveman-commit`, `caveman-compress`, `caveman-help`, `caveman-review` e `compress`.
- Evidencia de discoverability pelo proprio CLI: `npx skills ls -g --json` passou a listar as 6 skills Caveman como globais.
- Evidencia de enforcement always-on: `grep "Caveman Always-On (mandatory)"` encontrou o bloco nas 4 superficies globais nativas e em 35 superficies repo-locais dos owners ativos.
- Evidencia de governanca repo-local:
  - `preflight-prompt`: `audit-compliance.py=100`, `verify-precedence.py=0`
  - `meuagendamento-workspace`: `audit-compliance.py=100`, `verify-precedence.py=0`, `audit-workspace-baseline.py=OK`
  - `portfolio`: `audit-compliance.py=100`, `verify-precedence.py=0`, `audit-workspace-baseline.py=OK`
  - `helenSantosPortfolio`: `audit-compliance.py=100`, `verify-precedence.py=0`, `audit-workspace-baseline.py=OK`
  - `meuagendamento-governance`: `audit-self.py --strict=OK`
  - `portfolio-governance`: `audit-self.py --strict=OK`
  - `helen-santos-portfolio-governance`: `audit-self.py --strict=OK`
- Drift ativo corrigido nos arquivos tocados: referencias ao root operacional atualizadas para `/media/jonathan/Dados1/Documentos` nas superficies ativas editadas.
- Residuo nao acionavel desta rodada: algumas skills globais ainda preservam referencias historicas do Partner/caradhras em `/media/jonathan/Dados/Documentos/...`; esses owners nao existem na raiz `Dados1` atual e nao foram alterados para evitar reescrever rotas de um estate nao presente sem evidencia local.
