# coherence-check

Checks that a piece of writing works for a reader who has nothing but the text: no background, no chat history, no chance to ask you what you meant. Useful for anything someone else will act on, such as a handoff note, a proposal, a README, or instructions for another AI agent.

Works on its own. You don't need the other skills.

## How to use it

Ask in your own words; the agent picks it up when your request fits. Or type `/coherence-check` to ask for it by name. What you ask for decides what it does:

| You say | It does |
|---------|---------|
| "Clean this up", "tighten this", "fix this" | Edits the text in place. It asks before removing a section, changing a rule or command, or touching any other file |
| "Does this make sense?", "read this through", "sanity check this", "before I send this" | Tells you what's wrong and leaves the text alone until you ask for changes |

A quick question gets a short answer. Ask for a review and you get a numbered list of every problem, where it is, and a suggested fix.

## What it looks for

- **Stands on its own:** terms are explained where they first appear, "this" and "it" point at something clear, and nothing depends on a conversation the reader never saw.
- **Structure matches content:** one topic per section, headings that say what's under them, lists that hold one kind of thing.
- **Curated and concise:** only what the reader needs, stated plainly.
- **Grounded and consistent:** the same fact says the same thing everywhere, and no claim is stronger than what's actually known.
