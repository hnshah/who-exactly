#!/usr/bin/env python3
"""Vendor the canonical policies/ into every skill's references/ folder.

Each skill must work when installed on its own, so the shared research
policies are copied into skills/<name>/references/ rather than linked.
policies/ is the only place to edit them.

  python scripts/build.py          # rewrite vendored copies
  python scripts/build.py --check  # change nothing; exit 1 if any copy drifted

Deterministic, offline, no external services.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICIES = ROOT / 'policies'
SKILLS = ROOT / 'skills'


def skill_dirs(root: Path = ROOT) -> list[Path]:
    return [d for d in sorted((root / 'skills').iterdir()) if d.is_dir() and (d / 'SKILL.md').exists()]


def drift(root: Path = ROOT) -> list[str]:
    """Return human-readable differences between policies/ and vendored copies."""
    policies = {p.name: p.read_bytes() for p in sorted((root / 'policies').glob('*.md'))}
    problems = []
    for d in skill_dirs(root):
        refs = d / 'references'
        for name, blob in policies.items():
            dest = refs / name
            if not dest.is_file():
                problems.append(f'{d.name}/references/{name}: missing')
            elif dest.read_bytes() != blob:
                problems.append(f'{d.name}/references/{name}: differs from policies/{name}')
    return problems


def build(root: Path = ROOT) -> None:
    policies = sorted((root / 'policies').glob('*.md'))
    for d in skill_dirs(root):
        refs = d / 'references'
        refs.mkdir(exist_ok=True)
        for p in policies:
            (refs / p.name).write_bytes(p.read_bytes())
        print(f'updated {d.name}: {len(policies)} shared references')


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='report drift without writing')
    args = ap.parse_args(argv)
    if args.check:
        problems = drift()
        for p in problems:
            print('DRIFT:', p)
        if problems:
            print('Run python scripts/build.py and commit the result.', file=sys.stderr)
            return 1
        print(f'PASS: vendored references match policies/ in {len(skill_dirs())} skills')
        return 0
    build()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
