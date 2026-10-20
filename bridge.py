#!/usr/bin/env python3
"""Agent Bridge autopilot: Muse -> Meta Llama API -> inbox-meta.

Polls 06-agent-bridge/outbox-muse/ for open messages, sends each body to
Meta's Llama API, writes the reply as a result JSON into inbox-meta/,
and flips the original to answered (then archives the pair to messages/).

Needs: LLAMA_API_KEY env var (https://developers.meta.com / Meta AI API).
Manual mode (no key): Michael copy-pastes between outbox-muse/ and the
Meta AI app, dropping replies into inbox-meta/ by hand.

Usage:
    python3 bridge.py --once        # single poll
    python3 bridge.py --watch 300   # poll every 300s
"""
import json, os, sys, time, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUTBOX = os.path.join(HERE, 'outbox-muse')
INBOX = os.path.join(HERE, 'inbox-meta')
ARCHIVE = os.path.join(HERE, 'messages')
API_URL = 'https://api.llama-api.com/chat/completions'
MODEL = os.environ.get('LLAMA_MODEL', 'llama-3.3-70b-versatile')


def load(p):
    with open(p) as f:
        return json.load(f)


def save(p, d):
    with open(p, 'w') as f:
        json.dump(d, f, indent=2)


def call_llama(prompt):
    key = os.environ['LLAMA_API_KEY']
    body = json.dumps({
        'model': MODEL,
        'messages': [
            {'role': 'system',
             'content': ('You are Meta AI, teammate to Muse (another AI agent) '
                         'and Michael Chapman. Answer directly and completely. '
                         'You are replying through a shared GitHub mailbox; '
                         'keep formatting plain markdown.')},
            {'role': 'user', 'content': prompt},
        ],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return d['choices'][0]['message']['content']


def process_one(path):
    msg = load(path)
    if msg.get('status') != 'open' or msg.get('to') != 'meta':
        return False
    print(f'-> answering {msg["id"]}: {msg.get("subject","")}')
    reply_body = call_llama(f"Subject: {msg.get('subject','')}\n\n{msg['body']}")
    rid = msg['id'] + '-reply'
    reply = {
        'id': rid,
        'from': 'meta', 'to': 'muse',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'type': 'result', 'in_reply_to': msg['id'],
        'subject': f"Re: {msg.get('subject','')}",
        'body': reply_body, 'status': 'open',
    }
    save(os.path.join(INBOX, rid + '.json'), reply)
    msg['status'] = 'answered'
    save(path, msg)
    for p, name in ((path, msg['id'] + '.json'),
                    (os.path.join(INBOX, rid + '.json'), rid + '.json')):
        os.rename(p, os.path.join(ARCHIVE, name))
    print(f'<- replied, archived pair {msg["id"]}')
    return True


def main():
    watch = '--watch' in sys.argv
    interval = int(sys.argv[sys.argv.index('--watch') + 1]) if watch else 0
    if 'LLAMA_API_KEY' not in os.environ:
        print('LLAMA_API_KEY not set. Manual mode: paste outbox bodies into '
              'the Meta AI app and drop replies into inbox-meta/.')
        sys.exit(2)
    while True:
        did = False
        for fn in sorted(os.listdir(OUTBOX)):
            if fn.endswith('.json'):
                try:
                    did = process_one(os.path.join(OUTBOX, fn)) or did
                except Exception as e:
                    print(f'!! {fn}: {e}')
        if not watch:
            break
        time.sleep(interval)


if __name__ == '__main__':
    main()
