# Cross Workspace Governance Audit Loop With Git Version Truth

**Status:** completed
**Created:** 2026-04-13
**Scope:** `preflight-prompt`, `meuagendamento-workspace`, `meuagendamento-governance`, `portfolio`, `portfolio-governance`, `helenSantosPortfolio`, `helen-santos-portfolio-governance`, nested repos/toolkits that expose governance scripts, and active global tool surfaces under `$HOME`

## Objective

Executar uma rodada global e autonoma de governance audit loop, usando como referencia as versoes e superficies corretas presentes nos repositorios Git donos de cada area, e corrigir todo drift acionavel ate restarem zero actionable findings em workspaces, projetos e ferramentas suportados.

## Context & Constraints

- O usuario quer uma verificacao/correcao completa, nao apenas uma auditoria pontual.
- As versoes e contratos corretos devem vir dos manifests e arquivos versionados reais dos repos donos (`package.json`, `pom.xml`, wrappers, skills, instructions, scripts), nunca de suposicoes.
- A raiz canonica de documentos continua em `/media/jonathan/Dados/Documentos`; `/home/jonathan/Documentos` permanece apenas como compatibilidade.
- Superficies globais locais em `~/.config/opencode`, `~/.copilot` e `~/.agent` tambem entram no escopo quando forem parte da arquitetura ativa.
- Nao commitar nem pushar sem solicitacao explicita do usuario.
- Para hubs nao-git do Partner, se houver edicao de arquivos de hub, sincronizar o mirror versionado e validar com `--check`.

## Execution Steps

1. Inventariar todos os owners com toolkit de governanca e seus manifests/version sources reais.
2. Executar auditorias iniciais (`audit-compliance.py`, `verify-precedence.py`, `audit-workspace-baseline.py`, `audit-self.py`, `validate-mandatory-rules.py --strict`) onde existirem.
3. Consolidar findings por owner e por categoria, separando drift real de eventuais falsos negativos de auditoria.
4. Aplicar correcoes minimas por owner usando como fonte de verdade o proprio repo Git dono da superficie e seus manifests/versionamentos reais.
5. Reexecutar auditorias e repetir o loop ate zerar actionable findings.
6. Atualizar `tasks/todo.md`, plano e evidencias finais por workspace/projeto/ferramenta.

## Acceptance Criteria

- Todos os owners ativos com toolkit de governanca foram inventariados e auditados.
- Toda correcao aplicada referencia manifests/versoes/superficies reais versionadas nos repos donos.
- Auditorias relevantes encerram verdes ou restam apenas gaps explicitamente nao acionaveis/documentados.
- Ferramentas e skills globais ativas ficam coerentes com os repositorios/workspaces que dependem delas.
- O resultado final consolidado reporta zero actionable findings.

## Decisions & Alternatives

- Owner escolhido: `preflight-prompt`, por continuar sendo a memoria e orquestracao cross-workspace.
- Estrategia escolhida: auditar primeiro, corrigir por owner em batches minimos, reauditar ate convergir.
- Rejeitado: corrigir em massa sem validar o repo dono e o manifesto/version source real de cada superficie.

## Execution Outcome Append (2026-04-14)

- Owners revalidados e encerrados verdes: `preflight-prompt`, `meuagendamento-workspace`, `backend`, `frontend`, `landingPage` e `portfolio`.
- Drift final remanescente foi reduzido a quatro batches minimos:
  1. `meuagendamento-workspace` skill mirrors raiz ainda hardcodavam Spring Boot `4.0.3`; agora deferem a versao para `backend/pom.xml` (atual `4.0.5`).
  2. `meuagendamento-workspace/scripts/smoke-workspace.ps1` ainda validava `scan-secrets.ps1`; agora valida o contrato Linux atual via `bash -n tools/governance/scan-secrets.sh`.
  3. `portfolio/PROJECT_STRUCTURE.txt` ainda orientava `python -m http.server`; agora documenta `npm start` e os builds reais de CSS/JS.
  4. As fallbacks globais `testing-standards` em `~/.config/opencode`, `~/.copilot` e `~/.agent` ainda descreviam um estate legado de 14 microservices; agora sao fallbacks repo-agnosticos orientados por manifests/instrucoes locais.
- Evidencias finais consolidadas:
  - `preflight-prompt`: `audit-compliance.py=100`, `verify-precedence.py=0`, `validate-mandatory-rules.py --strict => Findings: 0`
  - `meuagendamento-workspace`: `audit-compliance.py=100`, `verify-precedence.py=0`, `audit-workspace-baseline.py => OK`, `scripts/smoke-workspace.ps1 => Workspace smoke checks passed.`
  - `backend`: `audit-compliance.py=100`, `verify-precedence.py=0`
  - `frontend`: `audit-compliance.py=100`, `verify-precedence.py=0`
  - `landingPage`: `audit-compliance.py=100`, `verify-precedence.py=0`
  - `portfolio`: `audit-compliance.py=100`, `verify-precedence.py=0`, `audit-workspace-baseline.py => OK`, `validate-fast PASSED`
- Verificacao qualitativa final do loop nao encontrou findings acionaveis adicionais nas categorias remanescentes (versao Spring Boot, docs de start local, fallback testing skills e referencias `scan-secrets.ps1` / `python ./tools/governance`).
- Resultado final: zero actionable findings.
