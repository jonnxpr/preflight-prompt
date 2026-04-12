"""
Cross-repo mandatory rules validation orchestrator.

This script runs from preflight-prompt and validates that mandatory rules
are consistently declared across all known project repositories. It
orchestrates repo-local audit-compliance.py scripts where they exist,
and performs cross-repo consistency checks independently.

Usage:
    python3 tools/governance/validate-mandatory-rules.py [--strict]
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

REPO_ACTIVITY_MARKERS = [
    "PRE-FLIGHT.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "README.md",
    ".copilot",
    ".github",
    ".agent",
    ".opencode",
    "tools/governance",
    "tasks",
    ".git",
]

# Known repositories with their expected audit scripts
REPOS: dict[str, Path] = {
    "meuagendamento-workspace": HOME / "Documentos" / "meuagendamento-workspace",
    "caradhras-poc": HOME / "Documentos" / "caradhras-poc",
    "portfolio": HOME / "Documentos" / "portfolio",
    "helenSantosPortfolio": HOME / "Documentos" / "helenSantosPortfolio",
    "preflight-prompt": HOME / "Documentos" / "preflight-prompt",
    "meuagendamento-governance": HOME / "Documentos" / "meuagendamento-governance",
    "portfolio-governance": HOME / "Documentos" / "portfolio-governance",
    "helen-santos-portfolio-governance": HOME
    / "Documentos"
    / "helen-santos-portfolio-governance",
    "partner-governance": HOME
    / "Documentos"
    / "workspace"
    / "ambiente-partner"
    / "partner-governance",
}

# Mandatory surface files that every project repo must have
MANDATORY_FILES = [
    "PRE-FLIGHT.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
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

# Plan persistence markers (each must appear somewhere in AGENTS.md)
PLAN_MARKERS = [
    "plan-${camelCaseName}.prompt.md",
    "plans/",
    "append-only",
]

# Governance repos must have audit-self.py
GOVERNANCE_REPOS = {
    "meuagendamento-governance",
    "portfolio-governance",
    "helen-santos-portfolio-governance",
    "partner-governance",
}

# Product repos must have audit-compliance.py
PRODUCT_REPOS = {
    "meuagendamento-workspace",
    "caradhras-poc",
    "portfolio",
    "helenSantosPortfolio",
    "preflight-prompt",
}


def home_relative(path: Path) -> str:
    try:
        return f"~/{path.relative_to(HOME).as_posix()}"
    except ValueError:
        return path.as_posix()


def classify_repo_root(repo_path: Path) -> tuple[bool, str]:
    if not repo_path.exists():
        return False, "path not present on this machine"
    if not repo_path.is_dir():
        return False, "path is not a directory"
    if any((repo_path / marker).exists() for marker in REPO_ACTIVITY_MARKERS):
        return True, ""
    try:
        next(repo_path.iterdir())
    except StopIteration:
        return False, "directory exists but is empty/inactive"
    except OSError:
        return False, "directory is not readable"
    return False, "directory exists but no repo/governance markers were found"


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
            pass  # Report all missing plan persistence markers
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
    # Core markers every preflight.instructions.md must have
    core_required = [
        "Preflight OK:",
        "BLOCKED: preflight incompleto",
    ]
    for marker in core_required:
        if marker not in text:
            findings.append(
                f"[{repo_name}] preflight.instructions.md missing: {marker}"
            )
    # Tasks markers are only required in governance-repo preflight.instructions.md
    # (product repos delegate tasks governance to AGENTS.md / .copilot/base-instructions.md)
    if repo_name in GOVERNANCE_REPOS:
        tasks_required = [
            "tasks/todo.md",
            "tasks/lessons.md",
        ]
        for marker in tasks_required:
            if marker not in text:
                findings.append(
                    f"[{repo_name}] preflight.instructions.md missing: {marker}"
                )
    return findings


def check_verify_precedence(repo_name: str, repo_path: Path) -> list[str]:
    findings = []
    # verify-precedence.py is expected in product repos and partner-governance
    # Other governance repos use their sibling product repo's copy
    expected_repos = PRODUCT_REPOS | {"partner-governance"}
    if repo_name not in expected_repos:
        return findings
    script = repo_path / "tools" / "governance" / "verify-precedence.py"
    if not script.exists():
        findings.append(f"[{repo_name}] Missing tools/governance/verify-precedence.py")
    return findings


def check_gemini_integral_read(repo_name: str, repo_path: Path) -> list[str]:
    """G19: Every GEMINI.md must contain the integral read section markers."""
    findings = []
    gemini = repo_path / "GEMINI.md"
    if not gemini.exists():
        return findings
    text = read_text(gemini)
    integral_markers = [
        "Integral instruction read (mandatory)",
        "Read all mandatory files from first line through last line",
    ]
    for marker in integral_markers:
        if marker not in text:
            findings.append(
                f"[{repo_name}] GEMINI.md missing integral read marker: {marker}"
            )
    return findings


def check_subproject_agents(repo_name: str, repo_path: Path) -> list[str]:
    """G20: Subproject AGENTS.md files must contain preflight gate markers."""
    findings = []
    # Look for AGENTS.md one level deep (subprojects like backend/, frontend/, landingPage/)
    for sub_agents in repo_path.glob("*/AGENTS.md"):
        text = read_text(sub_agents)
        rel = sub_agents.relative_to(repo_path)
        for marker in ["Preflight OK:", "BLOCKED: preflight incompleto"]:
            if marker not in text:
                findings.append(
                    f"[{repo_name}] {rel} missing preflight marker: {marker}"
                )
    return findings


def check_global_agent_rules(repo_name: str, repo_path: Path) -> list[str]:
    """G21: ~/.agent/rules/ must exist (global config check, run once for any repo)."""
    findings = []
    if repo_name != "preflight-prompt":
        return findings
    rules_dir = HOME / ".agent" / "rules"
    if not rules_dir.exists():
        findings.append("[global] ~/.agent/rules/ directory does not exist")
    return findings


def check_global_gemini_gate(repo_name: str, repo_path: Path) -> list[str]:
    """G22: ~/.gemini/GEMINI.md must contain the gate directive."""
    findings = []
    if repo_name != "preflight-prompt":
        return findings
    candidates = [
        HOME / ".gemini" / "GEMINI.md",
        HOME / ".gemini" / "antigravity" / "GEMINI.md",
    ]
    gemini_global = next(
        (candidate for candidate in candidates if candidate.exists()), None
    )
    if gemini_global is None:
        findings.append(
            "[global] ~/.gemini/GEMINI.md or ~/.gemini/antigravity/GEMINI.md does not exist"
        )
        return findings
    text = read_text(gemini_global)
    for marker in [
        "Preflight OK:",
        "BLOCKED: preflight incompleto",
        "Integral instruction read (mandatory)",
    ]:
        if marker not in text:
            findings.append(
                f"[global] {home_relative(gemini_global)} missing marker: {marker}"
            )
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
    skipped_repos: list[tuple[str, Path, str]] = []
    active_repos = 0

    for repo_name, repo_path in sorted(REPOS.items()):
        is_active, skip_reason = classify_repo_root(repo_path)
        if not is_active:
            skipped_repos.append((repo_name, repo_path, skip_reason))
            continue

        active_repos += 1

        all_findings.extend(check_mandatory_files(repo_name, repo_path))
        all_findings.extend(check_mandatory_markers(repo_name, repo_path))
        all_findings.extend(check_plan_persistence(repo_name, repo_path))
        all_findings.extend(check_governance_audit(repo_name, repo_path))
        all_findings.extend(check_preflight_instructions(repo_name, repo_path))
        all_findings.extend(check_verify_precedence(repo_name, repo_path))
        all_findings.extend(check_gemini_integral_read(repo_name, repo_path))
        all_findings.extend(check_subproject_agents(repo_name, repo_path))
        all_findings.extend(check_global_agent_rules(repo_name, repo_path))
        all_findings.extend(check_global_gemini_gate(repo_name, repo_path))

        if not args.skip_local_audits:
            all_findings.extend(run_local_audit(repo_name, repo_path))

    # Generate report
    lines = [
        "# Cross-Repo Mandatory Rules Validation Report",
        "",
        f"- Repositories configured: **{len(REPOS)}**",
        f"- Active repositories checked: **{active_repos}**",
        f"- Skipped repositories: **{len(skipped_repos)}**",
        f"- Total findings: **{len(all_findings)}**",
        "",
    ]
    if skipped_repos:
        lines.append("## Skipped repositories")
        lines.append("")
        for repo_name, repo_path, reason in skipped_repos:
            lines.append(f"- `{repo_name}` (`{home_relative(repo_path)}`): {reason}")
        lines.append("")
    if all_findings:
        lines.append("## Findings")
        lines.append("")
        for f in all_findings:
            lines.append(f"- {f}")
    else:
        lines.append(
            "All mandatory rules validated successfully across all active repositories."
        )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Findings: {len(all_findings)}")
    print(f"Report: {OUT}")

    if args.strict and all_findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
