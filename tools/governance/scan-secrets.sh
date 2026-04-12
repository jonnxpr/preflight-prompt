#!/usr/bin/env bash

set -euo pipefail

update_baseline=false
fail_on_leaks=false

for arg in "$@"; do
  case "$arg" in
    --update-baseline)
      update_baseline=true
      ;;
    --fail-on-leaks)
      fail_on_leaks=true
      ;;
    *)
      printf 'Unknown argument: %s\n' "$arg" >&2
      exit 2
      ;;
  esac
done

mkdir -p tasks .governance

report="tasks/secret-scan.sarif"
baseline=".governance/gitleaks-baseline.json"

if ! command -v gitleaks >/dev/null 2>&1; then
  printf '%s\n' 'gitleaks not found in current shell. Secret scan skipped.' >&2
  printf '%s\n' 'Secret scan skipped: gitleaks not available in current shell.' > "$report"
  exit 0
fi

scan_mode_args=(detect --source . --redact --report-format sarif --report-path "$report")
baseline_mode_args=(detect --source . --redact --report-format json --report-path "$baseline" --exit-code 0)

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  scan_mode_args+=(--no-git)
  baseline_mode_args+=(--no-git)
fi

if [[ "$fail_on_leaks" == false ]]; then
  scan_mode_args+=(--exit-code 0)
fi

if [[ "$update_baseline" == true ]]; then
  gitleaks "${baseline_mode_args[@]}"
  printf 'Updated baseline: %s\n' "$baseline"
  exit 0
fi

if [[ -f "$baseline" ]]; then
  scan_mode_args+=(--baseline-path "$baseline")
fi

gitleaks "${scan_mode_args[@]}"
printf 'Report: %s\n' "$report"
