"""
NERDCOMMAND SUPER AGENT - Meta AI x Muse.ai Bridge
Written by Michael Chapman

Two-brain split:
  meta_ai  -> creation front-end: script, image_gen, video_prompt, thumbnail, youtube, github
  muse_ai  -> director back-end: director, clip_extend, auto_edit, viral_cut, voice_sync, timeline

Pipeline loop (Michael 2026-10-19): Meta auto-creates movies and delivers segment
files (.mp4/.webp, 16:9, named <scene-slug>.mp4) into meta_out/ -> sync carries them
to the shared handoff -> Muse assembles (timeline, voice_sync, credit_animation,
final cut) with the prompt packs as the shot record -> posts via the YouTube/social
pipeline. Drafts first: nothing publishes without Michael's say.

Usage:
    pip install watchdog requests        # watchdog optional; falls back to polling
    python super_agent_bridge.py --once            # one pass: route beats, write handoffs, sync
    python super_agent_bridge.py --watch 300       # loop every 300s, syncing meta_out/ <-> shared
    python super_agent_bridge.py --dry-run         # sandbox run: writes to a temp dir, touches nothing real
"""

import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_PATH = Path(os.environ.get("SUPER_AGENT_CONFIG", HERE / "super_agent_config.json"))

# ---------------------------------------------------------------------------
# Explicit beat -> brain map for MOON OVER BROKEN BOW.
# Meta leads on creation beats (script/prompt/still/thumbnail);
# Muse leads on director beats (extend/edit/voice/timeline/final cut).
# Every beat carries a concrete deliverable and the next action.
# ---------------------------------------------------------------------------
BEAT_MAP = {
    "gas_arrival": {
        "brain": "meta_ai",
        "deliverable": "scene prompt pack + establishing stills: weathered gas station, "
                       "one working pump, screen door, late-afternoon light, Michael's SUV arriving",
        "next_action": "muse_extend_10s_to_90s",
    },
    "gas_warning_tracks_since_78": {
        "brain": "meta_ai",
        "deliverable": "warning beats: Dale warning close-ups + animal-track inserts in dirt "
                       "(lore: tracks since '78), video_prompt per insert",
        "next_action": "muse_extend_10s_to_90s",
    },
    "gas_inside_hunters_moon_woods_dont_belong": {
        "brain": "meta_ai",
        "deliverable": "dread stills: cabin interior night, hunter's moon through pines, "
                       "'woods don't belong' unease set (no faces shown)",
        "next_action": "muse_extend_10s_to_90s",
    },
    "deck_claw": {
        "brain": "meta_ai",
        "deliverable": "claw-mark insert stills on deck railing (moonlight close-up) + "
                       "foley/narration prompt for the scratching scene",
        "next_action": "muse_auto_edit_inserts",
    },
    "forest_chase_fight_to_the_truck": {
        "brain": "muse_ai",
        "deliverable": "director cut: extend 10s chase still into 90s action — handheld chaos "
                       "grammar, shaky/dutch angles, SUV dents continuity",
        "next_action": "meta_beat_thumbnail",
    },
    "door_slam_hold_it": {
        "brain": "muse_ai",
        "deliverable": "extend + voice_sync the door-slam/hold sequence — tension edit, "
                       "breathing room before the final stand",
        "next_action": "meta_beat_thumbnail",
    },
    "dawn_survival": {
        "brain": "muse_ai",
        "deliverable": "final cut assembly: dawn survival wide, warm grade returns, "
                       "credit_animation roll, final-howling stinger kept",
        "next_action": "meta_youtube_package",
    },
    "[REDACTED 8th beat]": {
        "brain": "muse_ai",
        "deliverable": "HOLD — beat name was redacted in Michael's spec; awaiting his title "
                       "before routing real work",
        "next_action": "awaiting_michael_beat_name",
        "status": "blocked",
    },
}


def load_config():
    return json.loads(Path(CONFIG_PATH).read_text())


def route_task(task: str):
    """Explicit map first; keyword heuristics only for beats Michael adds later."""
    key = task.strip()
    if key in BEAT_MAP:
        info = BEAT_MAP[key]
        return info["brain"], info
    t = task.lower()
    if any(k in t for k in ["script", "image", "thumb", "youtube", "github", "prompt", "lore", "still"]):
        return "meta_ai", {"deliverable": f"creation assets for '{task}'", "next_action": "muse_extend_10s_to_90s"}
    if any(k in t for k in ["director", "extend", "timeline", "viral", "auto_edit", "voice", "cut", "assembly"]):
        return "muse_ai", {"deliverable": f"director work for '{task}'", "next_action": "meta_beat_thumbnail"}
    return "meta_ai", {"deliverable": f"creation assets for '{task}' (default route)", "next_action": "muse_extend_10s_to_90s"}


def sync_files(src: Path, dst: Path, types):
    """Newest-wins copy of tracked file types from src tree into dst."""
    dst.mkdir(parents=True, exist_ok=True)
    moved = []
    for f in src.rglob("*"):
        if f.is_file() and f.suffix.lower() in types:
            target = dst / f.name
            if not target.exists() or f.stat().st_mtime > target.stat().st_mtime:
                shutil.copy2(f, target)
                moved.append(f.name)
                print(f"[SYNC] {f.name} -> {dst}")
    return moved


def handoff_loop(shared_root: Path, dry_run: bool = False):
    config = load_config()
    print(f"=== {config['super_agent']} v{config['version']} ===")
    if dry_run:
        print("[DRY-RUN] sandbox mode — no real folders touched")

    shared = shared_root / config["bridge"]["local_shared"]
    shared.mkdir(parents=True, exist_ok=True)
    file_types = tuple(config["bridge"].get("file_types", [".mp4", ".webp", ".jpg", ".json", ".html"]))

    brain_folders = {}
    for brain, info in config["brains"].items():
        folder = shared_root / info["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        brain_folders[brain] = folder

    print("[BRIDGE ACTIVE] Meta AI + Muse.ai linked")
    print(f"Repo: {config['bridge']['shared_repo']}")
    print(f"Shared handoff dir: {shared}\n")

    routed = []
    for scene in config["pipeline"]["moon_over_broken_bow"]:
        brain, info = route_task(scene)
        status = info.get("status", "open")
        print(f"[ROUTING] {scene} => {brain} [{status}]")
        print(f"           deliverable: {info['deliverable']}")
        handoff = {
            "scene": scene,
            "assigned_to": brain,
            "deliverable": info["deliverable"],
            "next_action": info["next_action"],
            "project": "moon_over_broken_bow",
            "studio": "NERDCOMMAND STUDIOS",
            "written_by": "Michael Chapman",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "credit": config["credit_animation"],
        }
        (shared / f"{scene}.json").write_text(json.dumps(handoff, indent=2))
        routed.append((scene, brain, status))

    print(f"\n[DONE] {len(routed)} handoff JSONs in {shared}/")
    return routed, shared, brain_folders, file_types


def watch_loop(interval: int = 300):
    config = load_config()
    shared = Path(config["bridge"]["local_shared"])
    file_types = tuple(config["bridge"].get("file_types", [".mp4", ".webp", ".jpg", ".json", ".html"]))
    brain_folders = {b: Path(i["folder"]) for b, i in config["brains"].items()}

    def one_pass():
        print(f"[{datetime.now(timezone.utc).isoformat()}] sync pass")
        for brain, folder in brain_folders.items():
            if folder.exists():
                sync_files(folder, shared, file_types)

    try:
        from watchdog.observers import Observer  # type: ignore
        from watchdog.events import FileSystemEventHandler  # type: ignore

        class Handler(FileSystemEventHandler):
            def on_any_event(self, event):
                if not event.is_directory and Path(event.src_path).suffix.lower() in file_types:
                    one_pass()

        observer = Observer()
        for folder in list(brain_folders.values()) + [shared]:
            folder.mkdir(parents=True, exist_ok=True)
            observer.schedule(Handler(), str(folder), recursive=True)
        observer.start()
        print(f"[WATCH] live sync on {list(brain_folders)} (watchdog)")
        try:
            while True:
                time.sleep(interval)
                one_pass()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    except ImportError:
        print(f"[WATCH] watchdog not installed — polling every {interval}s")
        for folder in list(brain_folders.values()) + [shared]:
            folder.mkdir(parents=True, exist_ok=True)
        try:
            while True:
                one_pass()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("[WATCH] stopped")


def main():
    args = sys.argv[1:]
    if "--watch" in args:
        idx = args.index("--watch")
        interval = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else 300
        watch_loop(interval)
    elif "--dry-run" in args:
        sandbox = Path(tempfile.mkdtemp(prefix="superagent-dryrun-"))
        routed, shared, _, _ = handoff_loop(sandbox, dry_run=True)
        print(f"\n[DRY-RUN OK] {len(routed)} beats routed, sandbox at {sandbox}")
    else:  # --once or no args
        handoff_loop(Path.cwd())


if __name__ == "__main__":
    main()
