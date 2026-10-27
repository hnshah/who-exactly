# Changelog

All notable changes to this project. Dates are MM-DD-YYYY. The pack is versioned once, here and in `src/who_exactly/__init__.py`.

## [0.2.1] - 10-27-2026 (developer alpha, first public source release)

Repository and packaging release. The research method and skill behavior are unchanged from 0.2.0.

- Published as a standalone MIT-licensed repository. Added LICENSE, AGENTS.md, CONTRIBUTING.md and docs/PUBLIC-RELEASE-REVIEW.md.
- Moved the Grok Bot setup into `bot/` (PROFILE.md, INSTALL.md, FIRST-RUN.md), merging the earlier setup, bootstrap and legacy install docs.
- Added `license: MIT` to every skill's frontmatter so standalone copies carry it. Added `compatibility` to `x-people-safari`, saying that live discovery needs a public X search tool.
- `scripts/build.py --check` detects drift between `policies/` and the vendored skill references.
- The validator now checks: exactly four skills; references exactly mirror policies; required license; no per-skill version; one version across pyproject, the package and the CHANGELOG; relative links resolve; simple secret and local-path scan; no CRLF.
- `scripts/package_release.py` builds a reproducible release ZIP, four standalone per-skill ZIPs, a JSON manifest and a SHA256SUMS file in `dist/`.
- Added a GitHub Actions CI with pinned actions and read-only permissions. It runs pytest, the validator, the policy-sync check, the official `skills-ref` validator on each skill, and a package check.
- Removed internal pre-launch marketing copy and project-specific names that weren't needed in public examples.
- Noted that the Early Access Playbook v2.0 renamed Play 02 to "Find the people doing the work".
- Still not done: no live Grok Bot, no live X test, no template import test.

## [0.2.0] - 10-27-2026 (developer test iteration)

- Added scoped research knowledge notes and selective retrieval.
- Added draft and review gates, stale-finding checks and project-isolation tests.
- Strengthened source-author consistency checks and explicit candidate qualification.
- Fixed the installer accepting a symlink as its destination.
- Added live context verification prompts and synthetic integration regression tests.
- Still no Grok Bot installation or authenticated live X run.

## [0.1.1] - 10-26-2026 (Grok Bot installation kit)

- Checked the official Grok Bot skill activation, public X, connection and template docs. Separated them from Grok Build coding-agent skill paths.
- Added an installation guide, a Bot bootstrap message, a source-control and update policy, and a live smoke-test protocol.
- Added an opt-in, dry-run skill library installer with change detection and a required backup before replacement, plus installer tests.

## [0.1.0] - 10-26-2026 (developer release candidate)

- Bot identity and Grok instructions.
- Four structured Agent Skills with shared research policies and assets.
- Optional account-specific X access at point of need. Writing stays separate and requires approval.
- Schemas for job episode, candidate, mission and cohort records.
- Synthetic fixtures and local static and provenance tests.
