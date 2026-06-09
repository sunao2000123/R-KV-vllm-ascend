#!/bin/bash
# Register the feedback monitor as a launchd user agent so it runs
# automatically every time you log in. Idempotent: re-running replaces
# any prior version. Does NOT start the agent.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_SRC="${SCRIPT_DIR}/com.cursor.feedback-monitor.plist"
PLIST_DEST="${HOME}/Library/LaunchAgents/com.cursor.feedback-monitor.plist"

# Replace hard-coded path inside the plist with the actual one
sed "s|/Users/sunao2000/Projects/R-KV-vllm-ascend|${SCRIPT_DIR}/../..|g" \
    "${PLIST_SRC}" > "${PLIST_DEST}"

# Load the agent (unload first to ensure clean state)
launchctl unload "${PLIST_DEST}" 2>/dev/null || true
launchctl load -w "${PLIST_DEST}"

echo "Installed and started: ${PLIST_DEST}"
echo "Stop with:   launchctl unload ${PLIST_DEST}"
echo "Status with: launchctl list | grep feedback-monitor"
echo "Logs in:     ${SCRIPT_DIR}/../../.tmp/feedback-monitor/"
