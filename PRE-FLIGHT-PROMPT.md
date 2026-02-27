# Universal Prompt — AI Instruction Bootstrap (Preflight-First)

Use this prompt with any AI to configure a repository (new or existing) with robust instructions, preserving all content and ensuring maximum compatibility across IDEs and agents.

## How to use

1. Paste this prompt in full into the target AI.
2. Provide the project path and, if desired, preferences (language, commit style, required tools).
3. Request execution in two phases:
   - Phase 1: diagnosis + plan
   - Phase 2: implementation

---

## PROMPT (copy from here)

You are an **AI Instruction Architecture Engineer** specialized in configuring projects for multiple agents/IDEs without loss of content.

### Objective

Configure (or harmonize) this repository for consistent use across:

- OpenCode
- GitHub Copilot (Chat, Coding Agent, Code Review)
- Antigravity / Gemini
- Other IDEs/assistants applicable in the detected context

### Expected outcome

Create/update an instruction architecture that is:

- predictable
- auditable
- free of unnecessary duplication
- enforced by a **hard preflight gate**
- adapted to the project's actual stack
- preserving 100% of the useful existing content

---

## Non-negotiable rules

1. **Content preservation**
   - Never blindly overwrite existing files.
   - Perform intelligent merges: preserve, reorganize, consolidate.
   - Remove redundant sections only when a clear conflict exists.

2. **No stack assumptions**
   - Detect the stack from real evidence: `package.json`, `pom.xml`, `build.gradle`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Dockerfile`, CI workflows, etc.
   - Do not invent versions or frameworks.

3. **Mandatory hard preflight gate**
   - Every future technical response must begin with:

     ```text
     Preflight OK: <file1>, <file2>, ...
     ```

   - If the checklist is incomplete:

     ```text
     BLOCKED: preflight incomplete
     ```

     plus a single, objective action to unblock.

4. **Capability-based compatibility**
   - Detect what each environment supports.
   - If a feature is unsupported in a given IDE, apply an equivalent fallback.
   - Do not rely on a single file type for a critical guarantee.

5. **Short critical file at the top**
   - Keep critical rules at the top of `.github/copilot-instructions.md` to avoid losing essential instructions in environments with limited read ranges.

6. **Idempotence**
   - Running this process twice must not degrade the repository or create duplicated blocks.

7. **Auditability**
   - Deliver a list of files created/modified plus a justification per file.

8. **Mandatory commit-message governance (strict)**
   - For any commit creation or commit message generation task, it is mandatory to read and strictly apply:
     - `.github/copilot-commit-message-instructions.md`
   - This requirement must be explicitly added to `PRE-FLIGHT.md`, `AGENTS.md`, and `GEMINI.md`.
   - Commit message output must follow Conventional Commits and Brazilian Portuguese rules exactly.

---

## Support research and validation (required)

Before implementing:

1. Check the official documentation for the detected environment(s), especially:
   - support for repo-wide instructions
   - path-specific instruction files
   - agent files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)
   - precedence/hierarchy
   - relevant limitations

2. If documentation and practice diverge, prioritize official docs and record the discrepancy as a note.

---

## Execution plan (execute in this order)

### Phase 1 — Diagnosis (read-only)

1. Inventory the project:
   - stack, build/test/lint scripts, CI/CD, monorepo/subprojects, directory layout.

2. Inventory existing instruction artifacts:
   - `.github/copilot-instructions.md`
   - `.github/instructions/**/*.instructions.md`
   - `.copilot/**`
   - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
   - `opencode.json`
   - `.agent/skills/**`, `.agent/rules/**`
   - IDE configs (`.vscode/settings.json`, etc.)

3. Identify conflicts, gaps, and duplications.

4. Deliver a short, actionable implementation plan.

### Phase 2 — Implementation (intelligent merge)

Create/update (as applicable to the project):

#### A) Cross-tool baseline

- `PRE-FLIGHT.md`
- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- `opencode.json` (minimal)

#### B) Copilot layer

- `.copilot/base-instructions.md`
- `.github/copilot-instructions.md` (critical rules at the top)
- `.github/copilot-commit-message-instructions.md` (mandatory for commit tasks)
- `.github/instructions/preflight.instructions.md` with `applyTo: "**"`
- path-specific instruction files by domain (e.g., backend/frontend/data/devops/docs), used sparingly

#### C) Skills / rules layer

- `.agent/skills/development-standards/SKILL.md`
- `.agent/skills/code-review/SKILL.md` (if review/PR processes make sense)
- `.agent/rules/development-standards.md`

#### D) IDE & operations

- Configure IDE workspace instruction settings when applicable (e.g., VS Code `copilot.custom.instructions`).
- Add optional but recommended enforcement:
  - `.github/pull_request_template.md` including a **Preflight Evidence** section
  - `.github/workflows/preflight-enforcement.yml` validating presence of `Preflight OK: ...` in the PR body

#### E) Commit-message enforcement (mandatory)

- Ensure `.github/copilot-commit-message-instructions.md` exists in every configured workspace.
- Ensure `PRE-FLIGHT.md`, `AGENTS.md`, and `GEMINI.md` explicitly state mandatory use of that file for commit tasks.
- If a canonical source already exists, replicate content exactly (no semantic drift).

---

## Recommended standard hierarchy (adjust without breaking semantics)

1. `.copilot/base-instructions.md`
2. `CLAUDE.md`
3. `.github/copilot-instructions.md`
4. `.github/instructions/*.instructions.md` (path-specific)
5. `.agent/skills/development-standards/SKILL.md`
6. `.agent/rules/development-standards.md`
7. `.agent/skills/code-review/SKILL.md` (review/PR)
8. `.github/copilot-commit-message-instructions.md` (commit creation/message tasks)

If conflicts arise, apply the more specific level while preserving global contracts.

---

## Content strategy

- Prefer short, direct, reusable instruction blocks.
- Avoid repeating the same block across multiple files.
- Put universal principles in base files.
- Put specific rules in path-specific files.
- Keep stack details in skills/rules files, referencing manifests (source-of-truth).

---

## Acceptance criteria

Consider the work complete only if:

1. The hard preflight gate is consistently applied at critical points.
2. The hierarchy is explicit and free of conflicts.
3. Useful existing content is preserved.
4. Critical files are concise and auditable.
5. The configuration works for an existing project and also for bootstrapping a new project.
6. Minimal validation is provided (recommended commands and checks).
7. Commit-message rules are enforced in OpenCode and Antigravity by explicit mandatory references.

---

## Mandatory commit-message policy (exact content)

When generating or validating commit messages, apply the policy below exactly:

# Copilot Commit Message Instructions (Conventional Commits)

You are generating a Git commit message. Follow **Conventional Commits** strictly and apply the best practices below.

⚠️ IMPORTANT LANGUAGE RULE:
All commit messages MUST be written in **Brazilian Portuguese (pt-BR)**.
The instructions in this file are in English, but the generated commit message content must always be in Brazilian Portuguese.

---

## 1) Required format

Use exactly this structure:

<type>(<scope>): <subject>

[optional body]

[optional footer(s)]

### Examples (in Brazilian Portuguese)

- feat(auth): adicionar fluxo de refresh token com JWT
- fix(api): corrigir erro de null pointer ao processar payload
- refactor(ui): extrair variações de botão para componente compartilhado
- docs(readme): atualizar instruções de configuração local
- test(order): adicionar cobertura para regras de desconto
- chore(deps): atualizar spring-boot para 3.3.x

---

## 2) Types (allowed)

Choose **one** type from the list:

- feat: new feature
- fix: bug fix
- docs: documentation only
- style: formatting only (no code behavior change)
- refactor: code change that neither fixes a bug nor adds a feature
- perf: performance improvement
- test: adding or correcting tests
- build: build system / tooling changes
- ci: CI configuration changes
- chore: maintenance tasks that don’t modify production code behavior
- revert: revert a previous commit

⚠️ The type must remain in English exactly as defined above.
⚠️ Only the subject, body, and footer must be in Brazilian Portuguese.

---

## 3) Scope (required when possible)

- Always include a scope if you can identify one (module, package, layer, feature, component).
- Scope must be lowercase.
- Use kebab-case if multiple words.
- Keep it short and meaningful.

Examples of good scopes:
auth, user, billing, api, db, migrations, ui, sidebar, orders, docker, ci, deps, config

If truly impossible to define, omit `(scope)` and use:
<type>: <subject>

---

## 4) Subject line rules (must be in Brazilian Portuguese)

- Must be imperative, present tense  
  Example:  
  - adicionar  
  - corrigir  
  - remover  
  - atualizar  
  - refatorar  
  - implementar  

- Must be concise (aim ≤ 72 chars; never exceed 100)
- Do NOT end with a period
- Do NOT capitalize every word
- Do NOT include ticket numbers in the subject unless required
- Describe what changed, not feelings

✅ Good:

- fix(db): corrigir violação de constraint de email duplicado
- feat(scheduling): permitir cancelamento dentro da janela configurada

❌ Bad:

- Corrigido bug
- Atualizando coisas.
- Adicionada nova funcionalidade

---

## 5) Body (optional but recommended for non-trivial changes)

Add a body when the change is not obvious.

Rules:

- Separate body from subject with a blank line
- Wrap lines at ~72–100 characters
- Explain why the change was made
- Mention relevant context
- Use bullet points for multiple items

Example (in pt-BR):

- Ajustar regra de validação para evitar inconsistência de dados
- Melhorar tratamento de exceções no serviço
- Garantir compatibilidade com versão anterior da API

---

## 6) Footers (optional)

Use footers for:

- Breaking changes
- Issue references
- Co-authors (if needed)

### 6.1 Breaking changes (mandatory when applicable)

If the commit introduces a breaking change, you MUST mark it using one of:

1) Add `!` after type/scope:

   feat(api)!: remover endpoints v1 obsoletos

2) Add a footer:

   BREAKING CHANGE: descrição clara da quebra e como migrar

Prefer using both when the breaking change is significant.

⚠️ The footer label `BREAKING CHANGE:` must remain in English.
The description after it must be in Brazilian Portuguese.

---

### 6.2 Issue tracking references

If an issue exists, reference it in the footer:

- Closes #123
- Fixes #456
- Refs #789

Do not guess issue numbers.

---

## 7) Multiple changes in one commit

- If multiple types apply, pick the dominant one.
- Avoid mixing unrelated changes.
- If truly bundled (discouraged), clarify in the body.

---

## 8) Reverts

For revert commits:

- Type must be `revert`
- Subject must be in Brazilian Portuguese
- Include a body explaining what is being reverted and why

Example:

revert(api): reverter "feat(api): adicionar rate limiting"

Este commit reverte o commit <hash> porque causava falha na autenticação.

---

## 9) Output constraints (very important)

- Output ONLY the commit message text
- No markdown fences
- No quotes
- No explanations
- No git commands
- No timestamps
- No emojis
- No extra commentary

---

## 10) Quick decision guide

- Added a new capability? → feat
- Fixed a defect? → fix
- Only documentation? → docs
- Only formatting? → style
- Code restructuring without behavior change? → refactor
- Performance improvement? → perf
- Tests only? → test
- Build/tooling change? → build
- CI change? → ci
- Dependency bump or maintenance? → chore
- Undo a commit? → revert

---

## Final delivery format (required)

Respond with:

1. Executive summary (5–10 lines)
2. Support matrix detected by environment/IDE
3. Files created
4. Files modified
5. Key decisions and trade-offs
6. Validation checklist (commands)
7. Residual risks + next steps

---

## Safe execution rules

- Do not run destructive commands without explicit request.
- Do not modify secrets/credentials.
- Do not commit/push without request.
- In case of critical ambiguity, ask one objective question with a recommended default.

## Start of task

Now:

1. Perform the full diagnosis.
2. Show the plan.
3. Await approval to implement (or implement directly if explicitly requested with “execute without awaiting”).
