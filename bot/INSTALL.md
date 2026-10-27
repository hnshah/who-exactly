# Install Who Exactly? in Grok Bot

**Status: developer alpha (v0.2.1).** These steps have not yet been run end to end in a live Grok Bot account. Nothing here is evidence that the Bot is installed, that its skills activate, or that live X research works. Menu labels can change; check them in your own account.

The guide separates three kinds of statement:

- **Official:** documented Grok Bot behavior, linked at the end.
- **Community-observed:** filesystem behavior other people have reported. Inspect before relying on it.
- **Untested:** our own Who Exactly? steps, not yet verified in a live account.

## 0. Mental model

| Layer | Where it lives | Why |
| --- | --- | --- |
| Public name | `Who Exactly?` | What people see and say |
| Bot role | First Bot message, remembered role, name edited in Details | Personal Grok Bots take durable job instructions conversationally |
| Skill source | This repository, or a release ZIP, `skills/<slug>/` | Standard Agent Skills; each folder is self-contained |
| Active skills | Grok Bot's private skill library, **enabled for this Bot** | A cloned repository is not automatically a loaded skill |
| Research state | `/workspace/who-exactly/` on the user's Grok Bot computer | Persistent, user-owned mission and source records |
| Optional connections | X plugin, GitHub access, only when needed | App permissions belong to the account; ask only when needed |
| Distribution | Grok Bot Share → Create template, validated separately | A template is a recipe, not a copy of files or secrets |

## 1. Before opening Grok Bot

- Download `who-exactly-v0.2.1.zip` and `who-exactly-v0.2.1-SHA256SUMS.txt` from the [v0.2.1 release](https://github.com/hnshah/who-exactly/releases/tag/v0.2.1). Check the hash with `sha256sum -c who-exactly-v0.2.1-SHA256SUMS.txt --ignore-missing`.
- Open a **private personal** Grok Bot, not a Team Bot and not a public shared template.
- Do not enable X, GitHub, routines or message sending just to finish basic setup.
- Keep project work under `/workspace/who-exactly/`. The Grok Bot computer is shared by all Bots on the account, so this is not a private sandbox for one Bot.

## 2. Create the Bot

1. In Grok Bot, use `New chat` → `Create new Bot` (or the equivalent path).
2. Name it **Who Exactly?** if punctuation is accepted, otherwise **Who Exactly**. Record what actually shows in the sidebar, search and share preview. Punctuation support is untested.
3. Add the label **By Hiten Shah** only if the profile supports labels. Send the durable role as the first message and ask the Bot to remember it. The canonical role text is [`PROFILE.md`](PROFILE.md).
4. Attach the release ZIP and paste the setup message in section 7 below. It makes the Bot inspect, extract, install and validate the exact files instead of improvising skills from a summary.

## 3. Install the four self-contained skills

The release ZIP contains four complete folders:

- `skills/job-evidence-map/`
- `skills/x-people-safari/`
- `skills/workaround-atlas/`
- `skills/cohort-assembly/`

Each is also published as its own ZIP (`who-exactly-<skill>-v0.2.1.zip`) for Agent Skills clients that install one folder at a time.

**Official path:** use Grok Bot's skill library and `Connect apps`, and make sure each private skill is enabled for this Bot. Type `/` in the desktop composer to check that each one appears. If one is missing, open `Connect apps` → the connected count next to the title → enable it under `Private skills` for this Bot. A skill's `description` is its natural-language trigger; pasting it into memory is not the same as installing it.

**ZIP layout:** the release ZIP has one top-level `who-exactly/` folder. When placing source in `/workspace/who-exactly/source`, extract to a temporary directory and move the inner `who-exactly/` folder to `source/`, so you don't end up with `source/who-exactly/skills/`.

**Filesystem fallback (community-observed, inspect first):** community reports identify `~/agent-data/workflows/<slug>/SKILL.md` as the Grok Bot skill directory. This is not the `.grok/skills` directory of the separate Grok Build coding agent. Before copying, inspect where existing skills actually live and which are enabled. If your environment matches, use the bundled installer:

```bash
cd /workspace/who-exactly/source
python3 scripts/install_grok_bot_skills.py --destination "$HOME/agent-data/workflows"
# Review the dry run, then approve changes explicitly:
python3 scripts/install_grok_bot_skills.py --destination "$HOME/agent-data/workflows" --apply
```

The installer never installs packages, makes network requests, publishes anything or creates routines. It skips identical installs and refuses to overwrite differing installs unless you pass `--replace` with a `--backup-dir` outside the skill library. **Copying files to disk does not register a skill.** Check all four names in the `/` menu and in this Bot's enabled skills.

## 4. GitHub as source, not live sync

This repository is the source of code and method. It is not an automatic skill loader. See [`docs/GITHUB-SOURCE-AND-UPDATES.md`](../docs/GITHUB-SOURCE-AND-UPDATES.md) for the pinned-update procedure: check a tagged release, verify checksums, dry-run the installer, apply with approval and a backup, then re-check the `/` menu. Never `curl | bash` an unpinned installer.

## 5. Plugin access: just in time

- Public X posts: research without any connection.
- Your own bookmarks, home timeline, DMs and likes: check which X plugin operations exist, ask for connection through `Connect apps` only when needed, then resume the original task.
- Linking X for `@bot` routing is not the same as connecting the X plugin. An `@bot` mention on X goes to your main Bot, not automatically to Who Exactly?.
- Read permission is not send permission. Draft first, confirm a specific supported write action, and get approval per recipient and message. No bulk unsolicited contact.
- Connect GitHub only if reading an authorized private repository actually requires it.

## 6. Persistent research records

Create these inside **your** `/workspace/who-exactly/`, never inside the public skill source or a shared template:

```text
/workspace/who-exactly/
  source/                  # unpacked versioned skill source; code, not research
  missions/
    <mission-id>/
      brief.md             # one product decision and intended job
      sources.jsonl        # public URLs, author, date, retrieval time, quoted context
      candidates.json      # included / possible / rejected / unknown, with reasons
      counterexamples.md   # false fits and incumbent methods that already work
      outreach-drafts.md   # drafts; NOT a sent-message log
      result.md            # findings, interpretation, remaining unknowns
  install-state.json       # version, source commit, installed skill hashes
```

## 7. Setup message to paste with the ZIP

Use this as the Bot's first message after creating it and attaching the release ZIP.

---

You are **Who Exactly?**, by Hiten Shah. Your promise is: **Find people already doing the work.** You help founders find people on X who publicly describe doing the real job their product is supposed to improve, check and qualify that evidence, study current workarounds, and prepare thoughtful early-access research invitations.

I have attached `who-exactly-v0.2.1.zip`. It is the authoritative package for this install. **Do not invent skills or fetch a similarly named repository as a substitute.**

1. Read `bot/PROFILE.md`, `bot/INSTALL.md` and `docs/METHOD.md` from the ZIP. Adopt the role, evidence standard, tool limits, approval rules and source distinctions as your operating instructions. Example output is not real X evidence.
2. Extract the ZIP, **removing its single `who-exactly/` wrapper**, so the profile ends up at `/workspace/who-exactly/source/bot/PROFILE.md` and skills at `/workspace/who-exactly/source/skills/`. Check all four skill folders, including `references/` and `assets/`, against `MANIFEST.json`. Do not edit or overwrite unrelated skills.
3. Run the local validation and tests if the computer can execute them, and report exact commands and results. Report missing dependencies honestly; do not install system-wide tools just to pass a test.
4. Inspect your actual skill library. The official path is `Connect apps` → Private skills, enabled per Bot. On some computers the folder is `$HOME/agent-data/workflows`. Do not confuse Grok Bot with Grok Build's `.grok/skills`. Show me what is there. Run the installer dry run if it fits what you see, and ask before overwriting anything. Install all four complete skill folders and enable them for this Bot.
5. For a returning founder's research, follow `docs/KNOWLEDGE-LOOP.md`. The bundled knowledge note is a draft; do not claim prior evidence you cannot read. Never mix one founder's private research into another project, and propose scoped learning-note edits instead of silently changing GitHub or skill files.
6. Confirm that `/job-evidence-map`, `/x-people-safari`, `/workaround-atlas` and `/cohort-assembly` are discoverable in this Bot, or say which are not. Files on disk are not proof that a skill is active.
7. Create `/workspace/who-exactly/missions/` for my research. Never store personal X data, participant evidence or keys in the skill source or a shareable template. Do not create scheduled routines.
8. Public X needs no connection. When I later ask about my own bookmarks, DMs, home timeline or likes, check whether the X plugin operation exists, and only then ask me to connect X through the app. Never ask for passwords in chat. Treat posting or sending DMs as a separate, specifically approved action; drafts first.
9. Do not publish, share or update a public template. Do not contact anyone. Do not claim live X verification until you have actually retrieved a source.
10. Return a short setup receipt: Bot name and label, source location, package version, the four skills (enabled versus only on disk), files and tests checked, public X tool available, connection state if known, warnings, and one next test.

---

Then run [`FIRST-RUN.md`](FIRST-RUN.md).

## 8. What "installed and ready" means

| Level | Definition | Status for v0.2.1 |
| --- | --- | --- |
| Package ready | Validator, `skills-ref` and tests pass; installer dry run is clean | Checked in CI for this release |
| Bot installed | Name, role, four enabled skills and tool access verified in the real Grok Bot UI | **Not yet verified** |
| Research quality ready | An independent check confirms original authors, dates, relevance, negative cases and no invented results | **Not yet verified** |
| Share ready | A new person imports the template and completes a real task with no creator files, logins or help | **Not yet verified** |

## References

- Official: https://docs.x.ai/grok-bot/bots
- Official: https://docs.x.ai/grok-bot/skills-routines-and-automations
- Official: https://docs.x.ai/grok-bot/computer-and-apps
- Official: https://docs.x.ai/grok-bot/approvals-security-and-privacy
- Official: https://docs.x.ai/grok-bot/tag-on-x
- Official: https://x.ai/bot/guides/templates-for-grok-bot
- Community-observed deployment: https://github.com/microsoft/apm/issues/3083
- Community-observed deployment: https://github.com/fal3/grokbot-jev-skills
- Separate product, **not** the desktop Bot: https://docs.x.ai/build/features/skills-plugins-marketplaces
