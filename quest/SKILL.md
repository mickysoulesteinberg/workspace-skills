---
name: quest
description: Opt-in entry point for a piece of work that spans several chats (a "quest") — creates or continues its working session dir under logs/agent-sessions/_current-*/, forks a tangent into its own session mid-conversation, and routes in-flight notes and artifacts to that dir instead of memory. Invoke via /quest, with a path to continue an existing session.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/session-bootstrap.py *)
---

# quest

Claims (or resumes) a working session dir under `<project root>/logs/agent-sessions/_current-*/`, keeps in-flight artifacts routed to that dir instead of memory, and forks a live session mid-conversation when a tangent deserves its own dir. `current-state.md` is the file that actually carries live truth — a close-out skill, if the project has one (its settings may name it), reads from the session dir at the end and finalizes it.

A quest can span many chats. Each chat either starts the quest's session dir or resumes it, and this skill's files call that dir "the session" throughout.

**Status:** still being fitted to projects other than the one it was built in. When an instruction here doesn't fit the project you're in, ask the user rather than guessing.

**Files this skill uses** live in its own folder, `${CLAUDE_SKILL_DIR}`. For what each session-dir file is for — including `followups.md`, which this skill's body never fully explains — `Read` `${CLAUDE_SKILL_DIR}/references/session-files.md`.

**Writing files:** before writing `session.yml` / `current-state.md` / other session-dir files, follow the project's own rules for writing files (its `AGENTS.md` or `CLAUDE.md`).

---

## Invocation Modes

**Bootstrap** — full protocol (Steps 1–2 below). Triggered when:
- The user runs `/quest`, with or without a path to an existing session
- Any user message that names **`quest`** as a skill (including when task context rides along in the same message) — **hard gate:** read and follow this skill before any other work, even when task context is in the same message. Invoking the skill does not delay work; skipping it does.

This is **opt-in**, not run automatically on every message.

**Fork** — mid-session, when the user says something like "go ahead and fork," "split this off," "let's make this its own session" while a `_current-*/` dir is already live and being worked in. Full protocol in `${CLAUDE_SKILL_DIR}/references/fork-protocol.md`. Fork writes the child's `current-state.md` itself and does not invoke `tidy-quest` on either session — see that file's opening for why the origin is deliberately left uncurated. **After fork:** continue the **origin** in this chat; the user opens a new chat for the child when ready (`fork-protocol.md` § After fork).

When a session is already underway in this conversation, treat an explicit split-off request as Fork rather than Bootstrap, and a vague re-invocation as a question — ask what the user wants rather than starting a duplicate session.

---

## Bootstrap Protocol

**Step 1 — Find or create the session dir**

**Which project.** The session dir lives in the project the work belongs to. Call that project's root `$ROOT`; sessions go under `$ROOT/logs/agent-sessions/`. With several folders open, work out the project from the conversation — what the work is about, which project's files it touches. The current working directory is not a reliable signal: it can change mid-conversation. State which project you picked. If it's genuinely unclear, ask.

**Read the project's `AGENTS.md` (or `CLAUDE.md`) now if it isn't already in context.** Only the *primary* working directory's instructions load automatically at conversation start. When the session's project is an additional working directory, its own instructions never load, so its working preferences and layout are absent until read deliberately. Applies to any additional working directory whose conventions the session's work will touch, not just `$ROOT`.

**Project settings.** As soon as `$ROOT` is settled — from the conversation, or from a continuation path below — print the project's settings and follow them for the rest of the session:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/session-bootstrap.py --root "$ROOT" --show-settings
```

The settings live in `$ROOT/.agents/skill-settings/quest.md`, written by the user. They override this skill's defaults and, on anything about sessions, the project's `AGENTS.md`. They can change how sessions are named or found, which close-out skill the project uses, and anything else here. Run this before naming a new session, because the settings may say how to name it. No file means the defaults below apply unchanged.

**Continuation-by-path detection.** **First** — before the detections below — check whether the invocation itself names an existing session — a `_current-*/` dir, or a file inside one (`current-state.md`, `session.yml`, `timeline.md`). A path is a continuation: resolve it to `$SESSION_DIR` and take the **Resuming path** below. This is the *only* place a continuation gets named by path — nothing downstream asks for one. The path also settles `$ROOT`: it is the folder above the path's `logs/agent-sessions/`.

It matters most when the invocation arrives from a different project's working directory than the session belongs to. The path is then the only thing connecting the two, which is exactly why no other instruction came with it. Read the session before asking anything, then state the goal and current next step back **in your own words** — a restatement, not an echo. If the message still leaves the intent genuinely open (continue here / context only / wrong session), ask; if it doesn't, just continue.

**Descriptive-slug detection.** A session should get a descriptive name rather than defaulting straight to a random color-animal pair, whenever the topic is already clear from the conversation so far. Derive a short kebab-case slug from the conversation's actual topic and pass it as `--slug $SLUG`. When the project's settings say how to name a session (for example, after a ticket key in the start message), their rule wins. Do not ask the user to approve the name first — it's a session dir name, not a durable artifact. Fall back to the random color-animal pair only when the topic genuinely isn't established yet (e.g. `/quest` invoked as the very first message with no other context).

**Continuation by name.** If the user names a session rather than giving a path, look in `$ROOT/logs/agent-sessions/_current-*/`. Match the `name` in each `session.yml`, ignoring case, or the folder name or `slug`. If two open dirs match, ask which to join. A path wins over a name.

**Default is always a new session.** Continuation only happens when the user explicitly names a specific existing dir — by name or by path (see the detections above). The bootstrap script never decides this: it always creates a new dir. If the user doesn't name a dir, run bootstrap. The only question to ask first is which project, when that's unclear (**Which project** above) — not Claude usage or cost (see **`session.yml` fields** below) — and don't list other open session dirs.

Once the session dir is set, proceed immediately to any work the user expressed alongside the invocation. Do not ask about session goals or what the user wants to work on — if intent was clear from their message, act on it.

**New session path:** Run bootstrap with `--root`, plus `--slug` when a name was derived.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/session-bootstrap.py --root "$ROOT" [--slug $SLUG]
```

Put the actual project root in place of `$ROOT`, quoted (paths can contain spaces). Read the output, extract the slug, confirm the dir was created. Set `$SESSION_DIR`.

**The script always creates.** It makes `_current-HHMM-<slug>/` with `--slug`, or `_current-HHMM-<color>-<animal>/` without it (suffix `-2`, `-3`, … if that dir already exists), and records the unprefixed name as `name` in `session.yml`. It lists other open dirs as an FYI but never joins one. The only way to continue an existing dir is for the user to name it in the invocation — see the detections above.

**Resuming path:** Use the named dir as `$SESSION_DIR`. Read `session.yml` and **`current-state.md`** (live truth), then each file its Resources table marks `every time` — and no others until the work needs them. Do **not** load `timeline.md` unless troubleshooting or the user asks. Do not run bootstrap.

**Step 2 — Reinforce session dir routing**

Hold this rule throughout the session: anything the user asks you to remember, any note or task they hand you, any artifact produced — write it to `$SESSION_DIR/`, not to memory. If the user says "remember this" or "keep a note of that," write a file in the session dir immediately. The session dir is the single source of truth for in-flight work. Net-new docs and drafts go to `$SESSION_DIR`, even when the work belongs to a ticket or a project folder, unless the user asks to put them there now. Promotion into the project happens at close-out.

**The concern is that unfinished thinking must not ship — creating a stray file is only one way that happens.** In-flight state — what you are mid-way through, what you plan to check next, why something is currently expected to fail, a measurement taken while investigating — goes to `$SESSION_DIR`, never into a comment added to a committed repo file. That includes a file you are already editing for good reason: adding a note there creates nothing and feels like putting it nowhere, which is exactly why it gets through. Session state is provisional and personal; a repo comment is permanent, unowned, and nothing re-reads it — a comment carrying a *prediction* is the worst case, since it reads as authoritative right up until someone checks. If the finding is durable and belongs to the project, it goes to its real home — a doc, a ticket — not a comment near the code. Narrow exception: when knowingly committing something incomplete, a comment telling a teammate what is unfinished is warranted. That is an explicit decision, not a default.

**Continuable sessions (default):** Bootstrap seeds `current-state.md` + `timeline.md` from `${CLAUDE_SKILL_DIR}/references/`. Every session is continuable — stop on a dime, resume later by pointing a fresh chat at the existing `$SESSION_DIR` and reading **current-state**, plus the files it marks `every time`.

**`current-state.md`:** Live truth. Edit sections **in place** so the file stays accurate. Follow the HTML comment at the top of the file. When the user points at a file (or you produce a durable artifact), update the **Resources** table (primary vs derived, owner, when to read, provenance, how to use). **When to read** defaults to `if relevant`; mark a file `every time` only when a resuming agent can't work without reading all of it (`references/session-files.md` § When to read).

- **`## Context`:** What a fresh agent needs to understand the situation — background, facts, answers to questions that still matter. Keep it short; rewrite a fact when it changes and remove it once it no longer affects the work.
- **`## Goal / definition of done`:** Owns DoD. Rewrite in place; keep short and broad — closer to acceptance criteria than a task list, changes rarely, rough guideline of 1-5 bullets. Status `open` / `met-proposed` / `met-confirmed`.
- **`## Where we are`:** Status + next pointer only — no restated ask or DoD narrative. When the next step is done, suggest which `## Come back to` item looks next and ask before starting it.
- **`## Rules`:** Standing instructions for how to work in this session. A rule stays until the user drops it.
- **`## Come back to`:** Small sub-tasks of the DoD worth not losing — not full deliverable phases (`followups.md` is for work out of scope for this session entirely). New items go at the bottom and work starts from the top, unless the user says otherwise. `tidy-quest`'s Sweep applies promote-or-delete to the items its Checkpoint bears on; age in this list is not a signal.

**`timeline.md`:** Append one dated line only on durable changes (decision/resource/milestone / explicit "update for later"). Do not put rules or current truth here — permanent, never deleted by any skill at any point in the session's life.

**`followups.md`:** Real work explicitly out of scope for finishing *this* session — not this deliverable's own later phases. See `references/session-files.md` for the full "which later?" test; getting this wrong looks correct in either file at the time, so check that reference rather than guessing when the horizon is ambiguous.

**Legacy `session-notes.md`:** If a session still has `session-notes.md` and lacks `current-state.md`, on first touch **fold** any `## Current state` (or equivalent) into `current-state.md`; move leftover narrative into `timeline.md` as one dated block **or** rename to `session-notes.archive.md` as non-truth archive. Do not keep dual truth. Session-notes are never the home for Goal.

**Mid-session note-taking:** Prefer updating `current-state.md` (and a timeline line when durable). Do not treat session notes as an append-only debate log.

**Mid-session tasks:** When the user asks to "add a task" or "note that for later," hold it in context and include it at close-out. Do not park tasks only in `timeline.md`. If tasks accumulate and there's real risk of losing them before close-out, note them under `## Come back to` in `current-state.md`.

---

## `session.yml` fields

Sessions do not record **which machine, which tool, or what Claude cost/usage** they ran with. `session.yml` carries `slug`, `name`, `kind`, `started_at`, and the optional `forked_from` — nothing else. Do not ask for a starting cost or usage figure, do not ask "work or personal?", and do not add `source:` or `computer:` to any session file or capture frontmatter. Nothing reads them.

Older session folders may still carry `source:`, `computer:`, cost keys, `plan_slug`, `ticket_key` or `linked_sessions`, and may lack `name`. Leave them; they are history, not drift to reconcile. A project's settings may say how to read them.

## References

All in `${CLAUDE_SKILL_DIR}/references/`.

| File | Load when |
|------|-----------|
| `fork-protocol.md` | Fork mode triggers |
| `session-files.md` | Before writing session-dir files; routing a "for later" item |
| `curation-rules.md` | Fork, when writing the child's `current-state.md` (also loaded by `tidy-quest`) |
| `cold-read.md` | Fork, only if the child's restatement fails (also loaded by `tidy-quest`) |
| `current-state.md`, `timeline.md` | Templates the bootstrap script copies into a new session dir — not read by the agent |
