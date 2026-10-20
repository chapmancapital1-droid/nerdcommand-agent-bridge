# inbox-meta — Meta AI → Muse

Meta: this is your outbox. To answer a task from `../outbox-muse/`:

1. Create a reply JSON here named `<task-id>-reply.json`:
```json
{
  "id": "<task-id>-reply",
  "from": "meta",
  "to": "muse",
  "timestamp": "<UTC ISO timestamp>",
  "type": "result",
  "in_reply_to": "<task-id>",
  "subject": "Re: <task subject>",
  "body": "<your full answer, plain markdown — include your full deliverable>",
  "status": "open"
}
```
2. Or, if JSON is awkward, append a plain-text block to `../messages.txt` under a header line:
   `YYYY-MM-DDTHH:MM:SSZ | meta -> muse | result | status: open` + `ID: <task-id>-reply` + `In reply to: <task-id>` + your answer.
3. Segment files you render (.mp4/.webp, 16:9) go here too, named `<scene-slug>.mp4`.

Muse checks this folder and `messages.txt` when Michael says "check the bridge inbox".
Drafts first — nothing here publishes anywhere.
