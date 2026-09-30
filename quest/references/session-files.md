# What each file in a session directory is for

A quick reference so an agent that has loaded only one of `quest` / `tidy-quest` / a close-out skill still gets these conventions right, instead of inferring them from a filename. Consumers: `quest` and `tidy-quest`.

| File | What it is | Who edits it, how |
|------|------------|--------------------|
| `current-state.md` | Live truth. The single file a resuming agent should need. | Edited in place, continuously, by whoever is working the session. Owns Context, Goal, Where we are, Rules, Resources, Come back to. Curated by `tidy-quest`. |
| `timeline.md` | Permanent, append-only history. Never deleted, at any point in the session's life, by any skill. | Append-only — one dated line per durable change. Never curated, never swept, never edited in place. The one place a *correction* to an earlier claim is a new dated entry, not a rewrite. |
| `followups.md` | Real work, explicitly **out of scope for finishing in this session** — not this deliverable's own later phases. | Appended to when something is decided "not now." Read by the project's close-out skill, if it has one, folded into the task list of its summary, then deleted. |
| *everything else* | Deliverables and working docs the session accumulates — a draft plan, an analysis, a proposal. | **Declared in `current-state.md`'s Resources table, with ownership and when-to-read values**, the first time a pass writes to it. See below. |

## Ownership — for the files the last row covers

The three named files have their edit rules stated above because they are always present and always the same. Everything else a session accumulates declares its own, as a value in `current-state.md`'s Resources table. **This section is the canonical definition** — skills cite it rather than restating the values.

| Ownership | Meaning | How an agent writes to it |
|---|---|---|
| `agent` | working surface the agent maintains | directly |
| `user` | content the user authors | propose the text; never edit silently |
| *(empty)* | external reference — a web page, a ticket, another session's log | not applicable; nothing here writes to it |

Default it rather than asking: files the agent created are `agent`, files the user created or pasted are `user`. State it in the row so the user can correct it.

**The declaration happens on first write, not on creation.** A row is required for every file a pass has written to — not for every file in the directory. Sessions routinely carry files nobody is maintaining, and those staying undeclared is an accurate description of them, not a gap.

**An agent does not rewrite the user's deliverables.** That rule protects their **authored** content from agent edits. It does not exempt a deliverable from receiving a decision the user and the agent just agreed to — a missing decision is not authored content, it is content the file is missing.

## When to read — for the files the last row covers

Each Resources row also says when a resuming agent reads the file. This section is the canonical definition of the values.

| When to read | Meaning |
|---|---|
| `if relevant` | The default. Read it only when the work at hand needs it. |
| `every time` | A resuming agent reads it right after `current-state.md`, before starting work. |

Every agent that resumes the session loads each file marked `every time`, so keep them few. Before marking a file `every time`, ask whether the agent needs all of it. If it needs only a small part of a large file, summarize that part in `current-state.md`'s Context and leave the file `if relevant`.

## Which "later"? (the `followups.md` test)

"Later" names two horizons and the phrasing usually doesn't separate them — "for later," "at the very end," "come back to this" read both ways.

- **Later *this session*** — a phase of the current deliverable that just hasn't happened yet (e.g. "verify these three risks before implementation," when that verification is already part of the plan this session is building). This is an open item in `current-state.md`, not `followups.md`. It stays with the deliverable it belongs to — its own PRD/plan file, or `current-state.md`'s Where we are / Come back to — even when it's framed as "not this session."
- **Beyond *this* session** — genuinely unrelated work that came up in passing. This is `followups.md`.

Before writing an entry, check `current-state.md` (and the deliverable's own file, if one exists) for an item already covering the same work. If the phrasing still doesn't settle the horizon, ask — don't guess and don't default to the broader reading. Getting this wrong isn't visibly wrong from here: a misfiled entry looks correct in either file, and the cost lands later, when the close-out skill folds `followups.md` into its summary's task list and live deliverable work quietly becomes deferred work.

## Writing a followups.md entry

Give it enough context to be useful later — what the task is, why it matters. Don't over-engineer this: the user's own memory is a real backstop here. If neither the note nor their recollection can reconstruct why it mattered, it probably wasn't worth doing in the first place. There's no dedicated verification step for this — write it with reasonable context in the moment you decide it's a "not now," and move on.

## Paths written into a session doc

A session dir may be written on one machine and read on another, where the roots differ in both username and parent folder. So any path written into a session file is either **relative to a repo root** or **re-derived at write time** (`git rev-parse --show-toplevel`). Never copy an absolute `$HOME`-rooted path forward from a prior session — that includes carrying one across a fork, which is how it usually happens.

This applies to every session file, including `current-state.md`'s Resources table, which is the one place the template actively invites a path.

**Several repos in play.** "Repo-root-relative" only says enough when there is one repo. When a session's work touches another repo, write `<repo-name>/<path from that repo's own root>` — one path string, not a separate repo column. An unprefixed path means the project the session belongs to. Define the prefix as *the repo's name*, never as a path relative to whatever parent the repos happen to share: that parent differs by machine, which is the same portability problem this whole section exists to avoid.
