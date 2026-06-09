# Feedback Monitor

A read-only daemon that polls a designated GitHub Issue's comments and surfaces
new ones for an AI agent (or a human) to act on. Designed to bridge the gap
between a remote machine (where you actually run tests) and an AI assistant
(which cannot reach that machine).

## Why it exists

`xj-zhang2018/R-KV-vllm-ascend` has a "Codex 自动化测试反馈监控" issue that
the original owner uses to receive automated test feedback. This fork
(`sunao2000123/R-KV-vllm-ascend`) wants to run the same loop in a
self-contained way: error on server → paste to issue → AI pulls comment →
AI fixes code → push → server `git pull` → re-run.

## Components

| File | Role |
|---|---|
| `monitor_daemon.py` | Long-running poller. Calls the bundled `gh-issue-comment-monitor` skill for the heavy lifting, maintains a local checkpoint, and emits a log line per new comment. |
| `run_once.sh` | One-shot wrapper around the daemon. Useful for cron or manual triggering. |
| `com.cursor.feedback-monitor.plist` | launchd config template. |
| `install_launchd.sh` | Idempotently install + load the launchd agent (runs on login, restarts on crash). |
| `uninstall_launchd.sh` | Stop and remove the launchd agent. |

State files live under `.tmp/feedback-monitor/` (gitignored):

| File | Content |
|---|---|
| `checkpoint.json` | Last-seen comment id / author / time. Written by `--update-state`. |
| `updates.json` | Newest comments since checkpoint. Overwritten on every poll. |
| `monitor.log` | Human-readable log, one line per poll + one `NEW_COMMENT` line per new comment. |
| `launchd.out.log` / `launchd.err.log` | launchd stdout / stderr. |

## Prerequisites

1. `gh` CLI authenticated:
   ```bash
   brew install gh
   gh auth login
   ```
2. The `gh-issue-comment-monitor` skill installed (it's bundled in
   `.cursor/skills/` of this repo AND/OR `~/.cursor/skills-cursor/`).
3. A GitHub Issue created in `sunao2000123/R-KV-vllm-ascend` with title
   `Codex 自动化测试反馈监控` (do this once in the GitHub web UI).

## Quick start

```bash
# 1. Install launchd agent (runs forever, restarts on crash)
./tools/feedback-monitor/install_launchd.sh

# 2. Verify
launchctl list | grep feedback-monitor
tail -f .tmp/feedback-monitor/monitor.log

# 3. Trigger a one-shot check
./tools/feedback-monitor/run_once.sh

# 4. Stop
./tools/feedback-monitor/uninstall_launchd.sh
```

## How an AI agent should consume this

Three options, pick the one that fits your flow:

1. **Tail the log** for `NEW_COMMENT` lines. Each line contains the comment
   id, author, URL, and a 200-char body preview. The full body lives in
   `.tmp/feedback-monitor/updates.json`.
2. **Poll `.tmp/feedback-monitor/updates.json`** from a separate process.
   It's overwritten on every poll, so diff vs. the previous read.
3. **Run the daemon `--once` from a CI / dev script** when you want
   synchronous check-then-act behavior.

## Design notes

- **Read-only with respect to GitHub**: the daemon never posts comments,
  edits issues, or modifies state. It only reads.
- **Token safety**: Uses `gh` CLI exclusively, which stores the PAT in
  the macOS keychain. No `GITHUB_TOKEN` env var is ever set; no token
  appears in `.git/config` or any log line.
- **Crash-safe**: launchd's `KeepAlive.Crashed = true` restarts the
  daemon on a crash. The skill's checkpoint ensures no comment is missed
  across restarts.
- **Project-scoped**: The script only knows about this repository's
  `.tmp/` directory. It does not touch global state.
