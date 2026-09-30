# Fork Protocol

Triggered mid-session — a `_current-*/` dir is already live and being worked in, and the user says something like "go ahead and fork," "split this off," "let's make this its own session." Splits a barely-related tangent into its own session, so the origin stops accumulating work that no longer belongs to it.

Fork is mechanical plus editorial. The mechanical half — make the dir, write provenance, move files — is this skill's own job, same tools as Bootstrap. The editorial half is writing the new session's `current-state.md` for an agent holding none of this conversation.

**Neither session is curated by this protocol, and `tidy-quest` is not invoked on either.** The child's `current-state.md` is written here, by an agent holding full context, so there is nothing stale in it to sweep. The origin does not need curating because the user continues working in it with that same context and can tidy when they choose.

The consequence to accept, rather than fix: the origin keeps pointing at work that walked out the door. That is harmless while the user is live in it. It matters only if they later stop for the day without tidying — which is what `tidy-quest`'s own end-of-day pass is for. Do not add an origin-side pass here to close it.

## Steps

1. **Confirm scope.** If it isn't already clear from what the user said, confirm what specifically is forking off — the tangent, not the whole session.

2. **Propose a descriptive slug** for the new session, drawn from the tangent's actual topic — same judgment as Bootstrap's descriptive-slug detection (including any naming rule in the project's settings), but naming the fork's topic, not the origin's. No extra approval prompt needed for the name itself.

3. **Run bootstrap** with `--root <project> --slug <new-slug> --forked-from <origin path>`. The origin path is the origin's folder, prefixed with its project folder's name (e.g. `my-project/logs/agent-sessions/_current-1508-foo`). The child goes in the same project as the origin unless the user names a different one; if it's a different project, print that project's settings first (Bootstrap's **Project settings** step). This creates the new `_current-*/` dir and writes `forked_from` into its `session.yml`.

4. **Note the fork in the origin's `timeline.md`:** one dated line naming the child's folder, with its project when that differs from the origin's (e.g. `- 2026-03-14 — Forked the API cleanup into <project>/logs/agent-sessions/_current-1508-api-cleanup/.`). See "Where a fork came from" below.

5. **Move artifacts.** Move whatever obviously belongs with the fork into the new `$SESSION_DIR` now — a durable relocation, not a duplicate copy, done as a quick pass. Ask the user directly on anything unclear rather than guessing or deferring it — the fork is happening because a real decision is already being made, and **nothing downstream cleans up after this step.** No later pass re-triages either session until each session's own close-out. Overlap between the two sessions is fine: each artifact goes wherever it's needed. There is no fork-versus-stay rule to apply beyond that.

6. **Write the child's `current-state.md`.** The editorial half: Context, Goal, Where we are, Rules, and Resources, drawn from what is forking off. Context names the origin: its folder, and its project when that differs from the child's. Load `curation-rules.md` (in this folder) for the writing conventions.

   **Before writing it, scan the origin's own open-item files** — its backlog / improvements / followups files, whatever they are named — for items whose subject falls inside the fork's stated scope, and carry those forward as named candidate work. A fork's scope is everything the origin session *knew* that belongs to it, not only the items its prose happened to call out. Nothing downstream catches a miss here: the check in step 7 tests whether a cold reader can state the goal and next step, not whether the scope list is complete.

7. **Have the child state it back.** The child agent reads the `current-state.md` it did not write and states the goal and the next step, as if about to continue the work. This is the fork's version of `cold-read.md` (in this folder) — weaker, and free.

   It is weaker because the child holds this fork conversation: what moved, what scope was confirmed, why the split happened. But it is not the author self-grading either — **author ≠ reader** is the property the check turns on, and what the child lacks is exactly the hours of origin work the author would unconsciously fill gaps from. Acceptable here because the user is live and a bad answer costs one turn.

   **If the child's answer comes back wrong or hedged, run the real thing** — `cold-read.md` with a read-only agent spawn — rather than patching the file by hand.

8. **Report the new session's ID** to the user, the same way Bootstrap does.

## After fork — origin session default

When a fork completes, **stay in the origin session** and continue its work in this chat. The user opens a **new chat** themselves when they're ready to work the fork — do not switch context to the child here, and do not offer "do the fork work here vs continue triage" as equivalent options.

**Agent closing line:** report the fork session ID, note what the fork owns, state the origin's **next step** — then proceed (or wait on the user) on origin work only.

## Where a fork came from

A fork is recorded three ways: the child's `session.yml` `forked_from` names the origin's folder (step 3), the child's Context names the origin in prose (step 6), and the origin's `timeline.md` names the child (step 4). None of them is updated later. When either session is closed out and its folder renamed, the pointers to it go stale but stay readable — the slug inside each one still identifies the session — and that is accepted.
