#!/bin/bash
# Unregister the feedback monitor launchd agent.
set -euo pipefail
PLIST_DEST="${HOME}/Library/LaunchAgents/com.cursor.feedback-monitor.plist"
launchctl unload "${PLIST_DEST}" 2>/dev/null || true
rm -f "${PLIST_DEST}"
echo "Uninstalled: ${PLIST_DEST}"
