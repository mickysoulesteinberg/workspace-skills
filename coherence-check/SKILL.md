---
name: coherence-check
description: Check that a text works for a reader who has nothing but the text: it stands on its own, its structure matches its content, it's curated and concise, and its claims are grounded and consistent. Use when asked to fix, clean up or tighten a text, or asked "does this make sense", "read this through", "sanity check" or "before I send this".
---

# coherence-check

## Purpose

This skill makes a text work for a reader who may have nothing but the text and still needs to act on it. That reader is often an agent, and the text is often written by one. After a pass, the text stands on its own, its structure matches its content, it's curated and concise, and its claims are grounded and consistent.

## Instructions

Read the text and find every place where it falls short of the principles below. Each principle says why it matters; use that to judge whether a rule applies to this text and how. Change only what a rule calls for. If the text follows a required template or structure, keep that structure and check the content within it.

**Choose the mode from the request.** If the user asks you to fix, clean up or tighten the text, or another skill runs this as a step, fix in place. If they ask what you think ("does this make sense?", "read this through", "sanity check"), report, and leave the text as it is until they ask for changes.

**Fix in place.**

- Apply fixes that keep the meaning: rewording, naming what a reference points to, cutting filler.
- Correct a claim that goes beyond what you know, or that contradicts another part of the text, when you know what's right.
- Ask before removing a section, changing a rule or a command, changing who does what, or editing any other file.
- If a fix needs a fact only the user has, ask one targeted question.

**Report at the size the question calls for.** A quick question gets a short answer naming the problems that matter most. A request for a review gets every problem as a numbered finding, with where it is and the suggested fix.

## Principles

### 1. Stands on its own

_Why it matters:_ The reader may get nothing but this text, and still need to act on it: make a decision, carry out a task, review a change. The text has to carry everything they need to do that.

- **Enough to act on.** Work out what the reader needs to do with the text, and check that it gives them what that takes. Ask the user for anything missing rather than filling it in.
- **References resolve.** Every "this", "that", "these", "those", "it", "they" or "them" points to something named within about two sentences; if it doesn't, name the thing. In a table, every row and cell makes sense on its own. In steps, each cross-reference ("step 3", "see Phase 1") points at the right item.
- **Explain terms on first use.** A term, acronym or internal name the reader might not know is explained in plain words where it first appears, or replaced with the plain words. A label coined while the text was being written ("Option B", "the working packet") is replaced with what it stands for.
- **One term per concept.** Use the same term for a concept every time it comes up.
- **Names over shorthand labels.** Refer to things by name wherever they appear, rather than by a tag, number or abbreviation defined somewhere else. If a name is provisional, say so once. A shorthand label that stays means one thing everywhere and is defined where it's used, with its legend beside it covering every item that carries it.
- **Readable without the backstory.** Leave out anything that only makes sense to someone who saw how the text was written: the conversation behind it, or its earlier versions (correction notes, comparisons with an earlier draft, notes that it replaces something). Test: would a reader who saw neither follow it? Verification dates stay.
- **Openings.** The start of the text, and of each section with a heading, says what it is and why it matters, before any method, evidence or list. For a whole document, that means what kind of document it is, where it sits relative to the work it serves, and its point or request; the occasion that prompted it isn't enough on its own. Start with content rather than repeating the title.

### 2. Structure matches content

_Why it matters:_ The structure tells the reader what each part is before they read it: a topic, a finding, a task, a decision. That lets them find what they need, skip what they don't, and act on each part as what it actually is.

- **One topic per section.** Each section covers one topic, and each topic has one section.
- **Headings and labels.** The title covers every section. Each heading or label names one thing (the topic, the finding, or the principle) in plain words and matches what's under it; a finding is labelled with the finding rather than its fix. Words that imply action, ownership or a pending choice ("job", "candidates", "owner", "to do") appear only when the section carries one. A heading that packs a problem and its remedy together with an arrow, "X vs Y" or a slash gets split: the heading names one, and the body holds the other.
- **Lists and columns hold one kind of thing.** Every item in a list is the same kind of thing, so a list of problems keeps its remedies elsewhere. In steps (numbered or if/then), each number is one action, or one stop in a UI with sub-bullets for its fields, and finished steps are marked or moved out. In a table, each column holds one kind of value, such as all actions or all statuses.
- **Organizing axis.** Each section is organized along the axis that fits the document's purpose. A document that argues or proposes groups by point, with any full listing in a reference table after the points it supports.
- **Role boundaries.** When steps involve several roles, each role's steps sit under that role's heading or carry an inline label ("IT admin: …").

### 3. Curated and concise

_Why it matters:_ Including only what's directly relevant lets the reader focus on what matters. Anything else competes for their attention and can send them in the wrong direction.

- **The right level.** State the point as the general rule, specifically enough to say something. A sentence that would read fine lifted out of the text is too general to carry the point; an example can illustrate the rule but doesn't replace it.
- **Concept over tool.** When a passage names a tool or product, check whether the point depends on it. If not, state the point in terms of the underlying concept, and mention the tool only as where the evidence came from.
- **State what is.** Give the positive fact rather than what something isn't or what was declined. Turn a list of what not to do into what to do.
- **Cut what carries nothing.** Cut filler phrases ("it's worth noting"), questions posed only to answer them, defensive asides ("not a strawman"), and restatements that add nothing new. Keep repetition that does a job: emphasis on the point that matters most, a summary that previews the detail, or a key constraint restated where it's acted on.

### 4. Grounded and consistent

_Why it matters:_ The reader treats what the text states as fact and acts on it. Keeping every claim to what's actually known, and stating it the same way everywhere, lets them rely on the text as written.

- **Agrees with itself.** A fact, number, name, status or rule stated in more than one place says the same thing each time. If two places disagree, one of them is wrong: fix it if you know which, otherwise ask.
- **Backed by what you know.** Check each claim against the context you already have: the conversation the text came from, or files you've read. When a claim is stated more strongly or precisely than that context supports (a passing comment written up as "decided", a "prefers" that became "requires", a date, number or name that was filled in), scale it back to what's supported, or cut it. Ask about gaps rather than filling them. Work only from what you already have, without searching for evidence to confirm claims; if you don't have the context the text came from, this rule doesn't apply.
