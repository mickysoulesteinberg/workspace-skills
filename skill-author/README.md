# skill-author

Conventions for writing your own agent skills, or reworking existing ones. I used it to write the other skills in this repo.

Its last step runs [`coherence-check`](../coherence-check/README.md) on each file, so install the two together, in the same skills folder.

## How to use it

Ask for skill work in your own words, and the agent usually picks it up:

- "Create a skill that summarizes my uncommitted changes."
- "This skill's instructions are too long. Split them up."
- "Should this skill run on its own or only when I type its name?"
- "Retire the `old-report` skill."

Type `/skill-author` before your request to ask for it by name.

## What it covers

**General skill practice**, for any agent that reads `SKILL.md` skills:

- **How to write the instructions:** only what the agent doesn't already know, written as standing rules, with strictness matched to how costly a mistake is.
- **How to lay out a skill:** what goes in the main `SKILL.md` file, what moves into separate reference files or scripts, and what to do when a skill gets long.
- **Where things belong:** a skill's own files, a folder several skills share, or your project's documentation, depending on who reads it and how many skills need it.
- **Retiring a skill:** finding and fixing everything that mentions it before deleting it.

**Based on Anthropic's documentation:** the guidance on a skill's header fields (its frontmatter). `name` and `description` are part of the general format. Several others are Claude Code fields that other tools may ignore or reject: `disable-model-invocation` (the skill runs only when you type its name), `when_to_use`, `user-invocable`, `argument-hint`, and `paths`. The length limits it gives for names and descriptions, and its advice on writing a description the agent will match against, also come from Anthropic's documentation; check your own tool's rules.

It covers writing a skill, not testing one.

Where your project's own instructions to the agent (an `AGENTS.md` or `CLAUDE.md` file) say something different, your project wins.

## Sources

The frontmatter guidance follows Anthropic's documentation: [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and [Extend Claude with skills](https://code.claude.com/docs/en/skills).
