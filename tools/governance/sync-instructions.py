import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DAG_MANIFEST = ROOT / "tools" / "governance" / "instruction-sync-manifest.json"
DAG_HINT = "- For non-trivial tasks, instantiate the `Template DAG 100% compliance` from `orchestrate-multi-agents`; owners/tasks may be reduced only when not applicable, but mandatory gates cannot be removed."
HEADER = "## Mandatory multi-agent orchestration skill"


def load_targets() -> list[Path]:
    data = json.loads(DAG_MANIFEST.read_text(encoding="utf-8"))
    targets: list[Path] = []
    for raw in data.get("targets", []):
        path = (ROOT / raw).resolve()
        if ROOT not in path.parents and path != ROOT:
            raise ValueError(f"target outside repo root: {raw}")
        targets.append(path)
    return targets


for path in load_targets():
    if not path.exists() or not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    if HEADER not in text or DAG_HINT in text:
        continue
    start = text.find(HEADER)
    end = text.find("\n## ", start + 1)
    if end == -1:
        block = text[start:].rstrip() + "\n" + DAG_HINT + "\n"
        updated = text[:start] + block
    else:
        block = text[start:end].rstrip() + "\n" + DAG_HINT + "\n"
        updated = text[:start] + block + text[end:]
    path.write_text(updated, encoding="utf-8")

print("ok")
