# Contributing

Thanks for helping. There are two kinds of contribution: **research lessons** and **code or docs**.

## Research lessons

Real research turns up corrections, for example "bios that mention the job were usually not practitioners". A lesson like that becomes a shared rule only after review:

1. **Draft.** Copy [knowledge/templates/LEARNING-NOTE.md](knowledge/templates/LEARNING-NOTE.md) into `knowledge/shared/` and keep `status: draft`. Fill in:
   - `applies_when`: the exact job or setup
   - `does_not_apply_when`
   - `source_urls`: public sources only

   Draft notes are never loaded automatically.
2. **Scope.** State only what your evidence supports. One project's finding is not a general rule. If the finding depends on private project data, keep it in your own private workspace (see [knowledge/templates/PRIVATE-PROJECT.md](knowledge/templates/PRIVATE-PROJECT.md)), not here.
3. **Review.** Open a PR. A reviewer other than the author checks the sources and scope, then sets `status: reviewed`, `reviewed_by` and `last_verified`.
4. **Promote, rarely.** A lesson that holds up across several jobs can become an edit to `policies/`. Run `python scripts/build.py` so every skill gets the change.

Never include participant names, handles, private messages, non-public posts, or anything someone did not publish themselves.

## Code and docs

- Run the checks in [AGENTS.md](AGENTS.md) before opening a PR. CI runs the same checks.
- Keep fixtures synthetic and labeled.
- Update CHANGELOG.md under a new version heading when behavior or packaging changes.

## License

By contributing, you agree your contribution is licensed under the [MIT License](LICENSE).
