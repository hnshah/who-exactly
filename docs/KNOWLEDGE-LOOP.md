# Test and use GitHub research context with Who Exactly?

**Status:** offline reference behavior (developer alpha). This is not a live Grok Bot
integration, and a GitHub URL by itself never auto-enables or updates skills.

## The architectural split

- Installed skills: how to research, qualify, investigate and invite.
- Public versioned knowledge: generic methods, reviewed patterns and examples.
- Founder-owned private project context: product decisions, source episodes,
  counterexamples, corrections and past research. This is outside the public
  skill pack. Connect a private repository only when authorized and necessary.
- Evaluation fixtures: synthetic or explicitly permissioned and access-limited.

## First local test

```bash
python scripts/knowledge_cli.py validate
python scripts/knowledge_cli.py select --tags qualification,firsthand-evidence
python -m pytest -q tests/test_knowledge.py tests/test_integration_flow.py
```

The bundled public note is intentionally **draft**, so the CLI returns no
approved notes. The tests create temporary, *fictional* reviewed notes and
show that the right one loads for the `beam` example project, not for an
unrelated `other-product` project, and only after review.

## In a private Grok Bot

1. Set the product/job and the research decision. Load the matching enabled
   skill. No extra login for public X.
2. If GitHub context has been made available, read `knowledge/INDEX.md` from
   a known, pinned source revision. Review the index before selecting a note.
3. For public reusable knowledge, load only reviewed, job-matching notes and
   carry their dates. Do not treat a draft or an example as verified evidence.
4. For product-specific context, retrieve its files **only** from the current
   user's explicitly authorized private workspace/repository. If access isn't
   granted, do the job without that context rather than guessing.
5. Use prior notes as a starting hypothesis, not as proof of a current X post.
   A new dated public retrieval is needed for a new person-level claim.
6. After research, prepare a specific proposed correction or learning note.
   Show the source, scope, rival explanation, and affected project. Get
   approval before modifying repository files. Never auto-promote private
   research to the public shared methodology.
7. A reviewed reusable method change still needs a regression test and
   versioned skill release. A knowledge edit doesn't silently replace the
   installed skill.

## Three reproducible prompts for the installed Bot

**Test 1: Read the right context**

> For the Beam example project, check the current product context and existing disqualifiers
> before finding public X examples of remote interactive Mac workflows.
> Tell me which approved knowledge files you actually read, the revision,
> and what remains unverified.

**Test 2: Record a correction without generalizing it**

> In Beam research, a terminal-only developer who doesn't need an
> interactive GUI is a non-fit. Propose a private project-specific
> qualification change with a counterexample and a future regression test.
> Show me the change before writing to GitHub.

**Test 3: No cross-project leakage**

> Now I'm researching conversion optimization for an unrelated website
> analytics product. Ignore Beam-specific qualification rules unless there is independent evidence
> that makes a general rule relevant. Identify the context you did load.

## Evidence receipt and baseline

For every test capture model/version, Grok Bot ID, enabled skills, connected
apps, time, source URL and actual tool result. Check whether a source is
accessible, authored by the claimed person, about the relevant task, and
current. Human source review is required; the Python validators cannot
fetch or verify X posts.

## GitHub operating model

A public source repo can be checked by a Bot with public internet access.
A private project repo requires a GitHub connection with the right grant.
Bot users do not inherit the author's GitHub or X credentials when they
import a template. Files on the Grok Bot cloud computer are visible to
other Bots belonging to the same account, so don't describe them as
private *between Bots*.

**GitHub version** != **installed skill version**. Read relevant contextual
notes on demand; install/upgrade skills only from a reviewed pinned tag or
commit, with checksums, backup, approval and a post-install skill-menu test.
