# Public release review — v0.2.1

Reviewed 10-27-2026 before the repository was made public. Every tracked file was read and checked for:

1. Private research records, or real participant names, handles or posts.
2. Credentials, tokens or keys.
3. Internal-only material: private experiments, internal notes of other companies or products, private Beam or Crazy Egg research.
4. Absolute paths to private repositories or local machines.
5. Licensing problems: third-party text or code without a compatible license.

Automated support: `scripts/validate.py` runs a secret-pattern and local-path scan on every text file. CI runs it on each push. Manual checks included a scan for capitalized name pairs, `@handles` and every URL. Every URL is one of: a public documentation link, the public Playbook Google Doc, the two public GitHub references in `bot/INSTALL.md`, an `example.org` placeholder, or a test-only `x.com/.../status/123`-style string that is not a real post.

## Removed before publication (relative to the v0.2.0 developer package)

| Removed | Why |
| --- | --- |
| `docs/PUBLIC-POSITIONING.md` | Internal pre-launch positioning and a draft social post. Its "prohibited claims" list moved into README Known limitations. |
| `docs/INSTALL-GROK.md`, `docs/GROK-BOT-FULL-SETUP.md`, `docs/GROK-BOT-BOOTSTRAP.md` | Superseded; merged into `bot/INSTALL.md`. Removed a private-repository name and local paths. |
| `MANIFEST.json` (root) | Build artifact; regenerated inside the release ZIP. |
| Named unrelated product (Crazy Egg) in docs and tests | Not needed for the example; replaced with a generic placeholder. |

**Not included at all:** the design-history private repository and its pull request, Beam research data or participant information, test-run reports, and any X account data.

**Licensing:** all content is original to this project and released under MIT. The design borrows structural ideas from the public MIT-licensed `LMTYdotcom/skills` repository: vendored shared references, a build/validate split, and deterministic ZIPs. No files were copied from it. The pinned GitHub Actions are used under their own licenses and are not redistributed.

**Result:** no blocking findings.

## File-by-file verdicts

Verdicts: **Clear** means reviewed and unchanged in substance. **Edited** means reviewed and changed for privacy, accuracy or release.

| File | Verdict | Notes |
| --- | --- | --- |
| `.gitattributes` | Clear | LF normalization; no content concerns. |
| `.github/workflows/ci.yml` | Clear | Actions pinned by commit SHA, read-only token, no secrets used. |
| `.gitignore` | Clear | Excludes caches, dist/, .env. |
| `AGENTS.md` | Clear | New. Contributor/agent rules; no private material. |
| `CHANGELOG.md` | Clear | Dates converted to MM-DD-YYYY; 0.1.0 "not shipped" line about license approval removed because MIT is now chosen. |
| `CONTRIBUTING.md` | Clear | New. Research-lesson draft → review workflow. |
| `LICENSE` | Clear | New. MIT, Copyright (c) 2026 Hiten Shah. |
| `README.md` | Clear | Rewritten. Status stated as developer alpha; no launch or live-test claims; synthetic example labeled. |
| `bot/FIRST-RUN.md` | Clear | New. Generic checks, no real people or posts. |
| `bot/INSTALL.md` | Clear | New; merges former setup + bootstrap docs. Only public URLs (docs.x.ai, x.ai, agentskills.io, two public GitHub links), each confirmed HTTP 200 on 10-27-2026. Community and untested steps labeled. |
| `bot/PROFILE.md` | Clear | Moved from BOT-PROFILE.md. Play 02 naming updated for Playbook v2.0. |
| `docs/GITHUB-SOURCE-AND-UPDATES.md` | Edited | Removed private repository name; now describes this public repo. |
| `docs/KNOWLEDGE-LOOP.md` | Edited | Renamed. Replaced a named unrelated product (Crazy Egg) with a generic placeholder; Beam kept only as the example project, no data. |
| `docs/LIVE-SMOKE-TEST.md` | Clear | Renamed. Protocol only; no results claimed. |
| `docs/LIVE-TEST-HANDOFF.md` | Edited | Renamed; unrelated-product name made generic; blank result form, no results. |
| `docs/METHOD.md` | Clear | Method description only. |
| `docs/PLAYBOOK-COMPATIBILITY.md` | Edited | Added v1.1 → v2.0 play-name table from the public Playbook doc; Beam line limited to "described publicly in the Playbook", no records. |
| `docs/PUBLIC-RELEASE-REVIEW.md` | Clear | This file. |
| `docs/RELEASE-GATES.md` | Edited | Renamed from RELEASE-DECISION.md; removed internal staging notes; launch gates left open. |
| `evals/README.md` | Clear | Protocol with a generic test prompt; states it has not been run. |
| `fixtures/remote-mac-synthetic.json` | Clear | Fictitious: `fictional-*` handles, `example.org` URLs, explicit FICTITIOUS warning. |
| `knowledge/INDEX.md` | Clear | Index; Beam named only as an example scope. |
| `knowledge/README.md` | Clear | No private material. |
| `knowledge/shared/method-source-over-profile.md` | Clear | Draft method note; no empirical claims or sources. |
| `knowledge/templates/LEARNING-NOTE.md` | Clear | Empty template. |
| `knowledge/templates/PRIVATE-PROJECT.md` | Clear | Empty template, instructs copying outside the repo. |
| `policies/ACCESS.md` | Clear | Canonical policy. |
| `policies/CONTEXT.md` | Edited | Wording generalized ("one founder's private project research"). |
| `policies/EVIDENCE.md` | Clear | Canonical policy. |
| `policies/QUALITY.md` | Edited | Removed an unverifiable attribution to "LMTY skill presentations"; rubric unchanged. |
| `pyproject.toml` | Edited | Version 0.2.1, license MIT, name who-exactly. |
| `requirements-ci.txt` | Clear | New. Pinned public PyPI packages. |
| `requirements-dev.txt` | Clear | Public PyPI packages. |
| `schemas/candidate.schema.json` | Clear | Schema only. |
| `schemas/cohort.schema.json` | Clear | Schema only. |
| `schemas/episode.schema.json` | Clear | Schema only. |
| `schemas/mission.schema.json` | Clear | Schema only. |
| `scripts/build.py` | Clear | Rewritten with --check. |
| `scripts/install_grok_bot_skills.py` | Clear | Unchanged; dry-run by default, no network. |
| `scripts/knowledge_cli.py` | Clear | Unchanged; offline. |
| `scripts/package_release.py` | Clear | Rewritten; offline, writes dist/ only. |
| `scripts/validate.py` | Clear | Extended; contains secret-scan regexes (patterns, not secrets). |
| `skills/cohort-assembly/SKILL.md` | Edited | Added `license: MIT`; body unchanged; no real people or posts. |
| `skills/cohort-assembly/assets/COHORT-PLAN.md` | Clear | Output template. |
| `skills/cohort-assembly/assets/INVITATION.md` | Clear | Output template. |
| `skills/cohort-assembly/references/ACCESS.md` | Clear | Generated byte copy of policies/ACCESS.md. |
| `skills/cohort-assembly/references/CONTEXT.md` | Clear | Generated byte copy of policies/CONTEXT.md. |
| `skills/cohort-assembly/references/EVIDENCE.md` | Clear | Generated byte copy of policies/EVIDENCE.md. |
| `skills/cohort-assembly/references/QUALITY.md` | Clear | Generated byte copy of policies/QUALITY.md. |
| `skills/job-evidence-map/SKILL.md` | Edited | Added `license: MIT`; body unchanged; no real people or posts. |
| `skills/job-evidence-map/assets/JOB-CARD.md` | Clear | Output template. |
| `skills/job-evidence-map/references/ACCESS.md` | Clear | Generated byte copy of policies/ACCESS.md. |
| `skills/job-evidence-map/references/CONTEXT.md` | Clear | Generated byte copy of policies/CONTEXT.md. |
| `skills/job-evidence-map/references/EVIDENCE.md` | Clear | Generated byte copy of policies/EVIDENCE.md. |
| `skills/job-evidence-map/references/QUALITY.md` | Clear | Generated byte copy of policies/QUALITY.md. |
| `skills/workaround-atlas/SKILL.md` | Edited | Added `license: MIT`; body unchanged; no real people or posts. |
| `skills/workaround-atlas/assets/ALTERNATIVES-MATRIX.md` | Clear | Output template. |
| `skills/workaround-atlas/references/ACCESS.md` | Clear | Generated byte copy of policies/ACCESS.md. |
| `skills/workaround-atlas/references/CONTEXT.md` | Clear | Generated byte copy of policies/CONTEXT.md. |
| `skills/workaround-atlas/references/EVIDENCE.md` | Clear | Generated byte copy of policies/EVIDENCE.md. |
| `skills/workaround-atlas/references/QUALITY.md` | Clear | Generated byte copy of policies/QUALITY.md. |
| `skills/x-people-safari/SKILL.md` | Edited | Added `license: MIT` and `compatibility`; body unchanged; no real people or posts. |
| `skills/x-people-safari/assets/CANDIDATE-REVIEW.md` | Clear | Output template. |
| `skills/x-people-safari/references/ACCESS.md` | Clear | Generated byte copy of policies/ACCESS.md. |
| `skills/x-people-safari/references/CONTEXT.md` | Clear | Generated byte copy of policies/CONTEXT.md. |
| `skills/x-people-safari/references/EVIDENCE.md` | Clear | Generated byte copy of policies/EVIDENCE.md. |
| `skills/x-people-safari/references/QUALITY.md` | Clear | Generated byte copy of policies/QUALITY.md. |
| `src/who_exactly/__init__.py` | Edited | Version 0.2.1 (was stale 0.1.0). |
| `src/who_exactly/knowledge.py` | Clear | Offline selector. |
| `src/who_exactly/records.py` | Clear | Offline validation; no network. |
| `tests/test_adversarial_records.py` | Clear | Synthetic inputs only. |
| `tests/test_grok_skill_installer.py` | Clear | Temp directories only. |
| `tests/test_integration_flow.py` | Edited | Unrelated-product id made generic (`other-product`). Beam note is synthetic test data. |
| `tests/test_knowledge.py` | Edited | Same genericization. |
| `tests/test_records.py` | Edited | URL-normalization example used the creator's handle with a fake status id; changed to `ExampleAuthor`. |
| `tests/test_release_manifest.py` | Clear | Rewritten for new artifacts. |
| `tests/test_repo_checks.py` | Clear | New. Validator negative tests; the fake token string is built at runtime and is not a credential. |
