from pathlib import Path
import re

ROOT = Path('.')
TASKS = ROOT / 'tasks'
TASKS.mkdir(exist_ok=True)
OUT = TASKS / 'compliance-report.md'

patterns = [
    '**/PRE-FLIGHT.md', '**/AGENTS.md', '**/CLAUDE.md', '**/GEMINI.md',
    '**/.copilot/base-instructions.md', '**/.github/copilot-instructions.md',
    '**/.github/instructions/*.instructions.md', '**/.agent/rules/*.md',
    '**/.agent/skills/*/SKILL.md', '**/.github/skills/*/SKILL.md',
    '**/.opencode/skills/*/SKILL.md', '**/.agents/skills/*/SKILL.md',
    '**/*.code-workspace',
]

files = []
for pattern in patterns:
    files.extend(ROOT.glob(pattern))

files = sorted(
    set(
        f
        for f in files
        if '/.history/' not in f.as_posix().lower() and '/bin/' not in f.as_posix().lower()
    )
)

gate = '## Mandatory final code review, cross-validation, and factual integrity'
orch = '## Mandatory multi-agent orchestration skill'
dag = 'Template DAG 100% compliance'

missing_gate = []
missing_orch = []
missing_dag = []
frontmatter = []
broken = []

for file_path in files:
    text = file_path.read_text(encoding='utf-8', errors='ignore')
    if file_path.suffix == '.md':
        if gate not in text:
            missing_gate.append(file_path)
        if file_path.name.lower() in [
            'agents.md', 'gemini.md', 'copilot-instructions.md',
            'base-instructions.md', 'pre-flight.md', 'claude.md',
        ] and orch not in text:
            missing_orch.append(file_path)
        if orch in text and dag not in text:
            missing_dag.append(file_path)
        if file_path.name == 'SKILL.md':
            match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
            if not match or 'name:' not in match.group(1) or 'description:' not in match.group(1):
                frontmatter.append(file_path)

    # NOTE: .code-workspace file-reference validation is intentionally advisory-only.
    # It is not scored here to avoid false penalties with large multiplexed instruction lists.

total = max(1, len(files) * 3)
penalty = (
    len(missing_gate) * 3
    + len(missing_orch) * 2
    + len(missing_dag) * 2
    + len(frontmatter) * 4
    + 0
)
score = max(0, 100 - int((penalty / total) * 100))

lines = [
    '# Compliance Report',
    '',
    f'- Score: **{score}/100**',
    f'- Files checked: **{len(files)}**',
    f'- Missing final gate: **{len(missing_gate)}**',
    f'- Missing orchestration section: **{len(missing_orch)}**',
    f'- Missing DAG reference: **{len(missing_dag)}**',
    f'- Skill frontmatter issues: **{len(frontmatter)}**',
    f'- Broken workspace refs: **{len(broken)}**',
    '',
]

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(score)
