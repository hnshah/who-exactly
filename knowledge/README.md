# Knowledge and research continuity

The four portable Agent Skills teach a method. This directory is a separately
maintained set of **contextual data** that can improve repeat research.

- Shared, reviewed, scoped notes may be retrieved for relevant jobs.
- Draft notes are excluded from automatic retrieval.
- Product-specific records live in a founder-controlled private workspace.
- Public self-reports are not observed product use, consent or market share.
- Do not silently promote private material to a reusable public method.

## Test the local selection engine

```bash
python scripts/knowledge_cli.py validate
python scripts/knowledge_cli.py select --tags qualification,firsthand-evidence
```

The latter currently returns no reviewed notes, intentionally: the sample
method is a proposed draft. A real project note can be selected by passing
both `--private-dir` and `--project-id` to a directory the founder has
explicitly authorized. No private project path is bundled or selected by
default.

GitHub is **versioned storage**, not automatic model memory or a skill
loader. In Grok Bot, users must install/enable actual skills and request
access to private GitHub repos only when needed.
