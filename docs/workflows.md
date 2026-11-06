# Example workflows

**These are suggestions, not instructions.** Each skill works on its own (apart from the quest skills needing `quest` installed). Use whichever pieces help, in whatever order suits you. For how a quest works step by step, see [How a quest works](../README.md#how-a-quest-works).

## Light touch: start and finish

For work that takes two or three chats and doesn't need much upkeep.

1. `/quest` and say what the work is.
2. Work across as many chats as it takes, resuming each time with `/quest <name>`.
3. `/close-quest` when it's done.

Skip `/tidy-quest` entirely. The cost is that a new chat may have to work harder to catch up, because nothing has checked that the notes are complete and current.

## The long haul: tidy before every pause

For work that stretches over a week or more, or that you might hand to someone else.

1. `/quest` to start.
2. Before each break, `/tidy-quest I'll pick this up tomorrow`. Ask for a cold read before a long break, or before handing the work to someone else, if tidy-quest didn't run one. In a cold read, a second agent that hasn't seen your chat reads only the notes and says back the goal and next step, which shows whether a stranger could follow them.
3. Each day, `/quest <name>` in a fresh chat. Check the agent's summary of where things stand before carrying on.
4. `/close-quest` at the end.

## Following a tangent without losing the thread

When a side question turns out to deserve real work of its own.

1. Mid-chat, say "split this off into its own quest." The agent creates a second session folder for the tangent, with its own notes.
2. Keep going on the original quest in this chat.
3. When you're ready, open a new chat and type `/quest <tangent's name>` to work on the tangent.
4. Close each one separately with `/close-quest` when it's done. If you close the original first, the agent updates the tangent's link back to it.

## Checking writing before it goes out

No quest needed.

1. Draft the email, proposal, README, or handoff note.
2. Ask "sanity check this before I send it." `coherence-check` lists what a cold reader would trip on.
3. Fix what you agree with, or say "clean it up" to have the agent make the fixes.

## Writing your own skill

1. Describe the skill you want: "Create a skill that drafts my weekly status update." `skill-author` shapes it.
2. Its last step runs `coherence-check` on each file, so the instructions make sense to an agent that has only those files.
3. If designing the skill takes more than one chat, you could run it as a quest, so the design decisions end up in the notes.
