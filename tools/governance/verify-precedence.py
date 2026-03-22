from pathlib import Path
import argparse
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
    ROOT / '.copilot' / 'base-instructions.md',
    ROOT / '.github' / 'copilot-instructions.md',
]

MATRIX_TITLE = '# Precedence Matrix (OpenCode, Copilot VS Code, Copilot CLI, Antigravity)'


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def check_token_order(text: str) -> bool:
    positions = []
    for token in ORDER_TOKENS:
        index = text.find(token)
        if index == -1:
            return False
        positions.append(index)
    return positions == sorted(positions)


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
        for marker in [MATRIX_TITLE, '## Cases', '## Procedure', 'Copilot CLI']:
            if marker not in text:
                findings.append((str(matrix), f'Missing section or marker: {marker}'))

    for path in CORE_FILES:
        if not path.exists():
            continue
        text = read_text(path)
        if not check_token_order(text):
            findings.append((str(path), 'Missing or out-of-order precedence tokens for base/claude/copilot'))

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
