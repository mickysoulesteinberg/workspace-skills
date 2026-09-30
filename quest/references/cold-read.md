# The cold read

A real check that a document stands on its own, run by an agent that holds none of the context that
produced it.

**Why the author cannot run it.** The obvious way to check "would a fresh reader understand this" is
to have the agent that just wrote the file read it back. That does not work — an agent with the whole
conversation still in its own context will always find its own summary legible, because it is filling
in gaps from memory the next reader will not have. An anti-duplication rule sitting in a session's
own `current-state.md` header has been observed to get silently violated mid-session by an agent
that had every reason to know better — writing a rule down does not make an agent apply it, and
neither does asking that agent whether it did.

**What this tests, and what it does not.** Comprehensibility only — can a cold reader make sense of
the document. Not whether what it says is **true**. A `current-state.md` that stated "nothing is
blocking drafting" passed this check cleanly while being wrong about the project's actual phase. The
reader restated a false claim accurately. Truth is a different failure class and needs its own check
(for sessions, `tidy-quest`'s Confirm pass).

## The caller declares its own question — this pack does not

Before running, the caller states two things:

1. **The artifact** — one document, handed over whole.
2. **The question** — what the reader must be able to state back, as if about to act on it.

| Caller | Question the reader must answer |
|--------|---------------------------------|
| `tidy-quest` (end of day) | What is the current goal, and what is the next step? |
| `quest` fork (fallback when the child's restatement fails) | What is the current goal, and what is the next step? |

A caller not listed here writes its own question in the same shape: something the reader states
**back**, never a yes/no. "Does this make sense?" invites agreement and measures nothing.

## Running it

Fork a subagent with **zero shared context** — it inherits nothing from this conversation. Hand it
only the one artifact. Do not hand it supporting files: a reader given the context under test cannot
detect that it was missing.

- **It states the answer cleanly** → pass.
- **It asks a clarifying question, hedges, or gets the answer wrong** → that is the signal. Fix the
  document — usually a missing definition, a stale reference, or a next step that assumes context
  that was never written down — and run it again.

**Agent type: a read-only one, named explicitly.** Name it rather than leaving it to the run. A
spawn's cost is set by the agent type's system prompt and tool schemas, not by the size of the file
being read, so an unnamed type defaults to the heaviest one available — a `general-purpose` spawn was
measured at ~60K tokens to read a 50-line file. If the project defines a lightweight read-only agent
type (a few read-only tools, one that reads whole files), use it. Being unable to write is a feature:
this reader has no business editing what it is grading. Fall back to `general-purpose` when no such
type is available. Do **not** use `Explore` despite it looking like the lean choice — it reads
excerpts rather than whole files, which is exactly wrong for a check on whether the *whole* document
stands alone.

## When it is worth spawning

Both conditions, not either:

1. The artifact is about to be left for a genuine cold reader — the day is ending, a ticket is going
   to someone else, a page is being published.
2. Something substantive landed since the last time it was checked.

Never on every write. A document that has not changed does not need re-grading, and one still being
actively drafted is *expected* to fail — an unfinished draft failing a cold read is not a finding.

## Weaker substitutes, and when they are enough

Where a real downstream reader already exists, use it instead of spawning one. The property that
matters is **author ≠ reader**, not zero context in the strict sense: a reader who holds some
adjacent context but not the hours of work the author is unconsciously drawing on is a genuine, if
weaker, check.

The clearest case is a fork — the parent writes the child's `current-state.md` and the child reads
it, so the child's own restatement is a real gate at no cost. It is weaker than this pack, because
the child holds the fork-setup conversation. That is an acceptable trade when someone is present to
correct a bad answer cheaply.

**A weak check failing is the trigger to run the strong one.** If the substitute reader comes back
wrong or hedged, spawn the real thing rather than patching by hand.
