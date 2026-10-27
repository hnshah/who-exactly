# GitHub as source of truth

## Architecture

- **This repository stores versioned source:** the Bot profile, four portable skill folders, shared policies, tests, validators, schemas, synthetic fixtures and release notes.
- **Grok Bot stores enabled, installed copies** of skill folders and a short durable role. The Grok Bot UI is authoritative for whether a skill is active.
- **Your own `/workspace/who-exactly/` stores research history and private source records.** Never put real participant or candidate data in this public repository.
- **Versioning:** a pinned tag or release ZIP, its SHA-256 checksum, and an `install-state.json` on the Bot computer. Avoid unannounced live updates during ongoing research.

## Do Bot instructions link to GitHub?

**Yes, as documentation and update pointers.** They can point to a pinned release, the install guide or the method. Mentioning a repository in Bot instructions or in `SKILL.md` does **not** register a skill, make files readable across installs, or update installed copies.

A private repository needs an authorized GitHub connection, requested only when access is actually needed.

## Repository layout

```text
who-exactly/
  README.md  AGENTS.md  CONTRIBUTING.md  LICENSE  CHANGELOG.md
  bot/                    # Grok Bot profile, install guide, first run
  skills/                 # four self-contained Agent Skills
    job-evidence-map/
    x-people-safari/
    workaround-atlas/
    cohort-assembly/
  policies/               # canonical shared references, vendored into each skill
  knowledge/              # reviewed/draft research notes index and templates
  schemas/                # JSON Schemas for research records
  src/who_exactly/        # offline record and knowledge validation
  scripts/                # build, validate, package, install, knowledge CLI
  tests/  evals/  fixtures/   # fixtures are synthetic only
  docs/
  .github/workflows/
```

## Update process (manual, deliberate, observable)

1. Edit canonical policies in `policies/` or skill files on a branch. Run `python scripts/build.py` to refresh each skill's vendored `references/`.
2. CI runs the repository validator, the official `skills-ref` validator on each skill, the shared-reference sync check, the tests and the packaging check.
3. Release as an immutable tag (for example `v0.2.1`) with the release ZIP, four per-skill ZIPs and a SHA-256 manifest. Record the commit hash.
4. An installed Bot checks *whether* a newer approved release exists, shows the differences and asks before applying.
5. Download the pinned release, verify checksums, extract to a separate source directory and dry-run the installer.
6. Apply after approval, backing up any locally modified installed skills, then check hashes and the `/` skill menu.
7. Re-run one public X job, one exclusion, one unavailable-tool test and any tests for changed capabilities.
8. Update any shared template separately, and test the import in another account.

`git pull` in a workspace checkout does not update Bot skill registration. A source change has no effect on the active skill library until it is copied and re-enabled.

## Public safety checklist

Public: synthetic or de-identified fixtures only; no auth cookies or tokens; no real participant notes without consent; no private X DMs, bookmarks or protected group content; no secrets; no raw internal conversation exports.

Private (never here): sensitive historical research, evaluation answer keys, cohort permission records, internal annotations and mission output.

## Context versus software updates

`knowledge/INDEX.md` and its reviewed notes are versioned context data, not executable instructions. A Bot can consult them from a pinned revision. See [`KNOWLEDGE-LOOP.md`](KNOWLEDGE-LOOP.md) for the selection and correction protocol. A knowledge-note edit may be read on the next mission; skill code changes only through the versioned install procedure above.
