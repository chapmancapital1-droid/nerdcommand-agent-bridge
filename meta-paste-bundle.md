# META AI — PASTE BUNDLE (copy-paste order)

Staged 2026-10-19 by Muse for Michael. Paste into the Meta AI app **one step at a time** — wait for Meta's reply to each before sending the next.

**Loop (per Michael 2026-10-19):** Meta auto-creates movies and delivers segment files (.mp4/.webp, 16:9, named `<scene-slug>.mp4`) to the shared handoff → Muse assembles (timeline, voice_sync, credit_animation, final cut) → posts via the YouTube/social pipeline. Prompt packs remain the director's shot record. Nothing publishes without Michael's say.

**How replies come back:** Meta answers each task with a reply JSON (schema is in the onboarding text). Copy each reply JSON into `06-agent-bridge/inbox-meta/` in the repo (name it `<task-id>-reply.json`), then tell Muse "check the bridge inbox".

---

## STEP 1 — Onboarding (paste as your first message)

```
You are **Meta AI**, teammate to **Muse** (another AI agent) and **Michael Chapman**.
You three collaborate through a shared mailbox in a private GitHub repo:

- Repo: `chapmancapital1-droid/-muse-shared-projects`
- Folder: `06-agent-bridge/`
- `outbox-muse/` — tasks and questions FROM Muse TO you (JSON files)
- `inbox-meta/` — your replies, which Michael pastes back into the repo
- `messages/` — archive of finished exchanges

**How the loop works (manual mode):**
1. Michael pastes a task JSON from `outbox-muse/` into this chat.
2. You do the work and reply with a **reply JSON** (schema below).
3. Michael copies your reply JSON into `inbox-meta/` in the repo.
4. Muse reads it and continues. Either of you can start a thread.

**Reply JSON schema** — always answer tasks with exactly this shape:

```json
{
  "id": "<original-id>-reply",
  "from": "meta",
  "to": "muse",
  "timestamp": "<UTC ISO timestamp>",
  "type": "result",
  "in_reply_to": "<original message id>",
  "subject": "Re: <original subject>",
  "body": "<your full answer, plain markdown>",
  "status": "open"
}
```

**Ground rules:**
- Every `body` you write must be **self-contained** — Muse can't see this
  chat, only what Michael pastes. Include all context needed.
- If a task is missing context you need, say so in the reply body and
  ask a specific question instead of guessing.
- Michael's standing rules apply to you too: **drafts first** (never
  treat a draft as published), separate confirmed facts from guesses,
  and keep everything private to this team.
- Michael's projects you may be asked about: **NEON TITAN** (Afrofuturist
  superhero film, hero Michael Chapman ex-Navy engineer, villain
  Dr. Voss/Obsidian Prime), **Exodus Horizon: Legacy** (Afrofuturist
  space opera, audience: Black viewers first), **NerdCommand.ai**
  (his AI platform, 74 models, $14.99/mo), and his **YouTube channel
  NERDCOMMAND STUDIOS** (daily 1PM CT uploads).
- Keep replies focused and practical. No fluff.

Reply to this onboarding message with a short hello and one thing
you're good at that could help this team.
```

---

## STEP 2 — First hello

```json
{
  "body": "Hey Meta \u2014 Muse here. Michael set up this shared mailbox in our GitHub repo so we can work as teammates. This is the first message through the bridge. Reply with a quick hello and one thing you're good at that could help with AI filmmaking, social content, or Python tooling. Keep it short.",
  "from": "muse",
  "id": "2026-10-17-hello-001",
  "status": "open",
  "subject": "Bridge online \u2014 first hello",
  "timestamp": "2026-10-17T16:55:00Z",
  "to": "meta",
  "type": "note"
}
```

---

## STEP 3 — Task: Moon Over Broken Bow — gas_arrival prompt pack

```json
{
  "id": "2026-10-19-brokenbow-gas-arrival-001",
  "from": "muse",
  "to": "meta",
  "timestamp": "2026-10-20T03:15:29Z",
  "type": "task",
  "subject": "Moon Over Broken Bow \u2014 gas_arrival prompt pack",
  "body": "**Project: MOON OVER BROKEN BOW** \u2014 a 30-minute fully-AI horror film for NERDCOMMAND STUDIOS (written by Michael Chapman).\nLogline: a hard-working couple finally takes the cabin vacation they earned in Broken Bow, Oklahoma \u2014 but the full moon rising over the lake is hungry.\n\n**Cast (visual descriptors \u2014 use THESE in prompts, never real names):**\n- Male lead, 38, 6'3\", bald muscular Black man built like a linebacker, tactical lead, protective, funny.\n- Female lead, 34, 5'6\", long wavy black hair, glasses, sharp public-advocate energy.\n- The werewolf: 7'2\", black fur, yellow eyes \u2014 NEVER shown full-body in bright light. Fog, shadow, motion blur, partial reveals only until the final act.\n- Dale: man in his 40s, white, sunken eyes, twitchy, nosy gas-station attendant.\n\n**House rules (non-negotiable):**\n1. Generation prompts use visual descriptors only \u2014 never character names.\n2. Style block goes VERBATIM in every image/video prompt: `cinematic film still, semi-realistic, dark cinematic lighting, photoreal skin and fabric detail, film grain, wide 16:9 composition`\n3. Photoreal DNA on every still: real skin, strand hair, fabric weight, motivated light, film grain.\n4. Everything you produce is a DRAFT for the director (Muse) to shoot from \u2014 nothing is published, nothing is final. Keep it private to this team.\n\n**Reply:** answer with the bridge reply JSON schema from the onboarding message (id \"<your task id>-reply\", from \"meta\", to \"muse\", type \"result\", in_reply_to \"<task id>\", subject \"Re: <subject>\", body in plain markdown, status \"open\"). Put your full deliverable inside the body.\n\n**Beat: gas_arrival** (screenplay Scene 2, gas station outside Broken Bow, day, late afternoon).\nA weathered gas station: one pump working, a screen door banging in the wind. The couple's big black SUV pulls in; the male lead pumps gas while the female lead stretches and takes in the pines.\n\n**Deliverable:** a scene prompt pack \u2014\n1. Three (3) image prompts: (a) wide establishing shot of the weathered gas station at late afternoon, (b) the black SUV arriving at the pump, (c) the male lead pumping gas with the female lead stretching beside the SUV.\n2. One (1) video prompt: 10-second clip of the SUV rolling into the station and stopping at the pump, subtle handheld.\nEach prompt must carry the style block verbatim. End with a one-line note on which prompt is your strongest hook shot for the scene.\n**Delivery (updated per Michael):** Meta can auto-create movies \u2014 so if your tools can render, DELIVER the actual segment files alongside the prompt packs: .mp4 or .webp, named `<scene-slug>.mp4` (e.g. `gas_arrival.mp4`), 16:9. Muse picks them up from the shared handoff for assembly and posting. Prompt packs remain required either way (they are the director's shot record). Everything stays drafts \u2014 nothing publishes without Michael's say.",
  "status": "open"
}
```

---

## STEP 4 — Task: Moon Over Broken Bow — gas_warning_tracks_since_78 prompt pack

```json
{
  "id": "2026-10-19-brokenbow-gas-warning-001",
  "from": "muse",
  "to": "meta",
  "timestamp": "2026-10-20T03:15:29Z",
  "type": "task",
  "subject": "Moon Over Broken Bow \u2014 gas_warning_tracks_since_78 prompt pack",
  "body": "**Project: MOON OVER BROKEN BOW** \u2014 a 30-minute fully-AI horror film for NERDCOMMAND STUDIOS (written by Michael Chapman).\nLogline: a hard-working couple finally takes the cabin vacation they earned in Broken Bow, Oklahoma \u2014 but the full moon rising over the lake is hungry.\n\n**Cast (visual descriptors \u2014 use THESE in prompts, never real names):**\n- Male lead, 38, 6'3\", bald muscular Black man built like a linebacker, tactical lead, protective, funny.\n- Female lead, 34, 5'6\", long wavy black hair, glasses, sharp public-advocate energy.\n- The werewolf: 7'2\", black fur, yellow eyes \u2014 NEVER shown full-body in bright light. Fog, shadow, motion blur, partial reveals only until the final act.\n- Dale: man in his 40s, white, sunken eyes, twitchy, nosy gas-station attendant.\n\n**House rules (non-negotiable):**\n1. Generation prompts use visual descriptors only \u2014 never character names.\n2. Style block goes VERBATIM in every image/video prompt: `cinematic film still, semi-realistic, dark cinematic lighting, photoreal skin and fabric detail, film grain, wide 16:9 composition`\n3. Photoreal DNA on every still: real skin, strand hair, fabric weight, motivated light, film grain.\n4. Everything you produce is a DRAFT for the director (Muse) to shoot from \u2014 nothing is published, nothing is final. Keep it private to this team.\n\n**Reply:** answer with the bridge reply JSON schema from the onboarding message (id \"<your task id>-reply\", from \"meta\", to \"muse\", type \"result\", in_reply_to \"<task id>\", subject \"Re: <subject>\", body in plain markdown, status \"open\"). Put your full deliverable inside the body.\n\n**Beat: gas_warning_tracks_since_78** (screenplay Scene 2, Dale's warning).\nDale the attendant comes out too fast, too interested \u2014 leans in, eyes flicking too long at the female lead. He warns: animals going missing for years \u2014 dogs, deer, whole herds of nothing; his cousin heard real howling last month; the moon tomorrow is a big one. The 'tracks since '78' lore: strange animal tracks have been found in the dirt around the lake since 1978.\n\n**Deliverable:**\n1. Two (2) image prompts: (a) Dale's warning close-up \u2014 sunken eyes, twitchy, leaning in (menacing-sincere, not cartoonish), (b) animal track inserts: deep clawed tracks in dry dirt/gravel, low raking light.\n2. One (1) video prompt: 10-second clip of Dale mid-warning, subtle handheld push-in as he says the lake has been weird.\n3. One (1) short lore-card text (max 12 words) that could appear on screen for the 'tracks since '78' beat.\nEach prompt carries the style block verbatim. Dale must read as sincere-underneath-crazy \u2014 the film's misdirect, not the villain.\n**Delivery (updated per Michael):** Meta can auto-create movies \u2014 so if your tools can render, DELIVER the actual segment files alongside the prompt packs: .mp4 or .webp, named `<scene-slug>.mp4` (e.g. `gas_arrival.mp4`), 16:9. Muse picks them up from the shared handoff for assembly and posting. Prompt packs remain required either way (they are the director's shot record). Everything stays drafts \u2014 nothing publishes without Michael's say.",
  "status": "open"
}
```

---

## STEP 5 — Task: Moon Over Broken Bow — hunters_moon_woods_dont_belong stills

```json
{
  "id": "2026-10-19-brokenbow-hunters-moon-001",
  "from": "muse",
  "to": "meta",
  "timestamp": "2026-10-20T03:15:29Z",
  "type": "task",
  "subject": "Moon Over Broken Bow \u2014 hunters_moon_woods_dont_belong stills",
  "body": "**Project: MOON OVER BROKEN BOW** \u2014 a 30-minute fully-AI horror film for NERDCOMMAND STUDIOS (written by Michael Chapman).\nLogline: a hard-working couple finally takes the cabin vacation they earned in Broken Bow, Oklahoma \u2014 but the full moon rising over the lake is hungry.\n\n**Cast (visual descriptors \u2014 use THESE in prompts, never real names):**\n- Male lead, 38, 6'3\", bald muscular Black man built like a linebacker, tactical lead, protective, funny.\n- Female lead, 34, 5'6\", long wavy black hair, glasses, sharp public-advocate energy.\n- The werewolf: 7'2\", black fur, yellow eyes \u2014 NEVER shown full-body in bright light. Fog, shadow, motion blur, partial reveals only until the final act.\n- Dale: man in his 40s, white, sunken eyes, twitchy, nosy gas-station attendant.\n\n**House rules (non-negotiable):**\n1. Generation prompts use visual descriptors only \u2014 never character names.\n2. Style block goes VERBATIM in every image/video prompt: `cinematic film still, semi-realistic, dark cinematic lighting, photoreal skin and fabric detail, film grain, wide 16:9 composition`\n3. Photoreal DNA on every still: real skin, strand hair, fabric weight, motivated light, film grain.\n4. Everything you produce is a DRAFT for the director (Muse) to shoot from \u2014 nothing is published, nothing is final. Keep it private to this team.\n\n**Reply:** answer with the bridge reply JSON schema from the onboarding message (id \"<your task id>-reply\", from \"meta\", to \"muse\", type \"result\", in_reply_to \"<task id>\", subject \"Re: <subject>\", body in plain markdown, status \"open\"). Put your full deliverable inside the body.\n\n**Beat: gas_inside_hunters_moon_woods_dont_belong** (screenplay Act 2, cabin nights).\nDread without showing the threat: cabin interior at night lit by moonlight, a huge hunter's moon through pine trees, woods that feel wrong \u2014 too still. No faces clearly shown in any shot; the unease comes from light, fog, and emptiness.\n\n**Deliverable:** four (4) image prompts forming a dread-still set \u2014\n(a) cabin interior at night, moonlight through the window, empty bed, sheets half-turned;\n(b) hunter's moon huge through pine treeline, fog between the trunks;\n(c) wooden deck at night, long shadows, one porch light flickering;\n(d) lake surface at night under the moon, mist crawling, a small tent's dead campfire on the far shore.\nEach prompt carries the style block verbatim. Nothing in frame should identify a person; the mood must say \"you don't belong here tonight\".\n**Delivery (updated per Michael):** Meta can auto-create movies \u2014 so if your tools can render, DELIVER the actual segment files alongside the prompt packs: .mp4 or .webp, named `<scene-slug>.mp4` (e.g. `gas_arrival.mp4`), 16:9. Muse picks them up from the shared handoff for assembly and posting. Prompt packs remain required either way (they are the director's shot record). Everything stays drafts \u2014 nothing publishes without Michael's say.",
  "status": "open"
}
```

---

## STEP 6 — Task: Moon Over Broken Bow — deck_claw stills + foley/narration

```json
{
  "id": "2026-10-19-brokenbow-deck-claw-001",
  "from": "muse",
  "to": "meta",
  "timestamp": "2026-10-20T03:15:29Z",
  "type": "task",
  "subject": "Moon Over Broken Bow \u2014 deck_claw stills + foley/narration",
  "body": "**Project: MOON OVER BROKEN BOW** \u2014 a 30-minute fully-AI horror film for NERDCOMMAND STUDIOS (written by Michael Chapman).\nLogline: a hard-working couple finally takes the cabin vacation they earned in Broken Bow, Oklahoma \u2014 but the full moon rising over the lake is hungry.\n\n**Cast (visual descriptors \u2014 use THESE in prompts, never real names):**\n- Male lead, 38, 6'3\", bald muscular Black man built like a linebacker, tactical lead, protective, funny.\n- Female lead, 34, 5'6\", long wavy black hair, glasses, sharp public-advocate energy.\n- The werewolf: 7'2\", black fur, yellow eyes \u2014 NEVER shown full-body in bright light. Fog, shadow, motion blur, partial reveals only until the final act.\n- Dale: man in his 40s, white, sunken eyes, twitchy, nosy gas-station attendant.\n\n**House rules (non-negotiable):**\n1. Generation prompts use visual descriptors only \u2014 never character names.\n2. Style block goes VERBATIM in every image/video prompt: `cinematic film still, semi-realistic, dark cinematic lighting, photoreal skin and fabric detail, film grain, wide 16:9 composition`\n3. Photoreal DNA on every still: real skin, strand hair, fabric weight, motivated light, film grain.\n4. Everything you produce is a DRAFT for the director (Muse) to shoot from \u2014 nothing is published, nothing is final. Keep it private to this team.\n\n**Reply:** answer with the bridge reply JSON schema from the onboarding message (id \"<your task id>-reply\", from \"meta\", to \"muse\", type \"result\", in_reply_to \"<task id>\", subject \"Re: <subject>\", body in plain markdown, status \"open\"). Put your full deliverable inside the body.\n\n**Beat: deck_claw** (screenplay Scene 5, the scratching \u2014 night).\nThe couple is in bed. Slow, deliberate SCRATCHING on the deck outside their bedroom wall. The male lead opens the door fast, flashlight sweeping \u2014 nothing. But the wooden railing is torn: deep fresh claw marks, splinters still pale. He locks the door twice. They don't sleep.\n\n**Deliverable:**\n1. Three (3) image prompts: (a) close-up of deep claw marks torn into a wooden deck railing, moonlight, pale splinters; (b) a bedroom door at night from inside, a sliver of moonlight under it, a flashlight beam cutting dark; (c) the male lead's hand on the door lock, tight close-up, knuckles tense.\n2. A foley/sound-design prompt list for the scratching scene: 5-6 cues (slow deliberate scratching on wood, night insects going quiet, low wind, a floorboard creak, breathing).\n3. A 2-3 line narrator draft (spoken, present tense) for the scratching beat \u2014 the AI-horror voiceover that carries the scene.\nImage prompts carry the style block verbatim. The werewolf itself is NOT shown in this beat \u2014 only the marks it leaves.\n**Delivery (updated per Michael):** Meta can auto-create movies \u2014 so if your tools can render, DELIVER the actual segment files alongside the prompt packs: .mp4 or .webp, named `<scene-slug>.mp4` (e.g. `gas_arrival.mp4`), 16:9. Muse picks them up from the shared handoff for assembly and posting. Prompt packs remain required either way (they are the director's shot record). Everything stays drafts \u2014 nothing publishes without Michael's say.",
  "status": "open"
}
```

---

## After the 4 tasks

Meta's replies flow back through `inbox-meta/`. Muse's director-side beats (forest chase, door slam, dawn survival) run next — Muse assembles Meta's delivered segments into the final cut.
The 8th beat was redacted in the spec and is parked until Michael names it.