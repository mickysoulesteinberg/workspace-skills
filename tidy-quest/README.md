# tidy-quest

Brings an open quest's notes up to date, so the next chat can pick up from them. Use it when you're about to stop for the day, before a risky change, or whenever the notes feel behind.

Needs [`quest`](../quest/README.md) installed beside it.

## How to use it

Type `/tidy-quest` in the chat where the quest is open. To stop for the day, say so:

```
/tidy-quest I'll pick this up tomorrow
```

You can also just say you'll pick the quest up later, and the agent may run it for you. It won't start on its own just because a chat seems to be winding down.

## What it checks

`tidy-quest` has five checks. The agent runs the ones the moment calls for and tells you which ran.

| Check | Question it answers |
|-------|---------------------|
| **Checkpoint** | Is everything decided so far actually written down, or only said in the chat? |
| **Sweep** | Does `current-state.md` still read clearly, with nothing out of date or contradictory? |
| **Reconcile** | Is each file the other checks just wrote to listed in the notes' file table? |
| **Confirm** | Is the "next step" in the notes still the real next step? |
| **Cold read** | Could someone with no background follow the notes? |

**Stopping for the day** runs the first four in that order, then offers the cold read and says why it might be worth it. In a cold read, a second agent that hasn't seen your chat reads only the notes and says back the goal and the next step, so you can see what a newcomer would take away. You can say no.

## What it changes

Only files in the session folder. It rewrites `current-state.md`, adds lines to `timeline.md`, and may add to `followups.md` or to the files the quest is producing. For files you're writing yourself, it suggests text instead of editing them. It never deletes files: deciding what to keep is [`close-quest`](../close-quest/README.md)'s job, at the end.

## Settings

It follows the same project settings as `quest`. See [settings](../docs/settings.md).
