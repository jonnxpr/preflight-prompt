# Precedence Matrix (OpenCode, Copilot, Antigravity)

## Cases
1. User-level vs workspace-level
2. Workspace-level vs repository-level
3. Repository-level vs path-specific
4. Nearest AGENTS/GEMINI in subfolders

## Procedure
1. Add unique marker token per layer.
2. Trigger one deterministic prompt per tool.
3. Capture marker order in output.
4. Compare with expected hierarchy from workspace instructions.
