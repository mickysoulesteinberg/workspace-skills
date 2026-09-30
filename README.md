# workspace-skills

Agent skills for [Claude Code](https://code.claude.com/docs/en/skills), written to work in any project. Each folder at the top of this repo is one skill: a `SKILL.md` with instructions Claude follows, plus any reference files or scripts it needs.

## Skills

| Skill | What it does |
|-------|--------------|
| [`coherence-check`](coherence-check/SKILL.md) | Checks that a text works for a reader who has nothing but the text, and fixes it or reports what falls short |
| [`quest`](quest/SKILL.md) | Starts or continues a working session folder for a piece of work that spans several chats |
| [`tidy-quest`](tidy-quest/SKILL.md) | Keeps a `quest` session folder accurate mid-session |
| [`skill-author`](skill-author/SKILL.md) | Conventions for drafting a new skill or reworking an existing one |

---

## skill-author

`skill-author` is a set of conventions Claude follows when it writes, restructures, or retires a skill. It covers:

- **Frontmatter:** which fields to set, whether the skill runs only from its slash command or Claude may pick it up on its own, and how to write a description Claude will match against.
- **Structure:** what goes in `SKILL.md`, what moves into `references/` or `scripts/`, and what to do when a skill gets long.
- **Where content goes:** a skill's own files, a folder shared by several skills, or the project's docs, chosen by who reads it and how many skills use it.
- **Retiring a skill:** finding and fixing every reference before deleting it.

It is for drafting, not for polishing: it doesn't cover testing a skill or hardening its scripts.

### Using it

You usually don't need to invoke it by name: Claude tends to pick it up when you ask for skill work, for example:

- "Create a skill that summarizes my uncommitted changes."
- "Split this skill's `SKILL.md` into references."
- "Should this skill run on its own or only from its slash command?"
- "Retire the `old-report` skill."

To load it explicitly, type `/skill-author` before your request.

Where a project's own `AGENTS.md` or `CLAUDE.md` sets a different convention, the project wins. Put project-specific rules there, such as where skills live or how they're catalogued, rather than in this skill.

### Pairs with coherence-check

The last step of `skill-author` is to run `coherence-check` on the new `SKILL.md` and each reference file, so every file works for an agent that has nothing but that file. `skill-author` depends on `coherence-check` for that step.

### Sources

The frontmatter and structure guidance follows Anthropic's documentation: [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and [Extend Claude with skills](https://code.claude.com/docs/en/skills) (Claude Code).
