#!/usr/bin/env python3
"""Feedback monitor daemon for sunao2000123/R-KV-vllm-ascend.

Polls a designated GitHub Issue's comments every POLL_INTERVAL seconds,
uses the gh-issue-comment-monitor skill's checkpoint pattern to advance
local state, and emits a machine-readable updates JSON for an AI agent
(or a human) to consume.

This daemon:
- Never writes to GitHub (read-only monitor)
- Uses `gh api` exclusively (token stays in macOS keychain)
- Maintains a local checkpoint under .tmp/feedback-monitor/
- Calls get_latest_comments.py from the bundled skill for the heavy lifting
- Logs to .tmp/feedback-monitor/monitor.log

Usage:
    python monitor_daemon.py --repo sunao2000123/R-KV-vllm-ascend --issue 1
    python monitor_daemon.py --once    # single check, then exit
    python monitor_daemon.py --status  # show last-checked info
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


POLL_INTERVAL = int(os.environ.get("FEEDBACK_MONITOR_POLL", "30"))
SKILL_DIR_GUESS = [
    Path(__file__).resolve().parent.parent.parent
    / ".cursor"
    / "skills"
    / "gh-issue-comment-monitor",
    Path.home() / ".cursor" / "skills-cursor" / "gh-issue-comment-monitor",
]
STATE_DIR = Path(".tmp/feedback-monitor")
STATE_FILE = STATE_DIR / "checkpoint.json"
UPDATES_FILE = STATE_DIR / "updates.json"
LOG_FILE = STATE_DIR / "monitor.log"


def log(msg: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}", flush=True)


def find_skill_dir() -> Path:
    for cand in SKILL_DIR_GUESS:
        if (cand / "scripts" / "get_latest_comments.py").exists():
            return cand
    raise FileNotFoundError(
        "Could not find gh-issue-comment-monitor skill. "
        f"Searched: {[str(p) for p in SKILL_DIR_GUESS]}"
    )


def check_gh_auth() -> bool:
    if not shutil.which("gh"):
        log("ERROR: `gh` CLI not on PATH. Install via `brew install gh` then `gh auth login`.")
        return False
    r = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True, text=True, timeout=10,
    )
    if r.returncode != 0:
        log(f"ERROR: gh not authenticated. {r.stderr.strip()}")
        return False
    return True


def run_skill_fetch(skill_dir: Path, repo: str, issue: int) -> dict:
    """Invoke get_latest_comments.py with checkpoint handling.

    Returns the parsed JSON result from the skill.
    """
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        "python3",
        str(skill_dir / "scripts" / "get_latest_comments.py"),
        "--repo", repo,
        "--issue", str(issue),
        "--state-file", str(STATE_FILE),
        "--updates-file", str(UPDATES_FILE),
        "--limit", "5",
        "--update-state",
    ]
    log(f"running: {' '.join(cmd)}")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        log(f"skill fetch failed (exit={r.returncode}): {r.stderr.strip()[:500]}")
        return {"ok": False, "error": r.stderr.strip()}

    updates_path = Path(UPDATES_FILE)
    if not updates_path.exists():
        return {"ok": True, "comments": []}
    try:
        return json.loads(updates_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        log(f"updates JSON decode error: {exc}")
        return {"ok": False, "error": str(exc)}


def notify_new_comments(comments: list, repo: str, issue: int) -> None:
    """Hook for downstream consumers (e.g., trigger Codex).

    The default implementation just logs. An AI agent can either:
    - tail LOG_FILE and react to `NEW_COMMENT` lines
    - poll UPDATES_FILE from another process
    - replace this function with macOS `osascript` notification
    """
    for c in comments:
        author = c.get("author") or c.get("user", {}).get("login", "?")
        cid = c.get("id") or c.get("comment_id", "?")
        url = c.get("url") or c.get("html_url", "")
        body_preview = (c.get("body") or "")[:200].replace("\n", " ")
        log(f"NEW_COMMENT repo={repo} issue={issue} id={cid} author={author} url={url}")
        log(f"  body_preview: {body_preview}")


def do_one_check(skill_dir: Path, repo: str, issue: int) -> dict:
    result = run_skill_fetch(skill_dir, repo, issue)
    if not result.get("ok"):
        return result
    comments = result.get("comments") or result.get("new_comments") or []
    if comments:
        log(f"detected {len(comments)} new comment(s)")
        notify_new_comments(comments, repo, issue)
    else:
        log("no new comments")
    return result


def cmd_status() -> int:
    if not STATE_FILE.exists():
        print(json.dumps({"ok": True, "state_file_exists": False}, ensure_ascii=False, indent=2))
        return 0
    print(STATE_FILE.read_text(encoding="utf-8"))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="sunao2000123/R-KV-vllm-ascend")
    ap.add_argument("--issue", type=int, required=False)
    ap.add_argument("--once", action="store_true", help="single check, then exit")
    ap.add_argument("--status", action="store_true", help="print last checkpoint and exit")
    ap.add_argument("--dry-run", action="store_true", help="skip actual fetch (sanity)")
    args = ap.parse_args()

    if args.status:
        return cmd_status()
    if not args.issue:
        log("ERROR: --issue NUMBER is required (the GitHub Issue number to monitor).")
        return 2
    if not check_gh_auth():
        return 3
    skill_dir = find_skill_dir()
    log(f"using skill: {skill_dir}")

    if args.once:
        if args.dry_run:
            log("dry-run, skipping fetch")
            return 0
        result = do_one_check(skill_dir, args.repo, args.issue)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    log(f"starting daemon (repo={args.repo} issue={args.issue} interval={POLL_INTERVAL}s)")
    while True:
        try:
            do_one_check(skill_dir, args.repo, args.issue)
        except Exception as exc:
            log(f"unhandled exception: {exc!r}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    sys.exit(main())
