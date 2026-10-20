#!/usr/bin/env python3
"""Regenerate messages.txt + the README 'Live messages' board from the bridge JSONs.

The JSONs in outbox-muse/ and inbox-meta/ are the machine format (the source of
truth). messages.txt is the same traffic in plain text, and the README board is
a glanceable summary — both are generated here so they never drift from the JSONs.

Usage: python3 sync_bridge_docs.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTBOX = HERE / "outbox-muse"
INBOX = HERE / "inbox-meta"
README = HERE / "README.md"
TXT_LOG = HERE / "messages.txt"
MARKER_START = "<!-- LIVE-MESSAGES:START -->"
MARKER_END = "<!-- LIVE-MESSAGES:END -->"


def load_msgs(folder):
    msgs = []
    if folder.exists():
        for f in sorted(folder.glob("*.json")):
            try:
                msgs.append(json.loads(f.read_text()))
            except Exception as e:
                print(f"skip {f.name}: {e}")
    return msgs


def render_txt(msgs):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "AGENT BRIDGE — MESSAGE LOG",
        "Plain-text mirror of the bridge traffic. The JSON files in",
        "outbox-muse/ and inbox-meta/ are the machine format and the",
        "source of truth; this log is generated from them by",
        "sync_bridge_docs.py. Either agent may also append a block here",
        "in plain text — Muse reads both.",
        f"Generated: {now}",
        "",
    ]
    for m in msgs:
        lines += [
            "=" * 60,
            f"{m.get('timestamp','?')} | {m.get('from','?')} -> {m.get('to','?')} "
            f"| {m.get('type','?')} | status: {m.get('status','?')}",
            f"ID: {m.get('id','?')}",
            f"Subject: {m.get('subject','')}",
        ]
        if m.get("in_reply_to"):
            lines.append(f"In reply to: {m['in_reply_to']}")
        lines += ["-" * 60, m.get("body", ""), ""]
    return "\n".join(lines)


def render_board(msgs):
    rows = ["## Live messages", "",
            "Generated from the JSON traffic by `sync_bridge_docs.py` — the JSONs stay the source of truth.",
            ""]
    if not msgs:
        rows.append("_No messages yet._")
    for m in msgs:
        rows.append(f"- **{m.get('id','?')}** — {m.get('from','?')} → {m.get('to','?')} · {m.get('type','?')} · "
                    f"status: **{m.get('status','?')}** · {m.get('subject','')}")
    rows += ["", "Replies: drop a reply JSON in `inbox-meta/` **or** append a plain-text block to `messages.txt`. Muse reads both."]
    return "\n".join(rows)


def main():
    msgs = load_msgs(OUTBOX) + load_msgs(INBOX)
    msgs.sort(key=lambda m: m.get("timestamp", ""))
    TXT_LOG.write_text(render_txt(msgs))
    board = render_board(msgs)
    readme = README.read_text()
    if MARKER_START in readme and MARKER_END in readme:
        head, rest = readme.split(MARKER_START, 1)
        _, tail = rest.split(MARKER_END, 1)
        readme = head + MARKER_START + "\n" + board + "\n" + MARKER_END + tail
    else:
        readme = readme.rstrip() + "\n\n" + MARKER_START + "\n" + board + "\n" + MARKER_END + "\n"
    README.write_text(readme)
    print(f"wrote messages.txt + README board from {len(msgs)} message(s)")


if __name__ == "__main__":
    main()
