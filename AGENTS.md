# AGENTS.md

Instructions for coding agents and contributors working in this repository.

## What this is

**Who Exactly?** is four Agent Skills plus a Grok Bot profile for finding people who have posted about doing a specific job firsthand on X. It is a developer alpha. The offline code validates research records. It does not search X.

## Layout

- `skills/<name>/`: the shipped skills. Each must work when installed alone.
- `policies/`: the **canonical** shared research policies. `scripts/build.py` copies them into `skills/*/references/`. Never edit the vendored copies directly.
- `bot/`: the Grok Bot profile, the install guide and the first-run checks.
- `knowledge/`: scoped research notes, plus the selector (`scripts/knowledge_cli.py`, `src/who_exactly/knowledge.py`).
- `schemas/`, `src/who_exactly/`, `fixtures/`, `tests/`: offline record validation. All fixtures are synthetic.
- `scripts/`: build, validate, package, and the optional Grok skill installer.

## Before you commit

```bash
python scripts/build.py && python scripts/build.py --check
python scripts/validate.py
python scripts/knowledge_cli.py validate
python -m pytest -q
for s in skills/*/; do python -m skills_ref.cli validate "$s"; done
python scripts/package_release.py --check
```

## Rules

- **Never invent evidence.** No made-up people, posts, handles, quotes, URLs or test results. Mark anything unverified as UNKNOWN.
- Fixtures must be obviously fictitious: `example.org` URLs, `fictional-` handles, and a `FICTITIOUS FIXTURE` warning.
- No private research records, participant names or handles, non-public posts, credentials, or absolute local paths. `scripts/validate.py` scans for some of these. A review is still required.
- Frontmatter keys are limited to the Agent Skills spec. Every skill has `license: MIT` and `metadata.author`. Do not add a per-skill version.
- Bump the version in `src/who_exactly/__init__.py`, `pyproject.toml` and `CHANGELOG.md` together.
- Every file a skill ships must be referenced from its `SKILL.md` as `` `references/...` `` or `` `assets/...` ``.
- Do not claim any live Grok Bot or X behavior that no one has tested.
