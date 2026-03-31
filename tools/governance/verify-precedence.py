from pathlib import Path
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / 'tasks'
TASKS.mkdir(exist_ok=True)
OUT = TASKS / 'precedence-report.md'

ORDER_TOKENS = [
    '.copilot/base-instructions.md',
    'CLAUDE.md',
    '.github/copilot-instructions.md',
]

CORE_FILES = [
    ROOT / 'PRE-FLIGHT.md',
    ROOT / 'AGENTS.md',
    ROOT / 'GEMINI.md',
    ROOT / 'CLAUDE.md',
    ROOT / '.copilot' / 'base-instructions.md',
    ROOT / '.github' / 'copilot-instructions.md',
]

MATRIX_TITLE = '# Precedence Matrix (OpenCode, Copilot VS Code, Copilot CLI, Antigravity)'
MATRIX_MARKERS = [
    MATRIX_TITLE,
    '## Cases',
    '## Procedure',
    '## Automated verification',
    'Copilot CLI',
]


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def compile_token_pattern(token: str):
    escaped = re.escape(token)
    if token == 'CLAUDE.md':
        return re.compile(r'`CLAUDE\.md`|CLAUDE\.md')
    return re.compile(escaped)


def check_token_order(text: str):
    cursor = 0
    for token in ORDER_TOKENS:
        pattern = compile_token_pattern(token)
        match = pattern.search(text, cursor)
        if not match:
            return False, f'Missing precedence token: {token}'
        cursor = match.end()
    return True, None


def main():
    parser = argparse.ArgumentParser(description='Verify instruction precedence evidence')
    parser.add_argument('--strict', action='store_true', help='Exit with code 1 on any finding')
    args = parser.parse_args()

    findings = []
    matrix = ROOT / 'tools' / 'governance' / 'precedence-matrix.md'
    if not matrix.exists():
        findings.append((str(matrix), 'Missing precedence matrix file'))
    else:
        text = read_text(matrix)
        for marker in MATRIX_MARKERS:
            if marker not in text:
                findings.append((str(matrix), f'Missing section or marker: {marker}'))

    for path in CORE_FILES:
        if not path.exists():
            continue
        text = read_text(path)
        ok, reason = check_token_order(text)
        if not ok:
            findings.append((str(path), reason))

    lines = [
        '# Precedence Verification Report',
        '',
        f'- Findings: **{len(findings)}**',
        '',
    ]
    if findings:
        lines.append('## Findings')
        for path, reason in findings:
            lines.append(f'- `{path}` - {reason}')
    else:
        lines.append('- No precedence findings detected.')

    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(0 if not findings else len(findings))

    if args.strict and findings:
        sys.exit(1)


if __name__ == '__main__':
    main()
