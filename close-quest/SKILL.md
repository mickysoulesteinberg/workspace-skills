---
name: close-quest
description: Closes a quest by turning its session directory into a dated log with a summary, after deciding what happens to each file.
disable-model-invocation: true
---

# /close-quest — Close a quest

Finalizes the session directory `quest` created and `tidy-quest` maintained. The summary this skill writes replaces `current-state.md` as the quest's record. `timeline.md` stays permanently.

**Status:** still being fitted to projects. When an instruction here doesn't fit the project you're in, ask the user rather than guessing.

**Shared files** live in the `quest` skill's folder, `${CLAUDE_SKILL_DIR}/../quest/references/`. This skill is installed next to `quest` and only works alongside it.

**A run has two stops:** confirming file dispositions (Step 3) and approving the draft (Step 4). Step 3 applies only the dispositions the user confirms; nothing else is written until the draft is approved.

## Project settings

A project can change this skill in two files under `$ROOT/.agents/skill-settings/`, both optional:

- **`quest.md`**: settings shared by `quest`, `tidy-quest` and this skill, such as who the user is or how links are written. They apply throughout.
- **`close-quest.md`**: this skill's own additions, under three headings. Read each section at the step that names it, not before:
  - **`## Overrides`**: changes to this skill's defaults, such as local time, extra files to delete by default, or the task-line format. Read in Step 1; they apply throughout.
  - **`## Draft additions`**: extra frontmatter, extra summary sections, and items the user should see and approve in the draft. Read in Step 4.
  - **`## After write`**: things to do elsewhere once the summary exists. Read in Step 5.

A section may point to another file for a long procedure; open it when its section is reached. These three headings are the contract a project relies on, so their names and the steps that read them stay stable.

---

## Step 1 — Find the session and its settings

`$SESSION_DIR` is the path or name the user gives, or the `_current-*/` dir `/quest` started or resumed in this conversation. A lone `_current-*/` dir is not evidence: it may be another chat's live quest, and Step 5 moves and finalizes it. If neither applies, ask which one.

`$ROOT` is the folder above `$SESSION_DIR`'s `logs/agent-sessions/`. Read `$ROOT/.agents/skill-settings/quest.md` if it exists, and the `## Overrides` section of `close-quest.md` if that exists. A missing file means no settings of that kind.

---

## Step 2 — Synthesize (no output yet)

From the conversation, `current-state.md`, and `followups.md` if present, work out:

- The goal, what was done and decided, and the status.
- **Files created and files edited** during the quest.
- **Tasks:** each item still open under `current-state.md`'s `## Come back to`, each `followups.md` entry, and any other unresolved next step. Skip a task that already exists as an open task in a file you've read, and skip anything the quest finished.
- **Tasks finished elsewhere:** open tasks in the project that this quest clearly resolved. Search the project's files for open tasks in the form its own notes use, or as the overrides say. Be conservative; when in doubt, leave one out.

Read `timeline.md` only to resolve a contradiction. Carry an item from `current-state.md`'s `## Rules` into the summary only if it explains a decision recorded there.

---

## Step 3 — Decide what happens to each file

`timeline.md` stays. `session.yml`, `current-state.md`, legacy `session-notes.md` and `followups.md` are replaced by the summary, and Step 5 deletes them, after the draft is approved. Add any files the overrides list as default deletes, and leave out any files they exclude from this step.

Each other file in `$SESSION_DIR` gets one of these dispositions:

| Disposition | Use when | What happens |
|-------------|----------|--------------|
| **Keep** | A record of what happened in this quest, not duplicated elsewhere | Stays in the session dir |
| **Delete** | Never used or abandoned, with no findings; or a durable copy already exists elsewhere | Removed. If a durable copy exists, the summary links to that copy, not to both |
| **Summarize, then delete** | A dump or intermediate that produced findings | The finding goes in the summary, then the file is removed |
| **Move out** | A durable home exists, or the file is input for work that hasn't happened yet | Moved there, and the summary links to it |

Recommend a disposition rather than asking open-endedly:

1. Batch the obvious deletes into one confirmation, recommending yes: default deletes, durable duplicates, and files that were never used.
2. Show `.csv` and `.tsv` files, result dumps, and any file of 100KB or more in a table: path, size, recommended disposition.
3. Ask about the real judgment calls. If a file's fate isn't clear, ask now; there is no "undecided" state.

⛔ **Stop** until the user confirms, then apply the confirmed dispositions.

---

## Step 4 — Show the draft

Read the `## Draft additions` section of `close-quest.md`, if there is one, and carry out each item as you build the draft.

Propose a descriptive kebab-case slug. The final location is `$ROOT/logs/agent-sessions/YYYYMMDD-HHMM-<slug>/`, using the date and time from `started_at` in `session.yml`, converted from UTC to the user's local time. Show the full summary, which is `YYYYMMDD-HHMM-<slug>.md` in that folder:

```markdown
---
type: agent-session
title: [Title]
datetime: YYYY-MM-DDThh:mm
datetime_end: YYYY-MM-DDThh:mm
tldr: "[One sentence, specific enough to be useful out of context]"
---

# [Title]

## Summary

[2–4 sentences: what was worked on, what was decided, current status]

## What We Did

- [Key step or finding]

## Tasks

- [ ] [One sentence: what to do, and enough why to understand it without reading this file]

## Continuing

[Where things stand and what's next]

## Artifacts

- [File created, linked to wherever it lives now]

## Files edited

- [File] — [what changed]
```

Omit any section with nothing in it, and omit Continuing when the work is complete. `datetime_end` is the current local time; don't ask for it. Use `- [ ]` only for real tasks, because tools that read tasks treat every checkbox as one. Keep the summary tight: it's an entry point for later, not a transcript.

Below the summary, list:

- **Tasks to close elsewhere** from Step 2, each with its file, if any.
- **Supplement applied:** the draft additions you carried out, or "none" when `close-quest.md` has no such section. This shows the user whether the project's additions ran.
- **To weigh in on:** anything the user might want to weigh in on before closing, such as a question that never got a clear answer, if any. Flag it rather than assume it doesn't matter.

⛔ **Stop.** Ask "Does this look right?" and wait for approval. The approval covers the summary, the tasks to close, and every item the draft additions put in front of the user.

---

## Step 5 — Write

1. Note `session.yml`'s `slug` for item 4, then delete `session.yml`, `current-state.md`, `session-notes.md` and `followups.md` from `$SESSION_DIR`, whichever exist.
2. Rename `$SESSION_DIR` to the final location. The new name uses the descriptive slug from Step 4, not the slug in `session.yml`.
3. Write the summary into the final location.
4. **Repoint live forks.** Search every open `$ROOT/logs/agent-sessions/_current-*/session.yml` for a `forked_from` naming this session: the bare slug, or a path ending in `/_current-<slug>`. For each such hit, set its `forked_from` to this session's final location, written as the project's settings say links are written (a path relative to `$ROOT` otherwise), and report it in one line. No hits is the common case; say so in one line.
5. Mark done the tasks elsewhere the user approved, in the project's task format.
6. Read the `## After write` section of `close-quest.md`, if there is one, and carry out each item.

Report the final location, what's in it, and what each after-write item did. Don't commit unless the project's settings or the user say to.
