# Curation rules for current-state.md

These are the rules behind "keep current-state.md trustworthy." Apply them every time a caller touches the file: lightly for a single-item touch, fully for a whole-file sweep. Most govern `current-state.md`'s core sections — Context, Goal, Where we are, Rules, Resources, Come back to — but a few reach wider: what gets logged to `timeline.md`, and where in the session directory a given piece of work is allowed to live.

Consumers: `tidy-quest` (every run), and `quest`'s fork mode when writing a new session's `current-state.md`.

## Opens with context, goal and next step

`current-state.md` should open with the context a fresh agent needs, then the current goal and the next step. That's the first thing a resuming agent sees — it shouldn't have to read the whole file to find out what's actually going on right now. Keep Context short so it doesn't bury the goal and next step.

## The promote-or-delete test

For every item: **could this still change future work in this session?**

- If no — delete it outright. Don't preserve it by softening it into a lesser note "just in case." That instinct — downgrade instead of delete — is the actual failure mode these rules exist to stop, not a hypothetical risk.
- If yes, and it just got answered, and the answer still matters going forward — promote the answer into Context (or into Rules, if it's a standing instruction) and delete the open-item line. There's no separate "resolved" tag or convention for this; it's just promote, then delete.

**When the test itself is unclear, ask — don't invent a third status.** If you can't confidently answer whether an item could still change future work, stop and ask the user. These skills run synchronously with the user in the loop; there is no reason to hold an item in an undecided "flagged" state waiting for a later pass. Get the answer, then apply whichever branch — promote or delete — it implies, immediately. Nothing about an ambiguous item persists in the file once it's been asked about.

**Applies to every item in every open-items list** — `## Come back to` foremost — walked start to finish each sweep, not only entries an edit happens to bring into view. A list that was fully curated once still needs the same full walk next time; it doesn't stay curated on its own.

**Log the outcome to `timeline.md`** — both branches. One dated line per touch for a single-item update; one dated block per sweep for a whole-file pass, not one line per item. Deletes matter more here than promotions: a promoted fact is still sitting in Context or Rules where a reader can question it, but a deletion leaves nothing behind, so a reader can't know to ask. Record what was removed and the basis for removing it, not just that something was. Name it the way it's named everywhere else in the session — a stray reference to X is only resolvable against a log that says "X" in the same words, and "narrowed scope per the morning's discussion" is unsearchable by whoever is holding the stray token. This is not the downgrade the rule above bans: that ban is about keeping a hedged remnant in `current-state.md`, where it competes with live truth. An append-only file nobody opens unless they're troubleshooting doesn't do that.

**A dropped scope isn't promotable.** "We're no longer doing X" is not current truth, it's the absence of one. Remove every reference to X from `current-state.md` and log the drop — don't promote it into Context on the grounds that it "prevents future work," which is the softening instinct wearing a promotion badge. The one exception is a live carve-out: where a positive scope statement would otherwise read as including X, "scope is XYZ, excluding X" is current truth and stays. The phrasing is the test — a property of the current scope stays, a record of a past choice goes to the timeline.

## Sweep for what a new decision makes moot

When a decision gets recorded — on a single-item touch (the one thing that just happened) or a whole-file sweep (everywhere) — check whether it silently orphans something else nearby. A rejected option can leave behind a related open question that only existed because of the now-rejected option. This is easy to miss because it's not where you're looking when you make the decision.

Because that miss is expected, `timeline.md` is the backstop. When you find a reference that contradicts current truth, or that looks orphaned with no live item behind it, read the log before deciding what to do with it. A dropped scope and an under-recorded live one look identical in `current-state.md`; the log is what separates them. If it records the thing as dropped, delete the stray outright — that's a confirmed removal, not a judgment call, and it needs no new entry of its own.

## Narrative sections aren't a second timeline

A "Where we are" section that gets one more dated paragraph added each time you touch it is turning into `timeline.md`, just duplicated. Compress or drop older material each time you run a whole-file sweep — the point of `current-state.md` is what's true *now*, not a history of what became true when.

The same applies to `## Goal / definition of done`. Goal/DoD is closer to acceptance criteria than a task list — it can change, but rarely, and stays broad: a rough guideline of 1-5 bullets naming what success looks like, not how to get there. Small sub-tasks belong in `## Come back to`, not stacked under Goal. A dated "Resolved" sub-list or a numbered sequence of completed steps growing under Goal is the same drift as a growing "Where we are" — compress or delete it on every sweep, don't let it accumulate.

## Rewrite in place, don't append a correction

When a framing turns out wrong or too broad, rewrite it to say the corrected thing — don't leave the old line and bolt a correction note next to it. Appending feels safer under time pressure, but it's exactly how the file turns into archaeology. (`timeline.md` is the one place a correction *is* a new dated entry — see its own conventions.)

A passage that explains itself by naming what it supersedes or replaces is the same smell wearing different clothes — it means two paragraphs are doing one paragraph's job. Rewrite the current-truth paragraph standalone, with no reference to the old one, and delete the superseded passage outright (or move it to `timeline.md` if the change itself is worth a record). Never leave both, cross-referencing each other.

## Grep before coining shorthand

Before using a shorthand code or a named artifact ("outcome D," "the working packet"), check whether it's actually defined anywhere in the session's own files. If there's no durable definition, spell it out instead of inventing a new abbreviation nobody wrote down. A term that felt obvious while you were writing it is not obvious to whoever reads it next.

The same check applies before deleting on the grounds that another file is already the source of truth for a fact: grep that file and confirm the specific fact is actually there before removing it from `current-state.md`. "File X is SoT for this" describes intention, not verified state.

## Context and Rules shrink too

Remove a fact from Context once it no longer affects the work. A rule stays in Rules until the user drops it. A change that's decided but not yet made is neither: it's a Come back to item marked *approved, not yet applied*, and it leaves that list when it's done. The promote-or-delete test above governs what comes *into* Context and Rules; these are the matching exit conditions.

## Don't track git-state mechanics

Commit hashes, `git diff --stat` counts, and claims like "everything is uncommitted" go stale the moment someone commits outside the conversation, and git already tracks them authoritatively. Describe what's true about the *work* — resolved, verified, blocked — never the repo's commit/diff mechanics. If commit state matters to a live decision ("don't force-push, there's committed work here"), that's a git check at the moment it matters, not a standing note.

## Every file and folder is defined

Every file or folder in the session directory needs to be identifiable from inside the directory itself — a subdirectory needs a short README naming what's in it and why. A resuming agent shouldn't have to open every file to find out which ones matter.

## One body of work, one home

A given piece of work is recorded in exactly one place. Never write an entry that restates a step already in the recorded goal or plan — point at the plan instead. When a plan step and an open-items list both describe the same work, the open-items list is the single home and the plan step points at it, not the reverse.

This failure is invisible from where you're writing: you're looking at one list, it looks incomplete, so you add the item — and the reader who checks the *other* list finds a partial answer and trusts it. Before adding a work item anywhere in the session directory, search for the work, not for the wording you were about to use.

## Deliverables get their own file

A plan, PRD, or other work product being drafted this session — including its own internal open questions or options — belongs in its own file from the start, not inlined into `current-state.md`. `current-state.md` links to it as a Resource and tracks only session-level status about it ("drafting PRD §2, blocked on X"), never its content. If a section's real content turns out to be a deliverable, that's a curation item on its own — split it out.

## Cite your sources and your basis

A claim resolved by external research needs its actual source cited at the claim, not just the conclusion — the conclusion alone reads as more certain than it is. An estimate needs its basis and what would move it, stated at the point of the claim. When something is checkable against a live system or the real code, check it live rather than reasoning from memory or a cached doc — inherited assumptions are wrong often enough that they're worth re-verifying, not trusting by default.

## Pre-close checklist doesn't accumulate crossed-off items

The list of things that need to happen before this session can close should only ever contain things that still need to happen. When something's done, it doesn't stay on the list checked off — it's either deleted outright, or, if it's worth remembering, promoted into a Decision the same way any other resolved item would be.

## Status tags on open items, not just prose

An item that's still open needs an explicit status — *undiscussed*, *needs a decision*, *approved, not yet applied* — not just descriptive prose. "Proposed fix: X" reads identically whether the fix is greenlit or was never even discussed; a cold reader can't tell the difference without re-deriving it from a conversation they weren't part of.
