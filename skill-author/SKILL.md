---
name: skill-author
description: Conventions for drafting agent skills — frontmatter, body structure, where content goes, splits, and retiring a skill. Use when creating or substantially changing a skill, or when asked "how should this skill work" or "what's the convention for X in skills".
when_to_use: Invoke when creating a skill from scratch, refactoring a skill for token efficiency, deciding whether a skill is ambient, splitting a SKILL.md into references/, placing content that more than one skill needs, or retiring a skill.
---

# skill-author

Conventions for drafting skills — folders with a `SKILL.md` that Claude loads to carry out a task, kept in a skills folder such as your personal `~/.claude/skills/` or a project's `.claude/skills/`. Read this before creating a skill or substantially changing one. The project's own `AGENTS.md` (or `CLAUDE.md`) wins wherever it says something different.

---

## Writing the instructions

These rules apply to the body text of every skill and its reference files.

- **Add only what Claude doesn't already know.** Skip explanations of common tools, formats, and concepts; spend the words on this project's specifics.
- **Write standing instructions.** Once a skill loads, its content stays in the conversation for later turns and isn't re-read, so every line is a recurring cost and guidance should read as rules that hold throughout the task, not one-time steps.
- **Match strictness to fragility.** Give exact commands and sequences where a mistake is costly or the order matters; give general direction where several approaches work and context decides.
- **Use one term per concept** throughout the skill and its references.

---

## Frontmatter

A skill is either **manual** (runs only when someone types its slash command) or **ambient** (Claude may also invoke it without a slash command, choosing it from its description).

The frontmatter is read only when its opening `---` is the file's first line. Field names must match exactly: Claude Code silently ignores a field it doesn't recognize.

| Field | Purpose | Use for |
|-------|---------|---------|
| `name` | The command name. Claude Code defaults it to the folder name; other surfaces require it. At most 64 characters, lowercase letters, numbers, and hyphens only, and it can't contain "anthropic" or "claude" | Every skill |
| `description` | What the skill does and when to use it. Claude chooses ambient skills from it | Every skill |
| `when_to_use` | Extra trigger phrases or example requests, appended to `description` in the list Claude chooses from | Ambient skills whose triggers don't fit in `description` |
| `disable-model-invocation: true` | Makes the skill manual; its description is removed from Claude's context | Most skills, and any skill with side effects or timing you want to control |
| *(omit `disable-model-invocation`)* | Makes the skill ambient. Omitting the key is how to say this — writing `false` is not needed | Skills meant to run without a slash command |
| `user-invocable: false` | Only Claude can invoke the skill: it's hidden from the `/` menu, and typing `/name` doesn't run it | Background knowledge that isn't a meaningful command |
| `argument-hint` | Autocomplete hint for expected arguments, such as `[issue-number]`. The body reads them through `$ARGUMENTS` | Skills that take input |
| `allowed-tools` | Tools Claude may use without asking, during the turn that invokes the skill | Skills that run the same commands every time |
| `paths` | Glob patterns; Claude loads the skill automatically only when working with matching files | Skills that apply only to certain files |

Claude Code accepts more fields than these; its skills documentation (code.claude.com/docs/en/skills) lists them all. Outside Claude Code (claude.ai uploads, the Skills API), only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools` are allowed, and any other field makes the upload fail.

**Manual vs ambient:** default to manual unless the skill is meant to be ambient. When designing a skill with the user, present both options — the default is a suggestion, not policy.

**Every description:** third person ("Processes X", not "I can help you…"), says what the skill does and when to use it, at most 1,024 characters, no XML tags.

**Description, manual skill:** one tight sentence on what the skill does. No trigger phrases — a manual skill's description isn't in Claude's context, so they add nothing.

**Description, ambient skill:** at most two sentences, key use case first, with condensed symptom and trigger phrases. Every ambient skill's description sits in Claude's context in every session, and the list Claude chooses from cuts `description` plus `when_to_use` at 1,536 characters.

---

## Body structure

`SKILL.md` holds the steps, the stops (points where the skill pauses for the user), and pointers to `references/`. Detail needed only on some runs lives in `references/`, loaded only when needed.

```
my-skill/
├── SKILL.md          ← steps + stops + pointers (loaded when the skill runs)
├── references/       ← detail loaded on demand
│   └── phase-name.md
└── scripts/          ← executed, never loaded as context
```

- **Link every reference file directly from `SKILL.md`**, saying what it contains and when to load it. Claude may read only part of a file it reaches through another reference file, so keep references one level deep.
- **Give a reference file over about 100 lines a table of contents** at the top, so a partial read still shows everything it covers.

### Scripts

`scripts/` is execute-only. When adding a helper:

- Prefer **argparse**, with a module docstring (or a usage block at the top) saying what the script does and how to run it.
- Run it through the project's own Python entrypoint (a wrapper script, pipenv, uv, and so on) if it has one — not bare `python`.
- Reuse an existing shared helper when one exists. Otherwise copy just the part of it you need into the skill's `scripts/`, and note where it came from.
- Call skill scripts directly, without another wrapper script around them.

---

## Where content goes

The tree in Body structure is one skill's own folder, and it is not the only place content can live. Two questions decide the home: *does more than one skill do this?* and *does a person ever read it?*

| Home | Test |
|------|------|
| `SKILL.md` | One skill; needed on every invocation |
| `references/` | One skill; needed only on some runs |
| A shared folder for skills (e.g. `.claude/skills/_shared/`) | Two or more skills do it; only agents read it |
| The project's docs | People read it too — conventions, guides, anything a teammate might open. Skills point at it rather than copying it |

Decide by audience and reuse, not by topic. A file does not belong in a folder because its neighbours happen to be about the same subject.

---

## When a skill gets long

Anthropic recommends keeping `SKILL.md` under 500 lines, because once a skill loads, all of it stays in context for the rest of the conversation. When a skill passes that, or feels long before then, look for a split that actually saves something:

- **Content only some runs need** (a phase procedure, a template, a rarely used mode) can move to `references/`.
- **Two jobs in one skill** can become two skills, each with its own description, so Claude loads only the one the request needs.
- **Content Claude already knows** can be cut.

If none of these apply, leave the skill long. A split that gets loaded on every run anyway saves nothing and adds a file to keep in sync.

**Reference file names:** name files by what they contain — `synthesize.md`, `phase-report-context.md` — rather than by step number, so a renumbered step doesn't leave a misleading name.

---

## Retiring a skill

1. Confirm what replaces it — another skill, a manual workflow, or nothing.
2. **Stop — do not delete** until the user confirms in the conversation.
3. Find every reference: `rg --hidden '<skill-name>'` across the repo. **`--hidden` is required**: skills live under `.claude/`, a hidden folder, so a plain `rg` returns only hits in visible folders and misses every skill file — where the callers actually are. It comes back looking like nothing references the skill.
4. **Fix every caller** the search found, not just the retired skill's own files. Cross-references sit in other skills' routing tables and `references/` files, and nothing links back from those.
5. Delete the skill folder entirely — no deprecated stub.
6. Re-run the search from step 3 and confirm nothing still tells an agent to invoke the old name.

---

## Before finishing

Run the `coherence-check` skill on `SKILL.md` and on every file in `references/`, and fix what it finds, so each file works for an agent that has nothing but that file.
