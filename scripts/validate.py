#!/usr/bin/env python3
"""Structural validator for the Who Exactly? repository.

Checks Agent Skills shape, standalone packaging, shared-policy parity, version
consistency, relative links and obvious secrets. This is NOT an evaluation of
source discovery or Grok Bot runtime behavior. The official `skills-ref`
validator runs separately (see .github/workflows/ci.yml).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = ('cohort-assembly', 'job-evidence-map', 'workaround-atlas', 'x-people-safari')
ALLOWED = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
ALLOWED_METADATA = {'author'}
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
REFS = re.compile(r'`((?:references|assets|scripts)/[^`]+)`')
MD_LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)\)')
SKIP_DIRS = {'.git', 'dist', '__pycache__', '.pytest_cache', '.venv', 'node_modules'}
TEXT_SUFFIXES = {'.md', '.py', '.json', '.toml', '.txt', '.yml', '.yaml', '.cfg', ''}
SECRET_PATTERNS = [
    re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{40,}'),
    re.compile(r'\bsk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'\bxox[abposr]-[A-Za-z0-9-]{10,}'),
    re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    re.compile(r'(?i)\b(?:api[_-]?key|secret|password|bearer)\b\s*[:=]\s*["\'][^"\'\s]{12,}["\']'),
]
LOCAL_PATH = re.compile(r'(?:/Users/[A-Za-z]|/home/[a-z][a-z0-9_-]*/|[A-Z]:\\\\Users)')


def repo_files(root: Path):
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts) or not p.is_file():
            continue
        yield p


def check_skill(d: Path, root: Path) -> list[str]:
    problems = []
    file = d / 'SKILL.md'
    if not file.exists():
        return [f'{d.name}: missing SKILL.md']
    text = file.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return [f'{d.name}: missing YAML frontmatter']
    try:
        meta = yaml.safe_load(text.split('---\n', 2)[1])
    except (IndexError, yaml.YAMLError) as exc:
        return [f'{d.name}: invalid frontmatter {exc}']
    if not isinstance(meta, dict):
        return [f'{d.name}: frontmatter is not a mapping']
    name, description = meta.get('name'), meta.get('description')
    if name != d.name or not SLUG.fullmatch(str(name or '')) or len(name or '') > 64:
        problems.append(f'{d.name}: invalid or mismatched name {name!r}')
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        problems.append(f'{d.name}: description must be 1-1024 characters')
    extra = set(meta) - ALLOWED
    if extra:
        problems.append(f'{d.name}: unsupported frontmatter keys {sorted(extra)}')
    if meta.get('license') != 'MIT':
        problems.append(f'{d.name}: license must be MIT so a standalone copy carries it')
    compat = meta.get('compatibility')
    if compat is not None and (not isinstance(compat, str) or not 1 <= len(compat) <= 500):
        problems.append(f'{d.name}: compatibility must be 1-500 characters')
    md = meta.get('metadata') or {}
    if not isinstance(md, dict) or set(md) - ALLOWED_METADATA:
        problems.append(f'{d.name}: metadata may only contain {sorted(ALLOWED_METADATA)}; '
                        'the pack is versioned once in src/who_exactly/__init__.py')
    elif md.get('author') != 'Hiten Shah':
        problems.append(f'{d.name}: metadata.author must be Hiten Shah')
    referenced = set(REFS.findall(text))
    for rel in sorted(referenced):
        if not (d / rel).is_file():
            problems.append(f'{d.name}: missing referenced file {rel}')
    shipped = {p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()} - {'SKILL.md'}
    for orphan in sorted(shipped - referenced):
        problems.append(f'{d.name}: {orphan} ships but SKILL.md never references it')
    for link in MD_LINK.findall(text):
        if link.startswith('../') or link.startswith('/'):
            problems.append(f'{d.name}: link {link} escapes the skill folder')
    policies = {p.name for p in (root / 'policies').glob('*.md')}
    vendored = {p.name for p in (d / 'references').glob('*')} if (d / 'references').is_dir() else set()
    for missing in sorted(policies - vendored):
        problems.append(f'{d.name}: missing vendored references/{missing}')
    for name in sorted(policies & vendored):
        if (d / 'references' / name).read_bytes() != (root / 'policies' / name).read_bytes():
            problems.append(f'{d.name}: references/{name} differs from policies/{name}; run scripts/build.py')
    for stray in sorted(vendored - policies):
        problems.append(f'{d.name}: references/{stray} has no canonical source in policies/')
    if '## Do not use' not in text:
        problems.append(f'{d.name}: missing "## Do not use" boundary section')
    return problems


def read_versions(root: Path) -> dict[str, str | None]:
    init = (root / 'src/who_exactly/__init__.py').read_text(encoding='utf-8')
    pyproject = (root / 'pyproject.toml').read_text(encoding='utf-8')
    changelog = (root / 'CHANGELOG.md').read_text(encoding='utf-8')
    find = lambda pat, s: (m.group(1) if (m := re.search(pat, s, re.M)) else None)
    return {
        'src/who_exactly/__init__.py': find(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", init),
        'pyproject.toml': find(r'^version\s*=\s*"([^"]+)"', pyproject),
        'CHANGELOG.md': find(r'^## \[?(\d+\.\d+\.\d+)\]?', changelog),
    }


def validate(root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    dirs = [d for d in sorted((root / 'skills').iterdir()) if d.is_dir()]
    if tuple(d.name for d in dirs) != EXPECTED_SKILLS:
        problems.append(f'skills/ must contain exactly {EXPECTED_SKILLS}, found {[d.name for d in dirs]}')
    for d in dirs:
        problems += check_skill(d, root)
    versions = read_versions(root)
    if len(set(versions.values())) != 1 or None in versions.values():
        problems.append(f'version mismatch: {versions}')
    for p in repo_files(root):
        if p.suffix not in TEXT_SUFFIXES:
            continue
        rel = p.relative_to(root).as_posix()
        try:
            text = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        if rel != 'scripts/validate.py':
            for pat in SECRET_PATTERNS:
                if pat.search(text):
                    problems.append(f'{rel}: possible secret matching {pat.pattern[:30]}')
            if LOCAL_PATH.search(text):
                problems.append(f'{rel}: absolute local user path')
        if '\r' in text:
            problems.append(f'{rel}: CRLF line endings')
        if p.suffix == '.md':
            for link in MD_LINK.findall(text):
                if re.match(r'^[a-z]+:', link) or link.startswith('#'):
                    continue
                target = (p.parent / link.split('#', 1)[0]).resolve()
                if not target.exists():
                    problems.append(f'{rel}: broken relative link {link}')
    return problems


def main() -> int:
    problems = validate()
    for p in problems:
        print('FAIL:', p)
    if problems:
        return 1
    v = read_versions(ROOT)['pyproject.toml']
    print(f'PASS: v{v}; {len(EXPECTED_SKILLS)} self-contained Agent Skills; vendored policies in sync; '
          'versions consistent; relative links resolve; no secrets or local paths found')
    return 0


if __name__ == '__main__':
    sys.exit(main())
