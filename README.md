# Who Exactly?

**Find people already doing the work.**
A Grok Bot and four portable Agent Skills by Hiten Shah.

> **Status: developer alpha (v0.2.1).** The source, skills, schemas and offline tests are here, and all checks pass locally. The GitHub Actions workflow is not active yet (see Known limitations). The Grok Bot has **not** launched. Live X research, skill activation inside Grok Bot, and template import into a clean account have **not** been tested yet ([open issues](https://github.com/hnshah/who-exactly/issues)). The name is provisional.

## What you get as a founder

You describe your product, or the job you want to make easier. Who Exactly? helps you find people who have posted about **doing that job themselves**. Every candidate comes with:

- a link to the original post and its date
- the reason the person fits
- a list of what is still unknown

You also get:

- people who look like a fit but aren't, with the reason for each
- the tools and workarounds people use today
- invitation drafts you review and send yourself

The output is a short list of people worth talking to, plus receipts you can check. It is not a lead list.

The work supports **Play 02 of Hiten Shah's [Early Access Playbook](https://docs.google.com/document/d/1bo9n52j_M4Nx094TObZQVAq1htlB6h9XlySLgFsH710/edit)**. In v1.1 that play was called "Assemble the group". In the current v2.0 edition it is "Find the people doing the work". The Playbook is a separate educational resource. Who Exactly? is one specialist for one part of it. It is **not** the Early Access Bot; a bot covering the whole Playbook may become a separate product later. See [docs/PLAYBOOK-COMPATIBILITY.md](docs/PLAYBOOK-COMPATIBILITY.md).

What it won't do:

- treat a public post as consent to be contacted
- rank followers or scrape audiences
- send messages without your explicit approval of each recipient and text
- claim a search was exhaustive

## Install

### In Grok Bot

Follow [bot/INSTALL.md](bot/INSTALL.md). In short:

1. Create a private draft Bot.
2. Use [bot/PROFILE.md](bot/PROFILE.md) as its profile.
3. Add the four skill folders.
4. Confirm that each skill is actually enabled.
5. Run [bot/FIRST-RUN.md](bot/FIRST-RUN.md).

INSTALL.md labels every step as official, community, or untested.

### In any other Agent Skills client

Each folder under `skills/` is a self-contained [Agent Skill](https://agentskills.io/specification). The shared policies are copied into each skill's `references/`, so a skill works when you install it alone.

Get a skill in either of two ways:

- Download its ZIP from the [v0.2.1 release](https://github.com/hnshah/who-exactly/releases/tag/v0.2.1), named `who-exactly-<skill>-v0.2.1.zip`.
- Copy `skills/<skill>/` into your client's skills directory.

Before you rely on anything, verify the downloads:

```bash
sha256sum -c who-exactly-v0.2.1-SHA256SUMS.txt --ignore-missing
```

Other clients do not have Grok Bot's X tools. Without a working public X search tool, `x-people-safari` returns a search plan you can reproduce, and no candidates. It never invents people or posts.

## The four skills

| Skill | Use it to | Output |
| --- | --- | --- |
| [`job-evidence-map`](skills/job-evidence-map/SKILL.md) | Define the real job, the signals that qualify someone, and who doesn't fit | Job Card |
| [`x-people-safari`](skills/x-people-safari/SKILL.md) | Find and qualify dated, firsthand X posts, including counterexamples | Candidate Review with source links |
| [`workaround-atlas`](skills/workaround-atlas/SKILL.md) | Map what people use today and when those alternatives win | Alternatives Matrix |
| [`cohort-assembly`](skills/cohort-assembly/SKILL.md) | Draft individual invitations and plan a voluntary early group | Invitation drafts and Cohort Plan |

You don't need to name a skill. The bot picks one from what you ask.

## Method

Start with the job, then look for sources. The full method is in [docs/METHOD.md](docs/METHOD.md):

1. **Define the job:** who does it, what triggers it, what they do now, and what disqualifies someone.
2. **Search for firsthand episodes.** A post describing work the author did beats a profile, a bio, or a follower count.
3. **Check each source.** Open the link, confirm the author and date, read the thread, and rule out quote-post misattribution.
4. **Classify every candidate:** included, possible, rejected, or unknown. Each label carries a reason and the evidence still missing.
5. **Map the alternatives.** Note when the current way already works well enough.
6. **Draft invitations one at a time.** Opt-ins are recorded separately. A post is never treated as consent.

Not finding something is not proof it doesn't exist. Every result separates the source, the interpretation, what it implies, and the suggested action.

## Examples and evidence status

| Example | Evidence status |
| --- | --- |
| [fixtures/remote-mac-synthetic.json](fixtures/remote-mac-synthetic.json): remote GUI work on another Mac | **Synthetic.** Invented people, quotes and `example.org` URLs. Used for offline tests only. Never cite it as X evidence. |
| Beam (interactive apps on another Mac), the example project in the docs | **Example use case only.** No Beam research records or participant data are included. The public Playbook describes that research in its own words. |
| Live Grok Bot runs on public X | **None yet.** Protocol: [evals/README.md](evals/README.md) and [docs/LIVE-SMOKE-TEST.md](docs/LIVE-SMOKE-TEST.md). |

## Quality rubric

Every result is judged on three parts. The full rubric is in [policies/QUALITY.md](policies/QUALITY.md).

- **Evidence:** the post URL resolves, and the author, date and firsthand attribution are correct. The excerpt supports the claimed job.
- **Judgment:** fit and non-fit decisions match the job. Existing alternatives are understood. The next question changes a research decision.
- **Honesty:** gaps and mismatches are stated. There is no invented consent, prevalence, quote, or tool result.

Each of these is a hard failure: an invented post or person, a misattributed quote, claiming a retrieval that never ran, or sending anything without approval.

## Schemas and templates

- [`schemas/`](schemas/) holds JSON Schemas for mission, episode, candidate and cohort records. `src/who_exactly/` validates them offline, with no network or X access.
- The templates for each skill's output live in its `assets/` folder: Job Card, Candidate Review, Alternatives Matrix, Invitation and Cohort Plan.
- [`knowledge/templates/`](knowledge/templates/) holds the learning-note and private-project templates.

## Research memory

[`knowledge/`](knowledge/INDEX.md) holds scoped, versioned research notes. `scripts/knowledge_cli.py` decides which notes get loaded:

- Only `reviewed` notes are selected.
- A note from one project never reaches another.
- Stale notes are flagged.

Founder project context stays in a private workspace that you control. See [docs/KNOWLEDGE-LOOP.md](docs/KNOWLEDGE-LOOP.md).

## Contributing research lessons

A correction that comes out of real research starts as a **scoped draft note**, using [knowledge/templates/LEARNING-NOTE.md](knowledge/templates/LEARNING-NOTE.md) with `status: draft`. The draft names the job it applies to, when it does not apply, and its public sources. Another person reviews it before it becomes a shared rule, either `reviewed` in `knowledge/shared/` or an edit to `policies/`.

- Private research, participant names, handles and non-public posts never enter this repository.
- Code and doc changes follow the usual PR flow.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).

## Develop

```bash
python -m pip install -r requirements-ci.txt
python scripts/build.py --check        # vendored references match policies/
python scripts/validate.py             # structure, versions, links, secret scan
python scripts/knowledge_cli.py validate
python -m pytest -q
python -m skills_ref.cli validate skills/x-people-safari   # official Agent Skills validator
python scripts/package_release.py --check                  # dist/: release ZIP, 4 skill ZIPs, manifest
```

Edit shared policies only in `policies/`, then run `python scripts/build.py`. CI fails if the vendored copies drift.

## Version and changelog

The pack carries a single version, in `src/who_exactly/__init__.py`. It must match `pyproject.toml` and the top entry of [CHANGELOG.md](CHANGELOG.md). Individual skills are not versioned separately.

## Known limitations

- There has been no live Grok Bot run, no verified public X retrieval, no test of authenticated X plugin reads, and no clean-account template import.
- The CI workflow (`.github/workflows/ci.yml`) has not run on GitHub yet; the same checks pass locally.
- There is no benchmark. Nothing like HumanEval exists for this task yet, so no accuracy number is claimed.
- Public X covers only people who post publicly. When the job is confidential, the right answer may be "no usable public evidence."
- The offline tests check structure and provenance rules. They cannot tell whether real search results are any good.
- Until the claims are proven, do not describe it as "finds anyone on X", "exhaustive", "sends invitations automatically", "has access to your DMs or bookmarks", or as reaching any accuracy percentage.

## Roadmap

These items are tracked as [GitHub issues](https://github.com/hnshah/who-exactly/issues):

- live X validation
- skill activation in Grok Bot
- clean-account template test
- personal reads through the X plugin
- an A/B comparison against an ordinary Grok Bot
- a reproducible benchmark

## License

[MIT](LICENSE) © 2026 Hiten Shah.
