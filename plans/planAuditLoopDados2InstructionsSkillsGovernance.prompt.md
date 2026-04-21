# Audit Loop Dados2 Instructions Skills Governance

**Status:** completed
**Created:** 2026-04-21
**Scope:** all active workspaces/repos under `/media/jonathan/Dados2/Documentos` plus active global tool surfaces under `$HOME` (`~/.config/opencode`, `~/.copilot`, `~/.agent`, `~/.gemini/antigravity`)

## Objective

Executar audit loop autonomo e completo para garantir que arquitetura de instructions, skills e governanca esteja correta, coerente e sem drift acionavel em todos os projetos, workspaces e ferramentas ativos sob `/media/jonathan/Dados2/Documentos`.

## Context & Constraints

- Usuario definiu raiz operacional atual como `/media/jonathan/Dados2/Documentos`.
- Auditoria deve cobrir workspaces/repos ativos encontrados nessa raiz e superficies globais ativas sob `$HOME`.
- Fluxo obrigatorio: phase 0 inspeção qualitativa profunda, phase 1 scripts de governanca, correcoes por owner em batches minimos, reauditoria ate zero actionable findings.
- `preflight-prompt` continua owner da memoria/orquestracao cross-workspace.
- Nao commitar nem pushar sem solicitacao explicita do usuario.
- Se algum owner estiver fora de `Dados2`, tratar como fora do escopo ativo desta rodada, exceto se for superficie global em `$HOME`.

## Execution Steps

1. Inventariar owners ativos e ler planos/auditorias anteriores relevantes para evitar regressao de criterio.
2. Executar phase 0 qualitativa nos owners de `Dados2` e nas superficies globais ativas.
3. Executar phase 1 com `audit-compliance.py`, `verify-precedence.py`, `audit-workspace-baseline.py`, `audit-self.py`, `validate-mandatory-rules.py --strict` onde existirem.
4. Consolidar findings por owner/categoria e aplicar correcoes minimas com fonte de verdade no owner real.
5. Reexecutar inspecao e scripts.
6. Repetir loop ate zero actionable findings remanescentes.
7. Atualizar `tasks/todo.md`, `tasks/lessons.md` e este plano com evidencias finais.

## Acceptance Criteria

- Todos os owners ativos em `Dados2` foram inventariados e auditados.
- Superficies globais ativas relevantes foram verificadas contra a arquitetura atual.
- Toda correcao aplicada foi revalidada por script ou evidencia qualitativa objetiva.
- Resultado final consolidado deixa zero actionable findings.

## Decisions & Alternatives

- Owner escolhido: `preflight-prompt`, por ser memoria cross-workspace canonica.
- Estrategia escolhida: tratar `Dados2` como nova raiz ativa e nao presumir validade operacional de referencias antigas a `Dados`/`Dados1` sem prova local.
- Rejeitado: reusar cegamente inventario antigo de `Dados1`, porque mudanca de raiz pode implicar estate diferente.

## Execution Outcome Append (2026-04-21)

- Owners ativos confirmados em `/media/jonathan/Dados2/Documentos`: `preflight-prompt`, `meuagendamento-workspace`, `meuagendamento-governance`, `portfolio`, `portfolio-governance`, `helenSantosPortfolio` e `helen-santos-portfolio-governance`.
- Verificacao qualitativa adicional confirmou ausencia de estates Partner/Caradhras em `/media/jonathan/Dados`, `/media/jonathan/Dados1`, `/media/jonathan/Dados2` e `/home/jonathan`; referencias absolutas quebradas para esses owners foram tratadas como drift acionavel.
- Correcao minima aplicada: skills globais e repo-locais `governance-audit-loop`, fallbacks globais `development-standards` e `workspace-partner-router.md` deixaram de depender de paths absolutos inexistentes e passaram a usar rotas condicionais do tipo `*/workspace/ambiente-partner/projetos` / `*/caradhras-poc` quando presentes.
- Revalidacao final verde:
  - `preflight-prompt`: `audit-compliance.py = 100`, `verify-precedence.py = 0`, `validate-mandatory-rules.py --strict = Findings: 0`
  - `meuagendamento-workspace`: `audit-compliance.py = 100`, `verify-precedence.py = 0`, `audit-workspace-baseline.py = OK`
  - `portfolio`: `audit-compliance.py = 100`, `verify-precedence.py = 0`, `audit-workspace-baseline.py = OK`
  - `helenSantosPortfolio`: `audit-compliance.py = 100`, `verify-precedence.py = 0`, `audit-workspace-baseline.py = OK`
  - `meuagendamento-governance`, `portfolio-governance`, `helen-santos-portfolio-governance`: `audit-self.py --strict = OK`
- Cross-validacao qualitativa final: os unicos hits remanescentes de roots antigos ficaram restritos a historico append-only em `preflight-prompt/plans/**`, `preflight-prompt/tasks/{todo,lessons}.md` e memoria efemera em `~/.copilot/session-state/**`; nenhum deles e superficie live fonte de verdade desta rodada.
- Resultado consolidado: zero actionable findings remanescentes.
