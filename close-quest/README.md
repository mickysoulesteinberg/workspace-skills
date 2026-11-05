# close-quest

Wraps up a finished quest. It turns the session folder into a dated record with a summary you've approved, and decides with you what happens to each file the quest produced.

Needs [`quest`](../quest/README.md) installed beside it.

## How to use it

Type `/close-quest` in the chat where the quest is open, or give it the quest's name: `/close-quest reorganize-docs`. **(Claude Code)** It only runs when you type it; other tools may differ.

## What happens

1. **The agent reviews the quest:** what was done and decided, which files were created or edited, and anything still open.
2. **You decide what happens to each file** (first stop). The agent suggests one of these for each file in the folder and waits for your OK:

   | Choice | Meaning |
   |--------|---------|
   | Keep | It's a record of this work; it stays in the folder |
   | Delete | Never used, or a copy already lives somewhere permanent |
   | Summarize, then delete | A large or temporary file that taught you something; the finding goes in the summary |
   | Move out | It belongs somewhere permanent, or some other piece of work will need it |

   Obvious deletes come as one yes-or-no.
3. **You approve the summary** (second stop). The agent shows the full draft: a title, a one-line summary, what was done, open tasks, and the files created and edited. It also lists any tasks elsewhere in your project that this quest finished, offering to mark them done.
4. **The agent writes it.** It removes the working notes (`current-state.md`, `session.yml` and `followups.md`), renames the folder from `_current-1102-reorganize-docs` to a dated name like `20261102-0930-reorganize-docs` (full date and time from when the quest started), and writes the summary inside. `timeline.md` stays. Then it marks done the tasks you approved and runs any after-write steps from your settings.

Nothing besides the files you confirmed in step 2 changes until you approve the draft in step 3. It doesn't make a git commit unless you or your settings ask for one.

If you split off a tangent from this quest earlier, the agent updates the tangent's link back to it. When it can't tell which tangent is meant, it asks.

## Adding your own steps

A project can add to `close-quest`: extra fields or sections in the summary, files to delete every time, or steps to run after the summary is written, such as adding a line to a changelog. The draft says which additions ran, so you can see if one was skipped. See [settings](../docs/settings.md).
