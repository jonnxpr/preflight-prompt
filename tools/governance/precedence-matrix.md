# Precedence Matrix (OpenCode, Copilot VS Code, Copilot CLI, Antigravity)

## Cases

1. User-level vs workspace-level
2. Workspace-level vs repository-level
3. Repository-level vs path-specific
4. Repository instructions vs local skill layers (`.github/skills`, `.opencode/skills`, `.agent/skills`)
5. Nearest AGENTS/GEMINI in subfolders

## Procedure

1. Add unique marker token per layer.
2. Trigger one deterministic prompt per tool, including Copilot CLI.
3. Capture marker order in output.
4. Compare with expected hierarchy from workspace instructions.

## Automated verification

- Generate precedence report: `python ./tools/governance/verify-precedence.py`
- Enforce strict mode in CI: `python ./tools/governance/verify-precedence.py --strict`
