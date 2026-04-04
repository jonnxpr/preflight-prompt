"""
Cross-repo mandatory rules validation orchestrator.

This script runs from preflight-prompt and validates that mandatory rules
are consistently declared across all known project repositories. It
orchestrates repo-local audit-compliance.py scripts where they exist,
and performs cross-repo consistency checks independently.

Usage:
    python tools/governance/validate-mandatory-rules.py [--strict]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / "tasks"
TASKS.mkdir(exist_ok=True)
OUT = TASKS / "cross-repo-validation-report.md"

HOME = Path.home()

# Known repositories with their expected audit scripts
REPOS: dict[str, Path] = {
    "meuagendamento": HOME / "Documents" / "meuagendamento",
    "caradhras-poc": HOME / "Documents" / "caradhras-poc",
    "Portfolio": HOME / "Documents" / "Portfolio",
    "HelenSantosPortfolio": HOME / "Documents" / "HelenSantosPortfolio",
    "preflight-prompt": HOME / "Documents" / "preflight-prompt",
    "meuagendamento-governance": HOME / "Documents" / "meuagendamento-governance",
    "caradhras-poc-governance": HOME / "Documents" / "caradhras-poc-governance",
    "portfolio-governance": HOME / "Documents" / "portfolio-governance",
    "helen-santos-portfolio-governance": HOME
    / "Documents"
    / "helen-santos-portfolio-governance",
    "partner-governance": HOME
    / "workspace"
    / "ambiente-partner"
    / "partner-governance",
}

# Mandatory surface files that every project repo must have
MANDATORY_FILES = [
    "PRE-FLIGHT.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".copilot/base-instructions.md",
    ".github/copilot-instructions.md",
]

# Mandatory markers in AGENTS.md for all repos
MANDATORY_MARKERS = [
    "Preflight OK:",
    "BLOCKED: preflight incompleto",
    "Context7",
    "Before connecting to any MCP server, request user confirmation",
    "Template DAG 100% compliance",
    "## Mandatory final code review, cross-validation, and factual integrity",
    "tasks/todo.md",
    "tasks/lessons.md",
]

# Plan persistence markers
PLAN_MARKERS = [
    "plans/plan-${camelCaseName}.prompt.md",
    "plans/",
    "append-only",
]

# Governance repos must have audit-self.py
GOVERNANCE_REPOS = {
    "meuagendamento-governance",
    "caradhras-poc-governance",
    "portfolio-governance",
    "helen-santos-portfolio-governance",
    "partner-governance",
}

# Product repos must have audit-compliance.py
PRODUCT_REPOS = {
    "meuagendamento",
    "caradhras-poc",
    "Portfolio",
    "HelenSantosPortfolio",
    "preflight-prompt",
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def check_mandatory_files(repo_name: str, repo_path: Path) -> list[str]:
    findings = []
    for rel in MANDATORY_FILES:
        full = repo_path / rel
        if not full.exists():
            findings.append(f"[{repo_name}] Missing mandatory file: {rel}")
    return findings


def check_mandatory_markers(repo_name: str, repo_path: Path) -> list[str]:
    findings = []
    agents = repo_path / "AGENTS.md"
    if not agents.exists():
        return [f"[{repo_name}] AGENTS.md missing — cannot check markers"]
    text = read_text(agents)
    for marker in MANDATORY_MARKERS:
        if marker not in text:
            findings.append(f"[{repo_name}] AGENTS.md missing marker: {marker}")
    return findings


def check_plan_persistence(repo_name: str, repo_path: Path) -> list[str]:
    findings = []
    agents = repo_path / "AGENTS.md"
    if not agents.exists():
        return []
    text = read_text(agents)
    for marker in PLAN_MARKERS:
        if marker not in text:
            findings.append(
                f"[{repo_name}] AGENTS.md missing plan persistence marker: {marker}"
            )
            break  # One finding per repo is enough
    return findings


def check_governance_audit(repo_name: str, repo_path: Path) -> list[str]:
    findings = []
    if repo_name in GOVERNANCE_REPOS:
        audit = repo_path / "tools" / "governance" / "audit-self.py"
        if not audit.exists():
            findings.append(
                f"[{repo_name}] Missing governance audit: tools/governance/audit-self.py"
            )
    if repo_name in PRODUCT_REPOS:
        audit = repo_path / "tools" / "governance" / "audit-compliance.py"
        if not audit.exists():
            findings.append(
                f"[{repo_name}] Missing compliance audit: tools/governance/audit-compliance.py"
            )
    return findings


def check_preflight_instructions(repo_name: str, repo_path: Path) -> list[str]:
    findings = []
    preflight = repo_path / ".github" / "instructions" / "preflight.instructions.md"
    if not preflight.exists():
        # Only governance repos are guaranteed to have this
        if repo_name in GOVERNANCE_REPOS:
            findings.append(
                f"[{repo_name}] Missing .github/instructions/preflight.instructions.md"
            )
        return findings
    text = read_text(preflight)
    required = [
        "tasks/todo.md",
        "tasks/lessons.md",
        "Preflight OK:",
        "BLOCKED: preflight incompleto",
    ]
    for marker in required:
        if marker not in text:
            findings.append(
                f"[{repo_name}] preflight.instructions.md missing: {marker}"
            )
    return findings


def check_verify_precedence(repo_name: str, repo_path: Path) -> list[str]:
    findings = []
    script = repo_path / "tools" / "governance" / "verify-precedence.py"
    if not script.exists():
        findings.append(f"[{repo_name}] Missing tools/governance/verify-precedence.py")
    return findings


def run_local_audit(repo_name: str, repo_path: Path) -> list[str]:
    """Run the repo-local audit script if it exists and capture failures."""
    findings = []
    for script_name in ["audit-compliance.py", "audit-self.py"]:
        script = repo_path / "tools" / "governance" / script_name
        if not script.exists():
            continue
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode != 0:
                findings.append(
                    f"[{repo_name}] {script_name} returned exit code {result.returncode}"
                )
        except subprocess.TimeoutExpired:
            findings.append(f"[{repo_name}] {script_name} timed out (60s)")
        except Exception as e:
            findings.append(f"[{repo_name}] {script_name} execution error: {e}")
    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Cross-repo mandatory rules validation"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Exit with code 1 on any finding"
    )
    parser.add_argument(
        "--skip-local-audits",
        action="store_true",
        help="Skip running repo-local audit scripts",
    )
    args = parser.parse_args()

    all_findings: list[str] = []

    for repo_name, repo_path in sorted(REPOS.items()):
        if not repo_path.exists():
            all_findings.append(f"[{repo_name}] Repository path not found: {repo_path}")
            continue

        all_findings.extend(check_mandatory_files(repo_name, repo_path))
        all_findings.extend(check_mandatory_markers(repo_name, repo_path))
        all_findings.extend(check_plan_persistence(repo_name, repo_path))
        all_findings.extend(check_governance_audit(repo_name, repo_path))
        all_findings.extend(check_preflight_instructions(repo_name, repo_path))
        all_findings.extend(check_verify_precedence(repo_name, repo_path))

        if not args.skip_local_audits:
            all_findings.extend(run_local_audit(repo_name, repo_path))

    # Generate report
    lines = [
        "# Cross-Repo Mandatory Rules Validation Report",
        "",
        f"- Repositories checked: **{len(REPOS)}**",
        f"- Total findings: **{len(all_findings)}**",
        "",
    ]
    if all_findings:
        lines.append("## Findings")
        lines.append("")
        for f in all_findings:
            lines.append(f"- {f}")
    else:
        lines.append(
            "All mandatory rules validated successfully across all repositories."
        )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Findings: {len(all_findings)}")
    print(f"Report: {OUT}")

    if args.strict and all_findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
