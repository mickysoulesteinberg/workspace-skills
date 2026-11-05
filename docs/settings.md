# Settings

The quest skills work without any setup. Settings let you change how they behave in one project: how quests are named, what time zone dates use, what goes in a summary, and extra steps to run when a quest closes.

Settings are plain Markdown files you write in your own words. The agent reads them and follows them. There's no special format to learn, apart from three headings in one of the files.

## Where they go

Both files are optional, and both live in your project, not in this repo:

```
your-project/
└── .agents/skill-settings/
    ├── quest.md          ← settings for all three quest skills
    └── close-quest.md    ← extra steps for close-quest only
```

A missing file means the skills use their defaults.

## `quest.md`: settings for all three quest skills

`quest`, `tidy-quest`, and `close-quest` all read this file. Use it for anything that should hold across a whole quest, for example:

- who you are, so summaries can refer to you correctly;
- how quests are named;
- how notes should link to other files;
- anything about how sessions work that's different in your project.

Where these settings and your project's general instructions to the agent (an `AGENTS.md` or `CLAUDE.md` file) disagree about sessions, these settings win.

## `close-quest.md`: extra steps when a quest closes

This file has three sections. The agent reads each one at a particular point in `close-quest`, so a step happens when it makes sense:

| Section | Read when | Put here |
|---------|-----------|----------|
| `## Overrides` | At the start | Changes to the defaults: your time zone, files to delete every time, how open tasks should be written |
| `## Draft additions` | While writing the draft summary | Extra fields or sections in the summary, and anything you want to see and approve along with it |
| `## After write` | After the summary is written | Things to do elsewhere in your project, such as adding a line to a log or updating a related note |

Keep the three headings spelled exactly as above: they're how `close-quest` finds each section. A long procedure can live in its own file, with the section pointing to it ("follow `.agents/close-quest/changelog.md`").

The draft summary lists which of your additions ran, so you can see if one was skipped.

## Example

An example setup, to show the kind of thing settings can do. Copy whatever is useful and ignore the rest. In this project:

- notes are kept in a notes app that links files by name, written `[[file-name]]`;
- each piece of work has a ticket in an issue tracker, with a key like `ABC-123`;
- open tasks carry the date they were added, written `[since:: 2026-11-02]` so the notes app can sort them;
- process notes picked up during a quest are collected in one backlog file for later review.

"Frontmatter" below means the block of `key: value` lines between `---` markers at the top of the summary file.

`.agents/skill-settings/quest.md`:

```markdown
# Quest settings

- **The user** is Sam (they/them).
- **Naming:** if my first message names a ticket key like ABC-123, name the quest after it.
- **Links:** link to files in this project as [[file-name]], not as paths.
- **Closing a quest:** use close-quest.
```

`.agents/skill-settings/close-quest.md`:

```markdown
# close-quest settings

## Overrides

- Use US Pacific time for dates and folder names.
- Always delete `scratch.md` from the session folder.
- Write open tasks as `- [ ] <task> [since:: YYYY-MM-DD]`.

## Draft additions

- If the quest is named after a ticket, add `ticket: "[[ABC-123]]"` to the summary's frontmatter.
- If the quest changed files in the `website` repo, draft a commit message for me to approve. Don't commit.
- If the session folder has a `process-notes.md`, list its entries in the draft so I can drop any that are already handled.

## After write

- Append the remaining entries in `process-notes.md` to `notes/process-backlog.md`.
- If the quest is named after a ticket, offer to update that ticket's note with any decisions still in force. Show me the change first.
```

## Checking your settings

For `quest.md`, you can print exactly what the skills will read. From your project folder, run the script inside your installed `quest` folder. The path below is the Claude Code location; use wherever you installed it:

```bash
python3 ~/.claude/skills/quest/scripts/session-bootstrap.py --root . --show-settings
```

That shows `quest.md` only. `close-quest` reads `close-quest.md` itself, and its draft tells you which sections it used.
