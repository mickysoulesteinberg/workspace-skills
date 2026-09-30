#!/usr/bin/env python3
"""
Session bootstrap. Claims a working directory at
<root>/logs/agent-sessions/_current-<slug>/ and writes starting metadata to
session.yml there. A close-out skill reads that file at session end.

Invocation: run by the `quest` skill, which decides which project the session
belongs to and passes that project's root as `--root`. This script never
guesses the project: without `--root` it exits.

Modes:
- Settings: `--show-settings` prints the project's settings file
  (<root>/.agents/skill-settings/quest.md) and exits without touching disk.
  `quest` runs it as soon as it knows the project; `tidy-quest` runs it
  before its passes.
- Default: dir is `_current-<HHMM>-<color-animal>/`.
- Named: `--slug NAME` -> dir is `_current-<HHMM>-<NAME>/` (suffix `-2`,
  `-3`, … on collision). Lets a session get a descriptive name instead of a
  random color-animal pair whenever the agent already knows what it's about.

Either way session.yml records `name` (NAME, or the color-animal pair) so a
session can be found by name without parsing the folder name. HHMM is the
computer's local time.

There is no automatic reuse: this script always creates a new dir.
Continuation is resolved by the calling skill (quest) *before* this script
ever runs: if the user names an existing `_current-*/` dir to continue, the
skill uses that dir directly and never calls this script.

Positional args are accepted and ignored (legacy `source` / `computer`
labels; the environment a session ran in is no longer recorded).

Required:
  --root PATH          Root of the project the session belongs to. The session
                       dir is created under PATH/logs/agent-sessions/.

Optional args (any order):
  --help, -h           Print this usage and exit. Never touches disk.
  --show-settings      Print the project's settings file and exit. Never
                       touches disk.
  --slug NAME          Named dir `_current-<HHMM>-<NAME>/`; never reuses.
  --forked-from PATH   Fork provenance: writes `forked_from: "PATH"` into this
                       (child) session's session.yml. PATH is the origin
                       session's folder, prefixed with its project folder's
                       name (e.g. `my-project/logs/agent-sessions/_current-1508-foo`).
                       Nothing updates it later, so it goes stale when the
                       origin is closed out and renamed; the slug inside it
                       still identifies the origin.

Example:
  python3 session-bootstrap.py --root ~/projects/my-project --show-settings

  python3 session-bootstrap.py --root ~/projects/my-project --slug api-cleanup

  python3 session-bootstrap.py --root ~/projects/my-project \
      --slug fork-skill-patches \
      --forked-from my-project/logs/agent-sessions/_current-1433-api-cleanup
"""

from __future__ import annotations

import datetime as dt
import random
import sys
from pathlib import Path

LOG_ROOT = "logs/agent-sessions"  # single place to change the session log root
SETTINGS_FILE = ".agents/skill-settings/quest.md"  # project settings, relative to --root
STALE_HOURS = 24  # warn about _current-*/ dirs older than this

# Flags earlier versions accepted. Each is ignored with a warning, and its value
# is skipped so it can't be misread.
RETIRED_FLAGS = {
    "--plan-slug": "plan rollouts are no longer supported",
    "--ticket-key": "pass the key as --slug; the project's settings file says how keys are named",
}

# Word lists for readable session IDs (color + animal)
COLORS = [
    "amber", "azure", "black", "blue", "bronze", "brown", "coral", "cream",
    "crimson", "cyan", "gold", "green", "grey", "indigo", "ivory", "jade",
    "lavender", "lime", "mint", "navy", "olive", "orange", "peach", "pink",
    "plum", "purple", "red", "rose", "ruby", "rust", "sage", "scarlet",
    "silver", "slate", "teal", "violet", "white", "yellow",
]

ANIMALS = [
    "badger", "bear", "beaver", "bison", "cobra", "condor", "crane", "crow",
    "deer", "dolphin", "eagle", "falcon", "ferret", "finch", "fox", "gecko",
    "hare", "hawk", "heron", "ibis", "jackal", "jaguar", "kestrel", "kite",
    "lemur", "lynx", "marten", "mink", "moose", "otter", "owl", "panda",
    "parrot", "penguin", "puffin", "quail", "raven", "seal", "shrew", "skunk",
    "sloth", "snipe", "stoat", "swift", "tapir", "thrush", "vole", "weasel",
    "wolf", "wombat", "wren", "yak",
]


def resolve_root(argv: list[str]) -> Path:
    """Return the project root passed as `--root PATH`. Exits if missing or not a dir."""
    if "--root" in argv:
        i = argv.index("--root")
        if i + 1 < len(argv):
            root = Path(argv[i + 1]).expanduser().resolve()
            if root.is_dir():
                return root
            sys.exit(f"[session-bootstrap] --root is not a directory: {root}")
    sys.exit("[session-bootstrap] missing --root PATH (the project the session belongs to)")


def show_settings(ws: Path) -> None:
    """Print the project's settings file, or say there isn't one."""
    path = ws / SETTINGS_FILE
    if not path.is_file():
        sys.stdout.write(
            f"[session-bootstrap] No project settings ({SETTINGS_FILE}); "
            "using quest's defaults.\n"
        )
        return
    sys.stdout.write(
        f"[session-bootstrap] Project settings from {SETTINGS_FILE}. Apply them: they "
        "override quest's and tidy-quest's defaults, and the project's AGENTS.md on "
        "anything about sessions.\n"
        "----- begin settings -----\n"
    )
    text = path.read_text(encoding="utf-8")
    sys.stdout.write(text if text.endswith("\n") else text + "\n")
    sys.stdout.write("----- end settings -----\n")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")


def random_word_pair() -> str:
    return f"{random.choice(COLORS)}-{random.choice(ANIMALS)}"


def hhmm_local() -> str:
    """Return HHMM in the computer's local time."""
    return dt.datetime.now().strftime("%H%M")


def find_stale_current_dirs(log_root: Path) -> list[Path]:
    if not log_root.exists():
        return []
    cutoff = dt.datetime.now().timestamp() - STALE_HOURS * 3600
    return [
        p for p in log_root.glob("_current-*")
        if p.is_dir() and p.stat().st_mtime < cutoff
    ]


def read_yaml_field(path: Path, field: str) -> str | None:
    """Extract a single scalar field from flat session.yml (quoted or bare)."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    prefix = f"{field}:"
    for line in text.splitlines():
        if not line.startswith(prefix):
            continue
        rest = line[len(prefix) :].lstrip()
        if not rest or rest == "null":
            return None
        if rest[0] == '"':
            out: list[str] = []
            i = 1
            while i < len(rest):
                ch = rest[i]
                if ch == "\\" and i + 1 < len(rest):
                    out.append(rest[i + 1])
                    i += 2
                    continue
                if ch == '"':
                    break
                out.append(ch)
                i += 1
            return "".join(out)
        return rest
    return None


def find_open_session_dirs(log_root: Path) -> list[Path]:
    """Return open `_current-*/` dirs that have a session.yml.

    Used only for the informational FYI listing at bootstrap time -- sessions
    are never auto-reused.
    """
    if not log_root.exists():
        return []
    return [
        p for p in log_root.glob("_current-*")
        if p.is_dir() and (p / "session.yml").exists()
    ]


def unique_named_session_dir(log_root: Path, hhmm: str, name: str) -> tuple[Path, str]:
    """Return (dir, slug) for a new named session.

    First try HHMM-NAME; if `_current-HHMM-NAME/` exists, suffix -2, -3, …
    Never reuses or overwrites an existing dir.
    """
    base = f"{hhmm}-{name}"
    slug = base
    n = 2
    while True:
        candidate = log_root / f"_current-{slug}"
        if not candidate.exists():
            return candidate, slug
        slug = f"{base}-{n}"
        n += 1


def parse_extra_args(args: list[str]) -> tuple[str | None, str | None]:
    """Parse flags from args.

    Returns: (custom_slug, forked_from)
      custom_slug -- str from --slug, or None
      forked_from -- str from --forked-from, or None

    Retired flags (RETIRED_FLAGS) print a warning and skip their value. Other
    unknown flags are ignored (forward-compatible). `--help`/`-h` and
    `--show-settings` are handled by the caller before this function runs.
    """
    custom_slug: str | None = None
    forked_from: str | None = None
    i = 0
    while i < len(args):
        if args[i] == "--slug" and i + 1 < len(args):
            custom_slug = args[i + 1].strip()
            i += 2
        elif args[i] == "--forked-from" and i + 1 < len(args):
            forked_from = args[i + 1].strip()
            i += 2
        elif args[i] in RETIRED_FLAGS:
            sys.stdout.write(
                f"[session-bootstrap] WARNING: {args[i]} is retired and was ignored "
                f"({RETIRED_FLAGS[args[i]]}).\n"
            )
            i += 2
        else:
            i += 1
    return custom_slug, forked_from


def yaml_double_quoted(value: str) -> str:
    """Escape a string for a YAML double-quoted scalar."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def write_session_yaml(path: Path, data: dict) -> None:
    """Hand-rolled YAML (no PyYAML dep). Handles str and None values."""
    lines = []
    for key, value in data.items():
        if value is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {yaml_double_quoted(str(value))}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def seed_continuity_files(ws: Path, session_dir: Path) -> None:
    """Seed current-state.md + timeline.md from this skill's own templates if missing."""
    # The templates sit in the skill folder, next to this script's folder.
    templates = Path(__file__).resolve().parent.parent / "references"
    for name in ("current-state.md", "timeline.md"):
        dest = session_dir / name
        if dest.exists():
            continue
        src = templates / name
        if src.is_file():
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            sys.stdout.write(
                f"[session-bootstrap] Seeded {dest.relative_to(ws)}\n"
            )
        else:
            sys.stdout.write(
                f"[session-bootstrap] WARNING: missing template {src}; "
                f"did not seed {name}\n"
            )


def main() -> int:
    # --help/-h first, before anything else touches disk (resolve_root() is a
    # pure path resolution and doesn't write, but the mkdir() below does).
    argv = sys.argv[1:]
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0

    ws = resolve_root(argv)
    if "--show-settings" in argv:
        show_settings(ws)
        return 0

    agent_sessions = ws / LOG_ROOT
    agent_sessions.mkdir(parents=True, exist_ok=True)

    # Parse argv: --slug and/or --forked-from.
    # Leading positionals are legacy `source` / `computer` labels -- still
    # accepted from older call sites so they don't get misread as flags, but
    # discarded: the environment a session ran in is no longer recorded.
    while argv and not argv[0].startswith("--"):
        argv.pop(0)
    custom_slug, forked_from = parse_extra_args(argv)

    stale = find_stale_current_dirs(agent_sessions)
    if stale:
        sys.stdout.write(f"[session-bootstrap] Stale _current-*/ dirs (>{STALE_HOURS}h):\n")
        for p in stale:
            sys.stdout.write(f"  {p.relative_to(ws)}\n")
        sys.stdout.write("[session-bootstrap] Close out or delete when you get a chance.\n")

    # Sessions are never auto-reused here. Continuation is resolved by the
    # calling skill (quest) before it ever invokes this script -- if the user
    # named an existing dir, the skill uses it directly and skips bootstrap
    # entirely. This always creates.
    hhmm = hhmm_local()
    if custom_slug:
        name = custom_slug
        session_dir, slug = unique_named_session_dir(agent_sessions, hhmm, name)
        if slug != f"{hhmm}-{name}":
            sys.stdout.write(
                f"[session-bootstrap] slug collision: using {session_dir.name}/ "
                f"(left _current-{hhmm}-{name}/ untouched)\n"
            )
    else:
        name = random_word_pair()
        slug = f"{hhmm}-{name}"
        session_dir = agent_sessions / f"_current-{slug}"

    others = find_open_session_dirs(agent_sessions)
    if others:
        sys.stdout.write(
            "[session-bootstrap] FYI -- other open _current-*/ dir(s) already exist "
            "(not reused; sessions are always new):\n"
        )
        for p in others:
            p_slug = read_yaml_field(p / "session.yml", "slug") or p.name
            sys.stdout.write(f"  {p.relative_to(ws)} (slug={p_slug})\n")

    session_dir.mkdir(parents=True, exist_ok=True)
    seed_continuity_files(ws, session_dir)

    # --- Write session.yml ---
    data: dict = {
        "slug": slug,
        "name": name,
        "kind": "adhoc",
        "started_at": now_iso(),
    }
    if forked_from:
        data["forked_from"] = forked_from

    write_session_yaml(session_dir / "session.yml", data)

    rel = session_dir.relative_to(ws)
    sys.stdout.write(
        f"[session-bootstrap] Active session: {rel}/\n"
        "[session-bootstrap] Drop session-scoped artifacts here.\n"
        f"[session-bootstrap] Session ID: {slug}\n"
        f'[session-bootstrap] Claude: tell the user the session ID is "{slug}". '
        "Do not ask about renaming the session dir.\n"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
