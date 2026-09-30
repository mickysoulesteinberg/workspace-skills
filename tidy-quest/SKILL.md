---
name: tidy-quest
description: >
  Mid-session maintenance for the session directory quest creates and a close-out skill later
  finalizes. Five passes, each with its own trigger and cost: Checkpoint (write down what has been
  decided), Sweep (curation rules and coherence), Reconcile (Resources rows), Confirm (is the stated
  next step true), and an opt-in cold read for when the file is about to be left for a stranger.
when_to_use: >
  Manual only. Use for /tidy-quest, or when the user says they'll continue the quest later and want
  a clean hand-off. NOT for starting, continuing or forking a session (quest) or closing one out.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../quest/scripts/session-bootstrap.py *)
---

# /tidy-quest — Session directory maintenance

`quest` creates `current-state.md` + `timeline.md` at session init. A close-out skill reads them once, at the very end. Nothing maintains the session dir *during* the session except this skill — that's the missing piece it fills.

`current-state.md` is this skill's file to curate. `timeline.md` is not: this skill appends to it and never curates it, because curating a history would empty it — the promote-or-delete test asks whether an item could still change future work, and a record of something that already happened can never pass.

**Status:** still being fitted to projects other than the one it was built in. When an instruction here doesn't fit the project you're in, ask the user rather than guessing.

**Shared files** live in the `quest` skill's folder, `${CLAUDE_SKILL_DIR}/../quest/references/` — this skill is installed next to `quest` and only works alongside it. Resolve `$SESSION_DIR` the way `quest` does: from a path, or a session name the user gives.

**Project settings.** Before any pass, print the project's settings and follow them. `$ROOT` is the folder above `$SESSION_DIR`'s `logs/agent-sessions/`:

```bash
python3 ${CLAUDE_SKILL_DIR}/../quest/scripts/session-bootstrap.py --root "$ROOT" --show-settings
```

They override this skill's defaults, the same way they do for `quest`. No file means the defaults apply unchanged.

## Not this skill

| Need | Go instead |
|------|------------|
| Start or continue a session dir, or fork one mid-session | `quest` |
| Close out / archive a finished session | the project's close-out skill, if it has one (its settings may name it) |
| Decide what survives — deletes, promoted duplicates, archival | the close-out skill |

**Mid-session nothing is deletable**, because the work is still live, so this skill never runs artifact triage.

## What can be wrong, and what checks it

Three properties. Coherence and legibility are one of them — comprehensibility — checked two ways, and the difference is who reads.

| Property | Check | Catches | Cannot catch |
|---|---|---|---|
| **Durability** — is what we decided written down at all | Checkpoint | an hour of decisions living only in the conversation | anything about what is already on disk |
| **Truth** — is what is written still true | Confirm | a next step that is already done, or that recent work contradicts | prose nobody can parse |
| **Comprehensibility** (weak) | Sweep — `/coherence-check`, same agent, own file | structural defects: undefined shorthand, a section doing two jobs, on-page contradictions | missing context — it fills gaps from memory |
| **Comprehensibility** (strong) | Cold read — different agent, no shared context | missing context | truth; it will restate a false claim accurately |

Ranked by what it costs when it fails, durability is first and comprehensibility is last. Run them in that order.

## Passes

Each pass has its own trigger and its own cost. They are not a fixed bundle — run the ones the moment calls for.

| Pass | Checks | Cost | Fires |
|---|---|---|---|
| **Checkpoint** | durability | seconds — no rules pack, no subagent, no full re-read | often; on request; before anything risky |
| **Sweep** | comprehensibility (weak) | cheap | when Checkpoint wrote something |
| **Reconcile** | every file a pass wrote to has a Resources row | seconds | when a pass wrote to a file |
| **Confirm** | truth | cheap | stopping, forking |
| **Cold read** | comprehensibility (strong) | one read-only agent spawn | **opt-in** — offered, never automatic |

**Stopping for the day** runs Checkpoint → Sweep → Reconcile → Confirm, then *offers* the cold read with its reason stated. That is the only named combination.

**The user invokes this skill.** It never fires itself on a judgement that the session looks like it is winding down.

## Checkpoint

The durability pass. Reads nothing, loads no pack, spawns nothing. Works from **what is live in the conversation**, not from the file — that is the whole point, because the file is what is missing things.

1. **Enumerate the commitments** made since the last Checkpoint. A commitment is something that, if lost, would have to be redone or re-decided:
   - a decision (we are doing X, not Y)
   - a finding (X turns out to be true; Z is verified)
   - an open question held for the user

   Not commitments: options listed but not picked, reasoning en route, anything already on disk, and work simply performed — the work is its own record.

2. **Route each one.** This is a lookup, not a judgement call:

   | The item… | Home |
   |---|---|
   | is a fact needed to understand the situation — background, a finding, an answered question | `current-state.md` → Context |
   | changes what "done" means | `current-state.md` → Goal / DoD |
   | changes what happens next | `current-state.md` → Where we are |
   | is a standing rule for the rest of the session | `current-state.md` → Rules |
   | is a sub-task not to lose | `current-state.md` → Come back to |
   | is content of a thing being written | that deliverable |
   | is a fact about an external file | `current-state.md` → Resources row |
   | is work out of scope for this session entirely | `followups.md` (`session-files.md` carries the "which later?" test) |

   **The scope of this pass is the union of those homes** — nothing else is touched. Zero items means nothing is in scope and the pass is over in seconds. That is a successful outcome, not a failed one; say so and stop.

3. **Write into deliverables, not just `current-state.md`.** A deliverable's own content belongs in it. An agent does not rewrite the user's deliverables — but that rule protects their **authored** content from agent edits, and a decision the user and the agent just agreed to is not authored content, it is content the file is missing. How it lands depends on the file's declared ownership: `agent` files are written directly, `user` files get the proposed text surfaced and never a silent edit. `session-files.md` § Ownership carries both rules in full.

4. **Log one line to `timeline.md`**, matching its append-only convention:

   ```
   2026-09-09 14:32 — Checkpoint: 4 items → current-state (Rules, Come back to), proposed-doc-rules.md
   ```

   Naming the homes, not the items, keeps the line short while telling a resuming agent where to look. **A resumed or compacted session** — the one case where the agent was not present for the work — reads back to the most recent such line and enumerates from there.

5. **Report what was written down.** The check has to be visible, or it is indistinguishable from not having run.

## Sweep

Runs `curation-rules.md`, scoped per rule. The rules do not all cost the same, so they do not all get the same scope.

**`current-state.md` gets whole-file treatment whenever any of its sections were touched.** At ~50 lines it is cheap to take whole, and taking it whole is what catches a contradiction between two sections Checkpoint wrote to separately.

| Rule | Scope | Why |
|---|---|---|
| `/coherence-check` | whole of `current-state.md` when any section was touched | cheap on a 50-line file; catches cross-section contradictions |
| shorthand-grep | whole file, always | it is a grep |
| one-home check | the homes Checkpoint wrote to | duplication can only be introduced by a write |
| narrative compression, rewrite-stale-framing | text that changed | nothing else moved |
| promote-or-delete on open items | items Checkpoint's enumeration bears on | the one genuinely expensive rule — it judges every open item individually |

Log promote and delete outcomes to `timeline.md` per `curation-rules.md`. Never sweep `timeline.md` itself.

### Surfacing an open item — the invalidation test

Surface an open item when the session's own progress has made it **wrong, orphaned, unreachable, or newly blocking**.

**Time in the queue is not a reason to raise anything.** A queue is a plan the user already sequenced; items sit in it unreached by design. Reporting an item's age turns the pass into a nag and costs the user a turn to say "not yet" about work they deliberately ordered — and surfacing on age trains them to dismiss the surfacing altogether. This applies to any open-item list, not only `## Come back to`.

When there is an actual question, give the context needed to answer it and ask it. Do not narrate queue status and leave the question to be found inside.

## Reconcile

Every file a pass wrote to has a row in `current-state.md`'s Resources table, carrying its **ownership**. `session-files.md` § Ownership defines the values and how to default them — read it there rather than from a copy.

**The bar is "written to," not "exists."** `quest`'s `current-state.md` template asks for a row for every durable artifact and in practice that is not what happens — live sessions carry files that never got one. So this pass does not reconcile the directory against the table. It requires a row for every file a pass has actually written to, which needs no separate mechanism: updating the row is part of the write.

Files nobody is maintaining stay undeclared, which is an accurate description of them. The cost is that this pass says nothing about whether the directory as a whole is accounted for.

Each row also says **when to read** the file; `session-files.md` § When to read defines the values. New rows default to `if relevant`. Check each row marked `every time`, not only new ones: does a resuming agent need the whole file each time? If only a small part of a large file matters, propose summarizing that part in Context and switching the row to `if relevant`; change it only once the user agrees.

## Confirm

The truth check. A legible file and a true file are different properties — a `current-state.md` that stated "nothing is blocking drafting" passed a cold read cleanly while being wrong about the phase the work was actually in. The reader restated the claim accurately; the claim was false.

A bare "does this look right?" does not fix this. It is the same self-report that already failed once, asked at the exact moment the user is tired and stopping for the day, which is when a skim-and-confirm is most likely.

1. Pull the stated next step from `current-state.md`'s Goal / Where we are.
2. Read the last handful of `timeline.md` entries and note which file in `$SESSION_DIR` was most recently touched.
3. Compare. A next step that is already done, or that points somewhere the recent activity does not support, is a mismatch.
4. **Mismatch:** surface it concretely — "Goal says next is X; the last few `timeline.md` entries and the newest file in the dir are about Y" — and ask the user to resolve it. Fix `current-state.md` to match their answer.
5. **No mismatch:** do not interrupt the user with a routine confirm. The check passed silently, the same way a passing test does not announce itself.

## Cold read

`cold-read.md`. This skill's declared question: **what is the current goal, and what is the next step?** Hand over `current-state.md` alone — no other session files.

**Opt-in.** Offer it with the reason stated rather than firing it or waiting to be asked — "eleven items landed this pass and three of them only exist in prose I wrote; worth a cold read before you stop?" The item count from Checkpoint is the signal: two items do not need it, eleven probably do.

Run it **after** every pass that can still edit `current-state.md`. It is the most expensive step available here, so an edit landing behind it costs a second full spawn, not just a stale verdict.

## References

All in `${CLAUDE_SKILL_DIR}/../quest/references/`.

| File | Load when |
|------|-----------|
| `curation-rules.md` | Sweep |
| `cold-read.md` | Cold read only — it is opt-in, so do not load it by default |
| `session-files.md` | Checkpoint, when routing a "for later" item — carries the test for which kind of "later" it is; Reconcile, for ownership values |
