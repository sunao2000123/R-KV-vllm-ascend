#!/bin/bash
# Single-shot monitor run. Useful for cron, manual triggering, or testing.
# Usage: ./run_once.sh [REPO] [ISSUE_NUMBER]
#        REPO defaults to sunao2000123/R-KV-vllm-ascend
#        ISSUE_NUMBER defaults to 1

set -euo pipefail

REPO="${1:-sunao2000123/R-KV-vllm-ascend}"
ISSUE="${2:-1}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}/../.."

exec python3 "${SCRIPT_DIR}/monitor_daemon.py" --repo "${REPO}" --issue "${ISSUE}" --once
