from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path('.')
TASKS = ROOT / 'tasks'
TASKS.mkdir(exist_ok=True)
OUT = TASKS / 'compliance-report.md'

GATE = '## Mandatory final code review, cross-validation, and factual integrity'
ORCH = '## Mandatory multi-agent orchestration skill'
DAG = 'Template DAG 100% compliance'
PREFLIGHT_OK = 'Preflight OK:'
PREFLIGHT_BLOCK = 'BLOCKED: preflight incompleto'
CONTEXT7 = 'Context7'
MCP_CONSENT = 'Before connecting to any MCP server, request user confirmation'
TASKS_READ_1 = 'tasks/todo.md'
TASKS_READ_2 = 'tasks/lessons.md'
TASKS_CREATE_HINT = 'If `tasks/` is missing, create `tasks/todo.md` and `tasks/lessons.md`'
COMMIT_POLICY = '.github/copilot-commit-message-instructions.md'

MANDATORY_PATTERNS = [
    '**/PRE-FLIGHT.md',
    '**/AGENTS.md',
    '**/CLAUDE.md',
    '**/GEMINI.md',
    '**/.copilot/base-instructions.md',
    '**/.github/copilot-instructions.md',
    '**/.github/instructions/*.instructions.md',
    '**/.agent/rules/*.md',
    '**/.agent/skills/*/SKILL.md',
    '**/.github/skills/*/SKILL.md',
    '**/.opencode/skills/*/SKILL.md',
    '**/.agents/skills/*/SKILL.md',
    '**/*.code-workspace',
]

REFERENCE_PATTERNS = [
    '**/*.code-workspace',
    '**/opencode.json',
    '**/.vscode/settings.json',
]


def is_ignored(path: Path) -> bool:
    p = path.as_posix().lower()
    return (
        '/.history/' in p
        or '/bin/' in p
        or p.startswith('bin/')
        or p.startswith('.history/')
    )


def collect(patterns):
    files = []
    for pattern in patterns:
        files.extend(ROOT.glob(pattern))
    return sorted(set(f for f in files if not is_ignored(f)))


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def rel(path: Path) -> str:
    return path.as_posix()


def add_finding(bucket: dict, category: str, path: Path, reason: str, fix: str):
    bucket.setdefault(category, []).append({
        'path': rel(path),
        'reason': reason,
        'fix': fix,
    })


def extract_quoted_path_candidates(text: str):
    out = []
    for m in re.finditer(r'["\']([^"\']+\.(?:md|json))["\']', text, re.I):
        raw = m.group(1).strip()
        if not raw:
            continue
        if '://' in raw:
            continue
        if raw.startswith('<') or raw.startswith('${') or raw.startswith('%'):
            continue
        if '*' in raw:
            continue
        lowered = raw.lower()
        if not any(token in lowered for token in [
            '.copilot/',
            '.github/',
            '.agent/',
            '.opencode/',
            '.vscode/',
            'pre-flight.md',
            'agents.md',
            'gemini.md',
            'claude.md',
            'copilot-instructions.md',
            'opencode.json',
            'skill.md',
        ]):
            continue
        out.append(raw)
    return out


def resolve_candidate(base: Path, candidate: str) -> Path:
    c = candidate.replace('\\', '/')
    if c.startswith('./'):
        return (base / c[2:]).resolve()
    if c.startswith('../'):
        return (base / c).resolve()
    if re.match(r'^[A-Za-z]:/', c):
        return Path(c)
    if c.startswith('/'):
        return Path(c)
    return (base / c).resolve()


def check_reference_integrity(reference_files, findings):
    for file_path in reference_files:
        text = read_text(file_path)
        if file_path.as_posix().endswith('.vscode/settings.json'):
            base = file_path.parent.parent
        else:
            base = file_path.parent
        for candidate in extract_quoted_path_candidates(text):
            target = resolve_candidate(base, candidate)
            if not target.exists():
                add_finding(
                    findings,
                    'broken_refs',
                    file_path,
                    f'Referenced path does not exist: {candidate}',
                    'Fix or remove stale path reference in workspace/tool settings.',
                )


def check_core_contracts(files, findings):
    root_core = {
        (ROOT / 'PRE-FLIGHT.md').resolve(),
        (ROOT / 'AGENTS.md').resolve(),
        (ROOT / 'GEMINI.md').resolve(),
        (ROOT / 'CLAUDE.md').resolve(),
        (ROOT / '.copilot' / 'base-instructions.md').resolve(),
        (ROOT / '.github' / 'copilot-instructions.md').resolve(),
    }

    for file_path in files:
        if file_path.suffix != '.md':
            continue

        is_root_core = file_path.resolve() in root_core
        text = read_text(file_path)
        name = file_path.name.lower()

        if GATE not in text:
            add_finding(
                findings,
                'missing_final_gate',
                file_path,
                'Missing mandatory final code review/cross-validation section.',
                f'Add section header: `{GATE}` with full policy block.',
            )

        if is_root_core and name in {
            'agents.md',
            'gemini.md',
            'copilot-instructions.md',
            'base-instructions.md',
            'pre-flight.md',
            'claude.md',
        } and ORCH not in text:
            add_finding(
                findings,
                'missing_orchestration',
                file_path,
                'Missing mandatory multi-agent orchestration section.',
                f'Add section `{ORCH}` including DAG requirement.',
            )

        if ORCH in text and DAG not in text:
            add_finding(
                findings,
                'missing_dag_reference',
                file_path,
                'Orchestration section exists but DAG requirement is missing.',
                f'Include `{DAG}` in the orchestration section.',
            )

        if file_path.name == 'SKILL.md':
            match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
            if not match or 'name:' not in match.group(1) or 'description:' not in match.group(1):
                add_finding(
                    findings,
                    'skill_frontmatter',
                    file_path,
                    'Skill file missing YAML frontmatter name/description.',
                    'Add YAML frontmatter with at least `name:` and `description:`.',
                )

        if is_root_core and name in {'pre-flight.md', 'copilot-instructions.md'}:
            if PREFLIGHT_OK not in text or PREFLIGHT_BLOCK not in text:
                add_finding(
                    findings,
                    'missing_preflight_gate',
                    file_path,
                    'Hard preflight strings are incomplete.',
                    'Ensure both `Preflight OK:` and `BLOCKED: preflight incompleto` are present.',
                )

        if is_root_core and name in {'pre-flight.md', 'agents.md', 'gemini.md'}:
            if COMMIT_POLICY not in text:
                add_finding(
                    findings,
                    'missing_commit_policy',
                    file_path,
                    'Mandatory commit-message instruction reference is missing.',
                    f'Add explicit mandatory reference to `{COMMIT_POLICY}`.',
                )

        if is_root_core and name in {
            'pre-flight.md',
            'agents.md',
            'gemini.md',
            'claude.md',
            'base-instructions.md',
            'copilot-instructions.md',
        }:
            if CONTEXT7 not in text:
                add_finding(
                    findings,
                    'missing_context7_policy',
                    file_path,
                    'Context7 policy reference is missing.',
                    'Add mandatory Context7 consultation policy for implementation/refactor/review.',
                )

            if MCP_CONSENT not in text:
                add_finding(
                    findings,
                    'missing_mcp_consent',
                    file_path,
                    'MCP connection consent sentence is missing.',
                    'Add explicit consent requirement before MCP connection.',
                )

        if is_root_core and name in {'pre-flight.md', 'claude.md'}:
            has_read = TASKS_READ_1 in text and TASKS_READ_2 in text
            has_create = ('tasks/' in text and 'missing' in text.lower() and 'create' in text.lower())
            if not has_read or not has_create:
                add_finding(
                    findings,
                    'missing_tasks_governance',
                    file_path,
                    'Tasks governance (read/create tasks files) is incomplete.',
                    'Include mandatory read + create-if-missing policy for tasks/todo.md and tasks/lessons.md.',
                )


def check_skill_routing(findings):
    frontend_skill = ROOT / '.agent' / 'skills' / 'frontend-design' / 'SKILL.md'
    if not frontend_skill.exists():
        return
    routing_files = [
        ROOT / 'PRE-FLIGHT.md',
        ROOT / 'AGENTS.md',
        ROOT / 'GEMINI.md',
        ROOT / '.github' / 'copilot-instructions.md',
    ]
    has_reference = False
    for path in routing_files:
        if path.exists() and 'frontend-design' in read_text(path):
            has_reference = True
            break
    if not has_reference:
        add_finding(
            findings,
            'missing_skill_routing',
            frontend_skill,
            'frontend-design skill exists without routing mention in core instruction files.',
            'Reference frontend-design in at least one core routing file (PRE-FLIGHT/AGENTS/GEMINI/copilot-instructions).',
        )


def count_findings(findings, keys):
    return sum(len(findings.get(k, [])) for k in keys)


def score_from_findings(findings):
    critical_keys = {
        'missing_preflight_gate',
        'skill_frontmatter',
        'broken_refs',
        'missing_commit_policy',
    }
    major_keys = {
        'missing_final_gate',
        'missing_orchestration',
        'missing_dag_reference',
        'missing_context7_policy',
        'missing_tasks_governance',
        'missing_mcp_consent',
        'missing_skill_routing',
    }

    critical = count_findings(findings, critical_keys)
    major = count_findings(findings, major_keys)
    minor = 0

    if critical == 0 and major == 0 and minor == 0:
        return 100, critical, major, minor

    penalty = critical * 12 + major * 5 + minor * 2
    score = max(0, 100 - penalty)
    if critical > 0 and score == 100:
        score = 99
    return score, critical, major, minor


def emit_report(files_checked, findings, score_tuple):
    score, critical, major, minor = score_tuple
    missing_gate = len(findings.get('missing_final_gate', []))
    missing_orch = len(findings.get('missing_orchestration', []))
    missing_dag = len(findings.get('missing_dag_reference', []))
    frontmatter = len(findings.get('skill_frontmatter', []))
    broken = len(findings.get('broken_refs', []))

    lines = [
        '# Compliance Report',
        '',
        f'- Score: **{score}/100**',
        f'- Files checked: **{files_checked}**',
        f'- Missing final gate: **{missing_gate}**',
        f'- Missing orchestration section: **{missing_orch}**',
        f'- Missing DAG reference: **{missing_dag}**',
        f'- Skill frontmatter issues: **{frontmatter}**',
        f'- Broken workspace refs: **{broken}**',
        f'- Critical findings: **{critical}**',
        f'- Major findings: **{major}**',
        f'- Minor findings: **{minor}**',
        '',
        '## Detailed Findings',
        '',
    ]

    if not any(findings.values()):
        lines.append('- No findings detected.')
    else:
        ordered = [
            'missing_preflight_gate',
            'missing_commit_policy',
            'skill_frontmatter',
            'broken_refs',
            'missing_final_gate',
            'missing_orchestration',
            'missing_dag_reference',
            'missing_context7_policy',
            'missing_tasks_governance',
            'missing_mcp_consent',
            'missing_skill_routing',
        ]
        for category in ordered:
            items = findings.get(category, [])
            if not items:
                continue
            lines.append(f'### {category}')
            for item in items:
                lines.append(f"- `{item['path']}` - {item['reason']} | Suggested fix: {item['fix']}")
            lines.append('')

    OUT.write_text('\n'.join(lines), encoding='utf-8')
    return score


def main():
    parser = argparse.ArgumentParser(description='Governance compliance audit')
    parser.add_argument('--strict', action='store_true', help='Exit with code 1 when any finding exists')
    args = parser.parse_args()

    files = collect(MANDATORY_PATTERNS)
    references = collect(REFERENCE_PATTERNS)
    findings = {}

    check_core_contracts(files, findings)
    check_reference_integrity(references, findings)
    check_skill_routing(findings)

    score_tuple = score_from_findings(findings)
    score = emit_report(len(files), findings, score_tuple)
    print(score)

    if args.strict and any(findings.values()):
        sys.exit(1)


if __name__ == '__main__':
    main()
