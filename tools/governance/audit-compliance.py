from pathlib import Path
import argparse
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / "tasks"
TASKS.mkdir(exist_ok=True)
OUT = TASKS / "compliance-report.md"

GATE = "## Mandatory final code review, cross-validation, and factual integrity"
ORCH = "## Mandatory multi-agent orchestration skill"
DAG = "Template DAG 100% compliance"
PREFLIGHT_OK = "Preflight OK:"
PREFLIGHT_BLOCK = "BLOCKED: preflight incompleto"
CONTEXT7 = "Context7"
MCP_CONSENT = "Before connecting to any MCP server, request user confirmation"
COPILOT_CLI = "Copilot CLI"
COPILOT_SKILLS = ".github/skills/"
COPILOT_GLOBAL_SKILLS = "~/.copilot/skills/"
MCP_COPILOT_CONFIG = ".copilot/mcp-config.json"
MCP_GEMINI_CONFIG = ".gemini/antigravity/mcp_config.json"
MCP_PROFILE_CONFIG = "profiles/*/mcp.json"
TASKS_READ_1 = "tasks/todo.md"
TASKS_READ_2 = "tasks/lessons.md"
LESSONS_TEMPLATE = "# Lessons Learned\n\nRegistre aqui licoes apos correcoes explicitas do usuario para evitar repeticao de erros.\n\n- Data:\n- Contexto:\n- Correcao recebida:\n- Regra preventiva:\n- Como validar na proxima vez:\n"
TODO_TEMPLATE = "# Task Plan\n\nRegistre aqui as tarefas nao triviais em execucao neste repositorio ou workspace.\n\n- Objetivo:\n- Plano de execucao:\n- Evidencias esperadas:\n- Status/Resultado:\n"
TASKS_PLACEHOLDERS = {
    "# Lessons\n",
    "# Todo\n",
    "# TODO\n",
    "Use este arquivo para tarefas nao triviais",
    "## Template",
    "- Nenhuma licao registrada ainda.",
}
COMMIT_POLICY = ".github/copilot-commit-message-instructions.md"
JDK_ENV = "jdk-env.ps1"
JAVA_VERSION = "java -version"
GRADLE_WRAPPER = "gradlew-jdk.ps1"
MAVEN_WRAPPER = "mvn-jdk.ps1"

MANDATORY_PATTERNS = [
    "**/PRE-FLIGHT.md",
    "**/AGENTS.md",
    "**/CLAUDE.md",
    "**/GEMINI.md",
    "**/.copilot/base-instructions.md",
    "**/.github/copilot-instructions.md",
    "**/.github/instructions/*.instructions.md",
    "**/.agent/rules/*.md",
    "**/.agent/skills/*/SKILL.md",
    "**/.github/skills/*/SKILL.md",
    "**/.opencode/skills/*/SKILL.md",
    "**/*.code-workspace",
]

REFERENCE_PATTERNS = [
    "**/*.code-workspace",
    "**/opencode.json",
    "**/.vscode/settings.json",
]


def is_ignored(path: Path) -> bool:
    value = path.as_posix().lower()
    return (
        "/.history/" in value
        or "/.stryker-tmp/" in value
        or "/bin/" in value
        or value.startswith(".history/")
        or value.startswith(".stryker-tmp/")
        or value.startswith("bin/")
    )


def collect(patterns):
    files = []
    for pattern in patterns:
        files.extend(ROOT.glob(pattern))
    return sorted({path for path in files if path.exists() and not is_ignored(path)})


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def add_finding(bucket: dict, category: str, path: Path, reason: str, fix: str):
    bucket.setdefault(category, []).append(
        {
            "path": rel(path),
            "reason": reason,
            "fix": fix,
        }
    )


def extract_quoted_path_candidates(text: str):
    out = []
    for match in re.finditer(r'["\']([^"\']+\.(?:md|json))["\']', text, re.I):
        raw = match.group(1).strip()
        if (
            not raw
            or "://" in raw
            or raw.startswith("<")
            or raw.startswith("${")
            or raw.startswith("%")
            or "*" in raw
        ):
            continue
        lowered = raw.lower()
        if any(
            token in lowered
            for token in [
                ".copilot/",
                ".github/",
                ".agent/",
                ".opencode/",
                ".vscode/",
                "pre-flight.md",
                "agents.md",
                "gemini.md",
                "claude.md",
                "copilot-instructions.md",
                "opencode.json",
                "skill.md",
            ]
        ):
            out.append(raw)
    return out


def resolve_candidate(base: Path, candidate: str) -> Path:
    normalized = candidate.replace("\\", "/")
    if normalized.startswith("./"):
        return (base / normalized[2:]).resolve()
    if normalized.startswith("../"):
        return (base / normalized).resolve()
    if re.match(r"^[A-Za-z]:/", normalized):
        return Path(normalized)
    if normalized.startswith("/"):
        return Path(normalized)
    return (base / normalized).resolve()


def check_reference_integrity(reference_files, findings):
    for file_path in reference_files:
        text = read_text(file_path)
        base = (
            file_path.parent.parent
            if file_path.as_posix().endswith(".vscode/settings.json")
            else file_path.parent
        )
        for candidate in extract_quoted_path_candidates(text):
            target = resolve_candidate(base, candidate)
            if not target.exists():
                add_finding(
                    findings,
                    "broken_refs",
                    file_path,
                    f"Referenced path does not exist: {candidate}",
                    "Fix or remove stale path reference in workspace/tool settings.",
                )


def check_core_contracts(files, findings):
    root_core = {
        (ROOT / "PRE-FLIGHT.md").resolve(),
        (ROOT / "AGENTS.md").resolve(),
        (ROOT / "GEMINI.md").resolve(),
        (ROOT / "CLAUDE.md").resolve(),
        (ROOT / ".copilot" / "base-instructions.md").resolve(),
        (ROOT / ".github" / "copilot-instructions.md").resolve(),
    }
    root_names = {
        "pre-flight.md",
        "agents.md",
        "gemini.md",
        "claude.md",
        "base-instructions.md",
        "copilot-instructions.md",
    }

    for file_path in files:
        if file_path.suffix != ".md":
            continue
        text = read_text(file_path)
        is_root_core = file_path.resolve() in root_core
        name = file_path.name.lower()

        if GATE not in text:
            add_finding(
                findings,
                "missing_final_gate",
                file_path,
                "Missing mandatory final code review/cross-validation section.",
                f"Add section header: `{GATE}` with the canonical policy block.",
            )

        if is_root_core and name in root_names and ORCH not in text:
            add_finding(
                findings,
                "missing_orchestration",
                file_path,
                "Missing mandatory multi-agent orchestration section.",
                f"Add section `{ORCH}` including DAG requirement.",
            )

        if ORCH in text and DAG not in text:
            add_finding(
                findings,
                "missing_dag_reference",
                file_path,
                "Orchestration section exists but DAG requirement is missing.",
                f"Include `{DAG}` in the orchestration section.",
            )

        if file_path.name == "SKILL.md":
            match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if (
                not match
                or "name:" not in match.group(1)
                or "description:" not in match.group(1)
            ):
                add_finding(
                    findings,
                    "skill_frontmatter",
                    file_path,
                    "Skill file missing YAML frontmatter name/description.",
                    "Add YAML frontmatter with at least `name:` and `description:`.",
                )

        if is_root_core and name in {"pre-flight.md", "copilot-instructions.md"}:
            if PREFLIGHT_OK not in text or PREFLIGHT_BLOCK not in text:
                add_finding(
                    findings,
                    "missing_preflight_gate",
                    file_path,
                    "Hard preflight strings are incomplete.",
                    "Ensure both `Preflight OK:` and `BLOCKED: preflight incompleto` are present.",
                )

        if (
            is_root_core
            and name in {"pre-flight.md", "agents.md", "gemini.md"}
            and COMMIT_POLICY not in text
        ):
            add_finding(
                findings,
                "missing_commit_policy",
                file_path,
                "Mandatory commit-message instruction reference is missing.",
                f"Add explicit mandatory reference to `{COMMIT_POLICY}`.",
            )

        if is_root_core and name in root_names:
            if CONTEXT7 not in text:
                add_finding(
                    findings,
                    "missing_context7_policy",
                    file_path,
                    "Context7 policy reference is missing.",
                    "Add mandatory Context7 consultation policy for implementation/refactor/review.",
                )
            if MCP_CONSENT not in text:
                add_finding(
                    findings,
                    "missing_mcp_consent",
                    file_path,
                    "MCP connection consent sentence is missing.",
                    "Add explicit consent requirement before MCP connection.",
                )
            if (
                MCP_COPILOT_CONFIG not in text
                or MCP_GEMINI_CONFIG not in text
                or MCP_PROFILE_CONFIG not in text
            ):
                add_finding(
                    findings,
                    "incomplete_mcp_search",
                    file_path,
                    "MCP discovery order does not cover Copilot config, Antigravity MCP config, and VS Code profile MCP files.",
                    "Add .copilot/mcp-config.json, ~/.gemini/antigravity/mcp_config.json, and profiles/*/mcp.json to the discovery instructions.",
                )
            if COPILOT_CLI not in text:
                add_finding(
                    findings,
                    "missing_copilot_cli_contract",
                    file_path,
                    "Copilot CLI is not explicitly modeled as a first-class tool.",
                    "Mention GitHub Copilot CLI alongside OpenCode, Copilot VS Code, and Antigravity.",
                )

        if is_root_core and name in {
            "pre-flight.md",
            "agents.md",
            "gemini.md",
            "copilot-instructions.md",
            "base-instructions.md",
        }:
            if COPILOT_SKILLS not in text:
                add_finding(
                    findings,
                    "missing_copilot_cli_skill_layer",
                    file_path,
                    "Copilot CLI local skill layer is missing from the instruction contract.",
                    "Reference `.github/skills/*/SKILL.md` as the Copilot CLI local skill layer.",
                )

        if is_root_core and name in {"pre-flight.md", "claude.md"}:
            has_read = TASKS_READ_1 in text and TASKS_READ_2 in text
            has_create = (
                "tasks/" in text
                and "missing" in text.lower()
                and "create" in text.lower()
            )
            if not has_read or not has_create:
                add_finding(
                    findings,
                    "missing_tasks_governance",
                    file_path,
                    "Tasks governance (read/create tasks files) is incomplete.",
                    "Include mandatory read + create-if-missing policy for tasks/todo.md and tasks/lessons.md.",
                )


def check_tasks_files(findings):
    checks = [
        (TASKS / "lessons.md", LESSONS_TEMPLATE, "tasks_lessons_template_drift"),
        (TASKS / "todo.md", TODO_TEMPLATE, "tasks_todo_template_drift"),
    ]
    for path, template, category in checks:
        if not path.exists():
            add_finding(
                findings,
                category,
                path,
                "Tasks governance file is missing.",
                "Create the file with the exact canonical top block before adding repository-specific entries.",
            )
            continue
        text = read_text(path)
        if not text.startswith(template):
            add_finding(
                findings,
                category,
                path,
                "Tasks governance file does not preserve the exact canonical top block.",
                "Restore the exact canonical top block and keep historical content only below it.",
            )
        for placeholder in TASKS_PLACEHOLDERS:
            if placeholder in text:
                add_finding(
                    findings,
                    "tasks_placeholder_content",
                    path,
                    f"Tasks governance file still contains placeholder content: {placeholder.strip()}",
                    "Remove placeholder text and keep only the canonical template plus real history or active work.",
                )
                break


def check_skill_routing(findings):
    frontend_sources = [
        ROOT / ".opencode" / "skills" / "frontend-design" / "SKILL.md",
        ROOT / ".agent" / "skills" / "frontend-design" / "SKILL.md",
        ROOT / ".github" / "skills" / "frontend-design" / "SKILL.md",
    ]
    if not any(path.exists() for path in frontend_sources):
        return
    routing_files = [
        ROOT / "PRE-FLIGHT.md",
        ROOT / "AGENTS.md",
        ROOT / "GEMINI.md",
        ROOT / ".github" / "copilot-instructions.md",
    ]
    if not any(
        path.exists() and "frontend-design" in read_text(path) for path in routing_files
    ):
        add_finding(
            findings,
            "missing_skill_routing",
            ROOT / "PRE-FLIGHT.md",
            "frontend-design skill exists without routing mention in core instruction files.",
            "Reference frontend-design in at least one core routing file.",
        )


def check_java_multi_agent_contract(findings):
    has_gradle = (ROOT / "scripts" / GRADLE_WRAPPER).exists()
    has_maven = (ROOT / "scripts" / MAVEN_WRAPPER).exists()
    if not (has_gradle or has_maven):
        return
    expected_wrapper = GRADLE_WRAPPER if has_gradle else MAVEN_WRAPPER
    required_files = [
        ROOT / "PRE-FLIGHT.md",
        ROOT / "AGENTS.md",
        ROOT / "GEMINI.md",
        ROOT / ".github" / "copilot-instructions.md",
        ROOT / ".agent" / "skills" / "orchestrate-multi-agents" / "SKILL.md",
        ROOT / ".opencode" / "skills" / "orchestrate-multi-agents" / "SKILL.md",
        ROOT / ".github" / "skills" / "orchestrate-multi-agents" / "SKILL.md",
    ]
    for path in required_files:
        if not path.exists():
            continue
        text = read_text(path)
        if (
            JDK_ENV not in text
            or JAVA_VERSION not in text
            or expected_wrapper not in text
        ):
            add_finding(
                findings,
                "missing_java_multi_agent_runtime",
                path,
                "Java multi-agent runtime contract is incomplete.",
                f"Add explicit same-shell JDK selection with `{JDK_ENV}`, `{JAVA_VERSION}`, and `{expected_wrapper}`.",
            )


def check_copilot_cli_skill_mirrors(findings):
    source_names = set()
    for base in [ROOT / ".opencode" / "skills", ROOT / ".agent" / "skills"]:
        if not base.exists():
            continue
        for skill in base.glob("*/SKILL.md"):
            if is_ignored(skill):
                continue
            source_names.add(skill.parent.name)
    for name in sorted(source_names):
        target = ROOT / ".github" / "skills" / name / "SKILL.md"
        if not target.exists():
            add_finding(
                findings,
                "missing_copilot_cli_skill_mirror",
                ROOT / ".github",
                f"Missing Copilot CLI local skill mirror for `{name}`.",
                f"Create `.github/skills/{name}/SKILL.md` aligned with the local skill source.",
            )


def check_global_copilot_cli_skills(findings):
    home = Path.home()
    opencode_root = home / ".config" / "opencode" / "skills"
    copilot_root = home / ".copilot" / "skills"
    required = {"development-standards", "code-review", "orchestrate-multi-agents"}
    if (opencode_root / "frontend-design" / "SKILL.md").exists():
        required.add("frontend-design")
    for name in sorted(required):
        if not (copilot_root / name / "SKILL.md").exists():
            add_finding(
                findings,
                "missing_global_copilot_cli_skill",
                ROOT / "tools" / "governance" / "audit-compliance.py",
                f"Missing global Copilot CLI skill `{name}` under `~/.copilot/skills/`.",
                f"Create `{COPILOT_GLOBAL_SKILLS}{name}/SKILL.md` aligned with the global fallback skill architecture.",
            )


def check_user_mcp_runtime(findings):
    home = Path.home()
    appdata = Path(os.environ.get("APPDATA", "")) if os.environ.get("APPDATA") else None
    runtime_targets = [
        home / ".config" / "opencode" / "opencode.json",
        home / ".copilot" / "mcp-config.json",
        home / ".gemini" / "antigravity" / "mcp_config.json",
    ]
    if appdata:
        runtime_targets.extend(
            [
                appdata / "Code" / "User" / "mcp.json",
                appdata / "Code" / "User" / "profiles" / "149c18e5" / "mcp.json",
                appdata / "Antigravity" / "User" / "mcp.json",
            ]
        )
    found_context7 = False
    for path in runtime_targets:
        if path.exists():
            text = read_text(path)
            if "context7" in text and "CONTEXT7_API_KEY" in text:
                found_context7 = True
                break
    if not found_context7:
        add_finding(
            findings,
            "missing_context7_runtime_config",
            ROOT / "tools" / "governance" / "audit-compliance.py",
            "Context7 runtime configuration was not found in user/global MCP configs.",
            "Configure Context7 in OpenCode, Copilot, and Antigravity MCP config files.",
        )
    if not os.environ.get("CONTEXT7_API_KEY"):
        add_finding(
            findings,
            "missing_context7_env",
            ROOT / "tools" / "governance" / "audit-compliance.py",
            "CONTEXT7_API_KEY user environment variable is not available in the current process.",
            "Set CONTEXT7_API_KEY at user level and restart tool sessions.",
        )


def count_findings(findings, keys):
    return sum(len(findings.get(key, [])) for key in keys)


def score_from_findings(findings):
    critical_keys = {
        "missing_preflight_gate",
        "skill_frontmatter",
        "broken_refs",
        "missing_commit_policy",
    }
    major_keys = {
        "missing_final_gate",
        "missing_orchestration",
        "missing_dag_reference",
        "missing_context7_policy",
        "missing_tasks_governance",
        "missing_mcp_consent",
        "missing_skill_routing",
        "incomplete_mcp_search",
        "missing_java_multi_agent_runtime",
        "missing_context7_runtime_config",
        "missing_context7_env",
        "missing_copilot_cli_contract",
        "missing_copilot_cli_skill_layer",
        "missing_copilot_cli_skill_mirror",
        "missing_global_copilot_cli_skill",
        "tasks_lessons_template_drift",
        "tasks_todo_template_drift",
        "tasks_placeholder_content",
    }
    critical = count_findings(findings, critical_keys)
    major = count_findings(findings, major_keys)
    minor = 0
    if critical == 0 and major == 0 and minor == 0:
        return 100, critical, major, minor
    score = max(0, 100 - (critical * 12 + major * 5 + minor * 2))
    if critical > 0 and score == 100:
        score = 99
    return score, critical, major, minor


def emit_report(files_checked, findings, score_tuple):
    score, critical, major, minor = score_tuple
    lines = [
        "# Compliance Report",
        "",
        f"- Score: **{score}/100**",
        f"- Files checked: **{files_checked}**",
        f"- Critical findings: **{critical}**",
        f"- Major findings: **{major}**",
        f"- Minor findings: **{minor}**",
        "",
        "## Detailed Findings",
        "",
    ]
    if not any(findings.values()):
        lines.append("- No findings detected.")
    else:
        ordered = [
            "missing_preflight_gate",
            "missing_commit_policy",
            "skill_frontmatter",
            "broken_refs",
            "missing_final_gate",
            "missing_orchestration",
            "missing_dag_reference",
            "missing_context7_policy",
            "missing_tasks_governance",
            "missing_mcp_consent",
            "incomplete_mcp_search",
            "missing_copilot_cli_contract",
            "missing_copilot_cli_skill_layer",
            "missing_copilot_cli_skill_mirror",
            "missing_global_copilot_cli_skill",
            "tasks_lessons_template_drift",
            "tasks_todo_template_drift",
            "tasks_placeholder_content",
            "missing_java_multi_agent_runtime",
            "missing_context7_runtime_config",
            "missing_context7_env",
            "missing_skill_routing",
        ]
        for category in ordered:
            items = findings.get(category, [])
            if not items:
                continue
            lines.append(f"### {category}")
            for item in items:
                lines.append(
                    f"- `{item['path']}` - {item['reason']} | Suggested fix: {item['fix']}"
                )
            lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    return score


def main():
    parser = argparse.ArgumentParser(description="Governance compliance audit")
    parser.add_argument(
        "--strict", action="store_true", help="Exit with code 1 when any finding exists"
    )
    args = parser.parse_args()

    files = collect(MANDATORY_PATTERNS)
    references = collect(REFERENCE_PATTERNS)
    findings = {}

    check_core_contracts(files, findings)
    check_reference_integrity(references, findings)
    check_skill_routing(findings)
    check_java_multi_agent_contract(findings)
    check_copilot_cli_skill_mirrors(findings)
    check_global_copilot_cli_skills(findings)
    check_user_mcp_runtime(findings)
    check_tasks_files(findings)

    score_tuple = score_from_findings(findings)
    score = emit_report(len(files), findings, score_tuple)
    print(score)

    if args.strict and any(findings.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
