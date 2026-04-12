---
name: gh-operations
description: Global fallback skill for GitHub repository, workflow run, pull request, issue, and release workflows using gh across any workspace.
license: Complete terms in LICENSE.txt
---

# Skill - gh-operations (global fallback)

Use this skill for GitHub tasks where `gh` is the primary interface: project discovery, workflow runs, job inspection, pull requests, issues, releases, or workspace-to-repository resolution.

## When to use

- Requests mentioning GitHub or `gh`.
- Workflow run, job, PR, issue, release, milestone, environment, or project-status queries.
- Requests like `buscar o status de todos os workflows do projeto do workspace X`.
- Tasks that start from a local workspace/path and need the owning GitHub repository resolved first.

## Resolution order

1. If the active git worktree contains `.opencode/skills/gh-operations/SKILL.md`, prefer that local skill.
2. Also inspect local `PRE-FLIGHT.md`, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, and `.github/skills/gh-operations/SKILL.md` when present.
3. Use this global skill as the fallback.

## Mandatory workflow

1. Resolve the repository that owns the target workspace, path, or project.
2. Resolve GitHub host and repository full path from `git remote get-url origin`, `gh repo view`, or explicit user input.
3. Check `gh` authentication for the target host when live GitHub data is required.
4. Prefer high-level `gh` commands first.
5. Use `gh api` only when you need fields, pagination, or endpoints not exposed by the high-level command.
6. Summarize results in plain language instead of dumping raw JSON unless the user explicitly asks for the raw payload.
7. For mutating actions, require clear user intent when the operation is destructive or hard to undo.

## Repository resolution rules

- If the user names a directory, file, workspace, or subproject, resolve which git repository owns that target before running `gh`.
- Never assume a workspace root owns the target when the workspace contains nested repositories.
- When possible, prefer `-R/--repo <owner/repo>` so `gh` does not depend on the current directory.
- When `gh api` is required outside the repository directory, build the endpoint with the explicit owner/repo path.
- If the request mentions `workspace <X>` and the workspace contains multiple repositories, identify the candidates first and only ask a question if the request is still materially ambiguous after discovery.

## Preferred commands

### Auth and project identity

- `gh auth status`
- `gh repo view -R <owner/repo> --json nameWithOwner,url,defaultBranchRef`

### Workflow runs (GitHub Actions)

- Recent workflow runs: `gh run list -R <owner/repo> --limit 20 --json databaseId,workflowName,status,conclusion,headBranch,displayTitle,updatedAt,url`
- Branch workflow status: `gh run list -R <owner/repo> --branch <branch> --limit 20 --json databaseId,workflowName,status,conclusion,headBranch,displayTitle,updatedAt,url`
- Failed workflow runs: `gh run list -R <owner/repo> --status failure --limit 20 --json databaseId,workflowName,status,conclusion,headBranch,displayTitle,updatedAt,url`
- Workflow run details: `gh run view <run-id> -R <owner/repo>`
- Job logs: `gh run view <run-id> -R <owner/repo> --log`

### Pull requests, issues, and releases

- `gh pr list -R <owner/repo> --state open --json number,title,author,headRefName,baseRefName,url,createdAt`
- `gh issue list -R <owner/repo> --state open --json number,title,author,labels,createdAt,url`
- `gh release list -R <owner/repo> --limit 20`

## Query interpretation defaults

- `status de todos os workflows`: list recent workflow runs, then summarize by status, conclusion, branch, updated time, and run ID.
- `workflow atual`: use `gh run list` for the requested branch, or the current/default branch if none was specified.
- `workflows falhos`: use `gh run list --status failure`.
- `jobs do workflow X`: use `gh run view <run-id>` to see jobs, or `gh run view <run-id> --log` for logs.
- `PRs abertas`, `issues abertas`, `ultimas releases`: use the matching high-level list command with JSON output and summarize the results.
- `do projeto do workspace X`: resolve the repo that owns workspace `X`, then query that repo with `gh`.

## Multi-repo workspace sweeps

- If the user requests all repositories in a workspace, discover candidate repos first, then run independent `gh` queries in parallel.
- Normalize each repo summary to: repo, branch, status, conclusion, updated_at, key ID, and web URL when useful.
- Report missing auth, missing remotes, or unresolved project mappings per repo instead of failing the whole sweep silently.

## Output contract

- Lead with the direct answer.
- State which repo or repos were inspected.
- State the branch, filter, or time window used.
- Highlight failed, running, and pending items first.
- Mention unknowns explicitly when auth, host resolution, or project mapping is incomplete.

## Safety and auth

- Read-only inspection commands do not need extra confirmation.
- For destructive or state-changing commands such as `cancel`, `delete`, `rerun`, `merge`, `approve`, or `close`, require clear user intent first.
- Never print tokens from environment variables or auth stores.
- Never guess a host, owner, or repo slug when it can be resolved from git remotes.

## Fallbacks and productivity rules

- If a high-level `gh` command does not expose the field you need, switch to `gh api` instead of using browser scraping.
- If JSON shaping is needed and `jq` is unavailable, use the local runtime already present in the environment (for example Python) to summarize safely.
- Prefer a single repo command with `-R` for ad hoc questions, and only change the working directory when repository ownership discovery requires it.
- Use `gh run watch` only when a live watch is explicitly useful.

## Mandatory final code review, cross-validation, and factual integrity

- At the end of every implementation/refactor/fix, perform a final code review before marking the task complete.
- Cross-validation is mandatory and does not replace code review: validate outputs against at least two independent sources of evidence (for example tests/build logs, contract/docs, runtime behavior, or diff-based verification).
- Final approval requires both gates: (1) technical code review quality and (2) evidence-based cross-validation consistency.
- Review and cross-validation must verify correctness, security, performance, readability, test impact, and compatibility with existing architecture/contracts.
- It is allowed (and encouraged) to use internet sources and up-to-date documentation (including Context7 and official docs) to close knowledge gaps.
- Never invent facts, APIs, versions, behaviors, references, or validation results; if uncertain, verify first or explicitly state uncertainty.
