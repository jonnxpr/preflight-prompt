# Preflight Prompt

Template profissional para inicializar ou harmonizar instruções de IA em repositórios novos e existentes, com foco em consistência, auditabilidade e compatibilidade entre OpenCode, GitHub Copilot VS Code, GitHub Copilot CLI e Antigravity/Gemini.

## Objetivo

Este projeto fornece um prompt base para orientar uma IA a:

- diagnosticar a estrutura real do repositório;
- organizar instruções por camadas (globais e específicas);
- configurar skills locais e globais para GitHub Copilot CLI e OpenCode sem quebrar os demais agentes;
- aplicar um gate de preflight obrigatório;
- preservar conteúdo existente com merge inteligente;
- padronizar governança de tarefas e mensagens de commit;
- resolver corretamente o repositório Git dono de cada caminho, inclusive em workspaces com nested repos;
- fortalecer governança MCP e validação de precedência com evidência auditável.

## Público-alvo

- Engenheiros de software que usam IA no fluxo de desenvolvimento;
- Times que precisam padronizar instruções entre ferramentas;
- Projetos que exigem previsibilidade e rastreabilidade nas respostas de agentes.

## Estrutura do repositório

- `PRE-FLIGHT-PROMPT.md`: prompt principal (copiar e colar na IA alvo).
- `README.md`: documentação do projeto e guia de uso.

## Como usar

1. Abra o arquivo `PRE-FLIGHT-PROMPT.md`.
2. Copie o conteúdo completo do prompt.
3. Cole no assistente de IA que irá configurar o projeto alvo.
4. Informe o caminho do projeto e preferências relevantes (stack, estilo de commit, ferramentas).
5. Execute em duas fases:
	- Fase 1: diagnóstico e plano;
	- Fase 2: implementação.

## O que este prompt garante

- Gate de preflight explícito para bloquear execuções incompletas;
- Compatibilidade por capacidade (com fallback por ambiente);
- Arquitetura de 4 ferramentas com camadas locais e globais para OpenCode (`.opencode/skills`), Copilot CLI (`.github/skills`, `~/.copilot/skills`) e demais agentes;
- Descoberta correta de contexto Git tanto para raiz sem repositório quanto para raiz com repositório + sub-repositórios aninhados;
- Verificação de precedência semântica, evitando falsos positivos por menções incidentais em títulos ou texto solto;
- Governança MCP com uso de variáveis de ambiente, perfis VS Code dinâmicos e DSN como fonte de verdade quando aplicável;
- Segurança operacional para não tentar commitar/pushar arquivos fora de qualquer repositório Git;
- Execução de toolkit de governança com evidência por alvo, incluindo compliance e precedence;
- Preservação de conteúdo útil sem sobrescrita cega;
- Idempotência (execuções repetidas sem degradação);
- Auditoria por lista de arquivos criados/modificados e justificativas;
- Política obrigatória de commit message com Conventional Commits em pt-BR.

## Boas práticas recomendadas

- Execute primeiro em modo diagnóstico para validar impacto;
- Ajuste apenas o necessário para o stack detectado;
- Revise conflitos entre instruções globais e específicas por caminho;
- Mantenha regras críticas no topo dos arquivos principais de instrução;
- Faça a validação final com `audit-compliance.py` e `verify-precedence.py` quando o projeto possuir toolkit de governança;
- Em workspaces com vários repositórios, confirme sempre o repo dono do caminho antes de qualquer operação Git.

## Aprendizados consolidados nesta versão

- A raiz do workspace pode ser um repositório válido e ainda conter nested repos; o prompt agora cobre os dois casos explicitamente.
- A linha de precedência canônica deve aparecer nos arquivos raiz para facilitar auditoria automatizada sem heurísticas frágeis.
- Em nested repos, `AGENTS.md`, `GEMINI.md` e `.github/copilot-instructions.md` também precisam explicitar os tokens de precedência em ordem; herança genérica não basta para auditoria semântica.
- A camada `.opencode/skills/*` precisa ser tratada como primeira classe, e não apenas como espelho implícito de outras ferramentas.
- O OpenCode usa `.opencode/commands/` para discovery de comandos; `.opencode/command/` gera drift e precisa ser evitado.
- Hubs não-git podem expor apenas comandos roteadores do Speckit, mas não devem possuir `.specify/` ou `specs/`; já roots que são git repos podem ter specs próprios sem contaminar nested repos.
- Perfis VS Code para MCP devem ser descobertos dinamicamente; não se deve assumir um identificador fixo de profile.
- Artefatos gerados de governança (por exemplo `tasks/compliance-report.md`, `tasks/precedence-report.md`, `tasks/workspace-baseline-report.md`, `tasks/secret-scan.sarif`) devem ser tratados como evidência gerada e ignorados/destrackeados quando não forem fonte de verdade.
- Descoberta automática de child repos precisa diferenciar `.git` diretório de `.git` arquivo de worktree para não aplicar rollout em worktrees paralelos por engano.
- Antes de commit/push, é obrigatório descobrir a política de branch do repo dono; não se deve assumir `main` quando o fluxo real usa `feature/*`, `homologation` ou outro branch operacional.
- Quando o toolkit fornecer auditoria de baseline de workspace, ela deve ser executada junto com compliance e precedence para fechar o diagnóstico global com evidência completa.
- Em cenários com arquivos fora de repositório, o fluxo correto é reportar como mudança local ou gerar patch, nunca forçar commit/push.

## Limites e escopo

- Este repositório não instala ferramentas automaticamente.
- O resultado final depende da capacidade do agente/IDE utilizado.
- O prompt orienta decisões; validações no projeto alvo continuam necessárias.

## Contribuição

Contribuições são bem-vindas para melhorar clareza, cobertura de cenários e compatibilidade entre ambientes.

Sugestão de fluxo:

1. Propor melhoria com contexto objetivo;
2. Atualizar o prompt sem perder conteúdo útil existente;
3. Garantir legibilidade e ausência de duplicação;
4. Validar exemplos e critérios de aceite.
