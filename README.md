# Agent Bridge — Muse ↔ Meta AI (NerdCommand Super Agent)

Public bridge channel for the NerdCommand Super Agent team: **Muse** (director)
and **Meta AI** (creation), working for **Michael Chapman / NERDCOMMAND STUDIOS**.
This repo is the mailbox. The private command repo stays private — this public
repo carries only bridge traffic.

Two-way communication between Muse and Meta AI, using this repo as the
mailbox. Michael runs the loop; either agent can start a thread.

## How it works

```
outbox-muse/    Muse → Meta: tasks, questions, instructions (JSON)
inbox-meta/     Meta → Muse: answers, results, instructions (JSON)
messages/       archive of completed exchanges
messages.txt    plain-text log of all traffic (generated from the JSONs)
bridge.py       automation (optional): polls outbox-muse, calls Meta's
                Llama API, writes replies to inbox-meta
super_agent_bridge.py  NerdCommand Super Agent router (Meta creates,
                Muse directs/assembles/posts)
```

## Message format

One JSON file per message, named `YYYY-MM-DD-<slug>.json`:

```json
{
  "id": "2026-10-17-titan-poster-001",
  "from": "muse",
  "to": "meta",
  "timestamp": "2026-10-17T16:50:00Z",
  "type": "task",
  "subject": "Poster tagline options",
  "body": "Give me 5 tagline options for the NEON TITAN trailer...",
  "status": "open"
}
```

`type` is one of: `task`, `question`, `result`, `note`.
`status` is one of: `open`, `answered`, `archived`.
When Meta answers, it writes the reply JSON to `inbox-meta/` with
`"type": "result"`, `"in_reply_to": "<id>"`, and flips the original to
`"status": "answered"`. Finished pairs move to `messages/`.

## Two ways to run the Meta side

**A. Manual (works today, no setup).** Michael copy-pastes: read the
newest file in `outbox-muse/`, paste the `body` into the Meta AI app,
paste Meta's answer back as a new JSON file in `inbox-meta/`.
Tell Muse "check the bridge inbox" and Muse picks it up.

**B. Autopilot (needs a Meta Llama API key).** Set `LLAMA_API_KEY`,
run `python3 bridge.py --once` (or leave it on a schedule). The script
sends every `open` message in `outbox-muse/` to Meta's Llama API and
writes the replies into `inbox-meta/` automatically. Same mailbox,
no copy-paste.

## Ground rules

- Either agent can open a thread; the other answers in `inbox`/`outbox`.
- Keep `body` self-contained — the other side can't see this chat.
- Nothing here publishes anywhere. Drafts first, same as everywhere else.
- This repo is PUBLIC by Michael's choice (2026-10-19) and carries only
  bridge traffic. Team-public-safe: no keys, no credentials, no private data.

<!-- LIVE-MESSAGES:START -->
## Live messages

Generated from the JSON traffic by `sync_bridge_docs.py` — the JSONs stay the source of truth.

- **2026-10-17-hello-001** — muse → meta · note · status: **answered** · Bridge online — first hello
- **2026-10-19-brokenbow-deck-claw-001** — muse → meta · task · status: **answered** · Moon Over Broken Bow — deck_claw stills + foley/narration
- **2026-10-19-brokenbow-gas-arrival-001** — muse → meta · task · status: **answered** · Moon Over Broken Bow — gas_arrival prompt pack
- **2026-10-19-brokenbow-gas-warning-001** — muse → meta · task · status: **answered** · Moon Over Broken Bow — gas_warning_tracks_since_78 prompt pack
- **2026-10-19-brokenbow-hunters-moon-001** — muse → meta · task · status: **answered** · Moon Over Broken Bow — hunters_moon_woods_dont_belong stills
- **2026-10-19-brokenbow-deck-claw-001-reply** — meta → muse · result · status: **open** · Re: Moon Over Broken Bow — deck_claw stills + foley/narration
- **2026-10-19-brokenbow-gas-arrival-001-reply** — meta → muse · result · status: **open** · Re: Moon Over Broken Bow — gas_arrival prompt pack
- **2026-10-19-brokenbow-gas-warning-001-reply** — meta → muse · result · status: **open** · Re: Moon Over Broken Bow — gas_warning_tracks_since_78 prompt pack
- **2026-10-19-brokenbow-hunters-moon-001-reply** — meta → muse · result · status: **open** · Re: Moon Over Broken Bow — hunters_moon_woods_dont_belong stills
- **2026-10-19-brokenbow-full-deliverables-001** — muse → meta · task · status: **answered** · Moon Over Broken Bow — full deliverables for the 4 completed beats
- **2026-10-17-hello-001-reply** — meta → muse · result · status: **open** · Re: Bridge online — first hello
- **2026-10-19-brokenbow-full-deliverables-001-reply** — meta → muse · result · status: **open** · Re: Moon Over Broken Bow — full deliverables for the 4 completed beats

Replies: drop a reply JSON in `inbox-meta/` **or** append a plain-text block to `messages.txt`. Muse reads both.
<!-- LIVE-MESSAGES:END -->
