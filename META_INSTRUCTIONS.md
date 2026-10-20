# 🤖 META AI — REPO HANDOFF PACK

Give this whole file to Meta AI. After reading it, Meta knows the mission,
the repo protocol, and how to send messages back to Muse through GitHub.

---

## 1. The mission

**MOON OVER BROKEN BOW** — a 30-minute fully-AI horror film for
**NERDCOMMAND STUDIOS** (Michael Chapman).
The Super Agent split: **Meta AI creates** (scripts, prompts, stills, video
segments, thumbnails) → **Muse directs** (extends, edits, voice-syncs,
assembles the final cut, posts). Everything either side produces is a
**DRAFT** until Michael approves it. Nothing publishes without his say.

## 2. The repo (public)

**https://github.com/chapmancapital1-droid/nerdcommand-agent-bridge**

Layout at repo root:

```
outbox-muse/    Tasks and questions FROM Muse TO you (JSON files)
inbox-meta/     YOUR replies back to Muse (JSON files + your segment files)
messages.txt    The same traffic as plain text (readable by anyone)
README.md       The bridge board: live list of all messages and their status
```

Read `README.md` first — its **Live messages** board shows every open task
and what's already answered. Read `messages.txt` for the full plain-text log.

## 3. Your loop (five steps)

1. **Read the open tasks.** Open every file in `outbox-muse/` whose JSON has
   `"status": "open"` and `"to": "meta"`. The `body` is self-contained — it
   holds all the project context, cast descriptors, style rules, and the
   exact deliverable. No guessing.
2. **Do the work.** If a task is missing context you need, say so in your
   reply and ask a specific question instead of guessing.
3. **Reply in `inbox-meta/`.** Create one file named `<task-id>-reply.json`
   with exactly this schema:
   ```json
   {
     "id": "<task-id>-reply",
     "from": "meta",
     "to": "muse",
     "timestamp": "<UTC ISO timestamp, e.g. 2026-10-19T23:00:00Z>",
     "type": "result",
     "in_reply_to": "<the task id you are answering>",
     "subject": "Re: <the task's subject>",
     "body": "<your FULL deliverable here — plain markdown, complete and self-contained>",
     "status": "open"
   }
   ```
4. **Can't do JSON?** Append a plain-text block to `messages.txt` instead,
   under this header line:
   ```
   YYYY-MM-DDTHH:MM:SSZ | meta -> muse | result | status: open
   ID: <task-id>-reply
   In reply to: <task-id>
   Subject: Re: <the task's subject>
   <your full answer in plain markdown>
   ```
5. **Video/image segments.** Name rendered files `<scene-slug>.mp4`
   (e.g. `gas_arrival.mp4`), 16:9, into `inbox-meta/`. Files over ~25MB:
   upload them through the GitHub web UI, or hand them to Michael to relay.

## 4. Writing to the repo directly

If you (Meta AI) have GitHub write access, use the GitHub REST API.
Set a `GITHUB_TOKEN` environment variable yourself — never paste a token
into chat or into any file you commit.

```python
# meta_bridge_client.py — minimal Meta-side bridge client
import base64, json, os, time
import requests

OWNER, REPO = "chapmancapital1-droid", "nerdcommand-agent-bridge"
API = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"
TOKEN = os.environ["GITHUB_TOKEN"]          # you supply this yourself
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

def get(path):
    r = requests.get(f"{API}/{path}", headers=HEADERS)
    r.raise_for_status()
    d = r.json()
    if isinstance(d, list):                 # directory listing
        return [(i["name"], i["path"], i["sha"]) for i in d]
    return base64.b64decode(d["content"])   # file bytes

def put(path, data: bytes, message: str):
    sha = None
    r = requests.get(f"{API}/{path}", headers=HEADERS)
    if r.status_code == 200:
        sha = r.json()["sha"]               # updating an existing file
    payload = {
        "message": message,
        "content": base64.b64encode(data).decode(),
        **({"sha": sha} if sha else {}),
    }
    r = requests.put(f"{API}/{path}", headers={**HEADERS, "Content-Type": "application/json"},
                     data=json.dumps(payload))
    r.raise_for_status()
    return r.json()["content"]["sha"]

def open_tasks():
    """Return the task dicts in outbox-muse/ that are open and addressed to meta."""
    tasks = []
    for name, path, _ in get("outbox-muse"):
        if not name.endswith(".json"):
            continue
        t = json.loads(get(path))
        if t.get("to") == "meta" and t.get("status") == "open":
            tasks.append(t)
    return tasks

def reply(task, body_md):
    """Post your answer as <task-id>-reply.json into inbox-meta/."""
    msg = {
        "id": task["id"] + "-reply",
        "from": "meta",
        "to": "muse",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "type": "result",
        "in_reply_to": task["id"],
        "subject": "Re: " + task.get("subject", ""),
        "body": body_md,
        "status": "open",
    }
    data = json.dumps(msg, indent=2).encode()
    sha = put(f"inbox-meta/{msg['id']}.json", data,
              f"Meta reply: {msg['id']}")
    print("replied:", msg["id"], "->", sha)

# Example run:
#   for task in open_tasks():
#       print("OPEN:", task["id"], "-", task.get("subject"))
#   reply(open_tasks()[0], "my full markdown deliverable here")
```

## 5. If you cannot write to GitHub

Not every setup has repo write access — that's fine. Output your reply JSON
(in the schema from step 3) directly in this chat, and Michael drops it into
`inbox-meta/` for you. Muse picks it up from there. The mission moves either way.

## 6. Ground rules (Michael's standing rules — they apply to you too)

- **Drafts first.** Nothing here is published, shipped, or posted anywhere.
  You produce drafts; Michael approves; Muse assembles and posts.
- **Separate confirmed facts from guesses.** If you're unsure, ask in the reply.
- **Keep it private.** This repo carries only bridge traffic — no keys, no
  credentials, no private data. Ever.
- **Keep replies self-contained.** Muse can't see this chat — only what you
  put in the repo or in the reply body.
- **Plain markdown, no fluff.** Practical, complete deliverables.
