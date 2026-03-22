# Preflight Prompt

Template profissional para inicializar ou harmonizar instruções de IA em repositórios novos e existentes, com foco em consistência, auditabilidade e compatibilidade entre OpenCode, GitHub Copilot VS Code, GitHub Copilot CLI e Antigravity/Gemini.

## Objetivo

Este projeto fornece um prompt base para orientar uma IA a:

- diagnosticar a estrutura real do repositório;
- organizar instruções por camadas (globais e específicas);
- configurar skills locais e globais para GitHub Copilot CLI sem quebrar os demais agentes;
- aplicar um gate de preflight obrigatório;
- preservar conteúdo existente com merge inteligente;
- padronizar governança de tarefas e mensagens de commit.

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
- Arquitetura de 4 ferramentas com espelhamento de skills locais (`.github/skills`) e globais (`~/.copilot/skills`) para Copilot CLI;
- Preservação de conteúdo útil sem sobrescrita cega;
- Idempotência (execuções repetidas sem degradação);
- Auditoria por lista de arquivos criados/modificados e justificativas;
- Política obrigatória de commit message com Conventional Commits em pt-BR.

## Boas práticas recomendadas

- Execute primeiro em modo diagnóstico para validar impacto;
- Ajuste apenas o necessário para o stack detectado;
- Revise conflitos entre instruções globais e específicas por caminho;
- Mantenha regras críticas no topo dos arquivos principais de instrução.

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
