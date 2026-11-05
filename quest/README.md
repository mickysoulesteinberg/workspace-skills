# quest

Starts a piece of work that will take more than one chat, or picks one back up. The agent keeps the quest's notes in a **session folder** inside your project, so a new chat can read them instead of starting from nothing.

Part of a set with [`tidy-quest`](../tidy-quest/README.md) and [`close-quest`](../close-quest/README.md). For how the three fit together, see [How a quest works](../README.md#how-a-quest-works).

## Start a quest

Type `/quest` in the chat, followed by what the work is:

```
/quest reorganize the docs folder
```

You can also ask in your own words ("let's make this a quest"), and the agent may start it for you.

The agent creates `logs/agent-sessions/_current-<MMDD>-<name>/` in your project (month and day of the start), names it after the topic when that's clear (or a random two-word name when it isn't), and tells you the name. It writes the goal into `current-state.md` and carries on with the work.

If you have several projects open, the agent puts the folder in the project the work belongs to and tells you which one it picked.

## Pick a quest back up

In a new chat, type `/quest` followed by the quest's name or the folder's path:

```
/quest reorganize-docs
/quest logs/agent-sessions/_current-1102-reorganize-docs
```

The agent reads `current-state.md` and tells you in its own words what the goal is and what comes next. Check that it matches what you meant before going on.

Plain `/quest` with no name always starts a new quest, even when one is already open.

## What's in the session folder

| File | What it holds |
|------|---------------|
| `session.yml` | The quest's name and when it started |
| `current-state.md` | Where things stand now: background, the goal, the next step, rules you've set for this work, a short list of smaller things to come back to, and a table of the files that matter. The agent rewrites it as things change |
| `timeline.md` | One dated line for each decision or milestone. Lines are only ever added |
| `followups.md` | Real work that came up but is outside this quest altogether. Later steps of this quest's own work go in `current-state.md` instead. Only created when needed |

Anything the agent produces along the way, such as drafts, query results, or notes you ask it to keep, goes in this folder too, until `close-quest` decides where each file ends up.

## Split off a tangent

When a side topic deserves its own quest, say so mid-chat: "split this off into its own quest." The agent creates a second session folder for it, moves over the files that belong to the tangent, writes the new quest's notes, and records which quest it came from. You carry on with the original quest in the current chat, and open a new chat for the new one when you're ready.

## Things to know

- **Notes go to the folder, not to the agent's memory.** "Remember this" while a quest is open writes it into the session folder.
- **Settings.** A project can change how quests are named and found. See [settings](../docs/settings.md).
- **Needs Python.** `quest` runs a small script to create the folder, so `python3` must be installed.
