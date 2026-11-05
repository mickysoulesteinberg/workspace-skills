# workspace-skills

Five skills for AI agents. A skill is a folder of written instructions, centered on a file called `SKILL.md`, that an agent follows when you ask for it, often by typing its name with a slash in front, like `/quest`. Nothing here is code you need to run yourself: each skill is a few Markdown files.

Three of the skills work together to keep a piece of work organized when it takes more than one chat. The other two are general tools: one checks that a piece of writing makes sense to someone reading it cold, and one helps you write skills of your own.

## Which agents this works with

The skills follow the general `SKILL.md` format: a folder with a `SKILL.md` file whose header gives the skill's `name` and `description`, plus any reference files or scripts it needs. Any agent tool that reads skills in that format can load them.

I built and tested them in [Claude Code](https://code.claude.com/docs/en/skills), Anthropic's coding agent, so a few details are specific to it. Those are marked **(Claude Code)** where they come up in these docs:

- the folders an agent looks in for skills;
- a few optional header fields, such as one that keeps a skill from running unless you type its name;
- `${CLAUDE_SKILL_DIR}`, which the skills use to find their own files.

On another tool, check its documentation for the equivalents. The instructions themselves are written for any agent.

## Is this for you?

**A good fit if** you use an agent for work that runs across several chats: a project that takes a few days, an investigation you keep coming back to. Each new chat starts with no memory of the last one, so you end up re-explaining where things stand. The quest skills keep a folder of notes that any new chat can pick up from.

**Not needed if** your tasks finish within one chat. You might still want `coherence-check` on its own.

**Still settling in.** I built the quest skills for my own project, and I'm still adjusting them so they work for other kinds of projects. When an instruction doesn't fit your project, the agent is told to ask you instead of guessing.

## The five skills

| Skill | What it's for | Guide |
|-------|---------------|-------|
| `quest` | Start a piece of work that spans several chats, or pick one back up | [quest](quest/README.md) |
| `tidy-quest` | Bring the notes up to date before you stop for the day | [tidy-quest](tidy-quest/README.md) |
| `close-quest` | Wrap up finished work into a dated record | [close-quest](close-quest/README.md) |
| `coherence-check` | Check that a text makes sense to a reader who has only the text | [coherence-check](coherence-check/README.md) |
| `skill-author` | Write or rework a skill of your own | [skill-author](skill-author/README.md) |

`quest`, `tidy-quest`, and `close-quest` are a set: the second and third only work when `quest` is installed beside them. `skill-author` uses `coherence-check` in its last step. `coherence-check` works on its own.

## Install

Download this repo, then copy the skill folders you want into the folder your agent loads skills from. **(Claude Code)** It looks in two places:

- `~/.claude/skills/` in your home folder, for skills you want in every project;
- `.claude/skills/` inside a project, for skills you want only there.

For example, to install the three quest skills for every project in Claude Code (replace `<repo-url>` with this repository's address):

```bash
git clone <repo-url> workspace-skills
mkdir -p ~/.claude/skills
cp -R workspace-skills/quest workspace-skills/tidy-quest workspace-skills/close-quest ~/.claude/skills/
```

**Install the three quest skills together, in the same folder.** `tidy-quest` and `close-quest` use files that live inside `quest`.

`quest` and `tidy-quest` run a small Python script, so you need `python3` installed.

**Check it worked (Claude Code):** type `/` in the chat box. The skills you installed appear in the list.

## How a quest works

A **quest** is one piece of work that spans several chats. Each quest gets its own **session folder**: a folder of plain Markdown notes inside your project that the agent keeps up to date as you go. Here is one quest from start to finish.

**Monday morning: start.** In the chat, type `/quest` and say what the work is: `/quest reorganize the docs folder`. The agent creates a session folder in your project and writes the goal into it:

```
your-project/
└── logs/agent-sessions/
    └── _current-1102-reorganize-docs/
        ├── session.yml         ← the quest's name and start time
        ├── current-state.md    ← where things stand now: goal, next step, key files
        └── timeline.md         ← one dated line per decision, never deleted
```

The `_current-` at the front marks a quest that's still open. Work as usual from here. When you ask the agent to remember something, it writes it into this folder instead of keeping it in the chat.

**Monday evening: stop.** Type `/tidy-quest` and say you'll pick it up tomorrow. The agent writes down anything decided today that isn't in the notes yet, tidies `current-state.md`, and checks that the "next step" it lists is still true.

**Tuesday: pick it back up.** Open a new chat and type `/quest` followed by the quest's name: `/quest reorganize-docs`. The agent reads the notes and tells you, in its own words, what the goal is and what's next, so you can correct it before carrying on. **Naming the quest is how you resume.** Plain `/quest` always starts a new one.

**Wednesday: finish.** Type `/close-quest`. The agent suggests what to do with each file in the folder (keep it, delete it, fold what it found into the summary and delete it, or move it somewhere permanent) and waits for your OK. Then it shows you a draft summary and waits again. Once you approve, it writes the summary and renames the folder:

```
your-project/
└── logs/agent-sessions/
    └── 20261102-0930-reorganize-docs/
        ├── 20261102-0930-reorganize-docs.md    ← the summary
        └── timeline.md
```

For other ways to use the skills, see [example workflows](docs/workflows.md). They're suggestions, not requirements.

## What these skills change in your project

- `/quest` creates one folder under `logs/agent-sessions/` and writes notes there.
- `/tidy-quest` edits the notes in that folder and the files the quest is producing there. It never deletes anything.
- `/close-quest` deletes or moves files from that folder, marks done any tasks elsewhere in your project that the quest finished, and runs any extra steps your settings add. All of it happens only after you've said yes, twice.
- None of them makes a git commit unless you or your settings ask for one. You decide whether `logs/` gets committed to your repository or goes in `.gitignore`.

## Tailoring the skills to your project

You can change how the quest skills behave in one project, such as how quests are named, what time zone dates use, or extra steps when a quest closes, by adding settings files to it. See [settings](docs/settings.md).

Many agent tools also read a project-wide instructions file, such as `AGENTS.md` (or `CLAUDE.md` in Claude Code). Where that file and these settings disagree about sessions, the settings win.

## Writing your own skills

`skill-author` holds the conventions I wrote these skills with. See its [guide](skill-author/README.md). Each skill's `SKILL.md` is the set of instructions the agent follows; read it when you want to change how a skill behaves.
