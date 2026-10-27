#!/usr/bin/env python3
"""Build reproducible, checksummed Who Exactly? release artifacts.

Writes to dist/ (or --out-dir):

  who-exactly-v<version>.zip                 full source, one who-exactly/ wrapper,
                                             with an internal MANIFEST.json
  who-exactly-<skill>-v<version>.zip         one per skill, a single <skill>/ folder
  who-exactly-v<version>-manifest.json       SHA-256 of every archive and every file
  who-exactly-v<version>-SHA256SUMS.txt      `sha256sum -c` compatible

Deterministic: sorted entries, one fixed timestamp, fixed permissions. Building
twice from the same tree gives byte-identical files. Offline; publishes nothing.

  python scripts/package_release.py --check            build, then re-verify
  python scripts/package_release.py --check-tag v0.2.1 also fail unless the tag matches
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 10, 27, 0, 0, 0)
SKILLS = ('cohort-assembly', 'job-evidence-map', 'workaround-atlas', 'x-people-safari')
IGNORE_DIRS = {'.git', '__pycache__', '.pytest_cache', '.venv', 'dist', 'node_modules', '.ruff_cache'}
IGNORE_SUFFIXES = ('.pyc', '.pyo', '.zip')
IGNORE_NAMES = {'.env', '.DS_Store', 'MANIFEST.json'}
WRAPPER = 'who-exactly'
NOTE = 'Packaging integrity only. Not a signature, and not evidence of live X or Grok Bot behavior.'


def version(root: Path = ROOT) -> str:
    text = (root / 'src/who_exactly/__init__.py').read_text(encoding='utf-8')
    m = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", text, re.M)
    if not m:
        raise ValueError('no __version__ in src/who_exactly/__init__.py')
    return m.group(1)


def members(base: Path, root: Path):
    for path in sorted(base.rglob('*')):
        rel = path.relative_to(root)
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f'release must not include symlinks: {rel}')
        if not path.is_file() or path.suffix in IGNORE_SUFFIXES or path.name in IGNORE_NAMES:
            continue
        yield path


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def zip_bytes(files: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            archive.writestr(info, files[name], compresslevel=9)
    return buf.getvalue()


def build(out_dir: Path, root: Path = ROOT) -> dict:
    v = version(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    archives: dict[str, dict[str, bytes]] = {}

    source = {f'{WRAPPER}/{p.relative_to(root).as_posix()}': p.read_bytes() for p in members(root, root)}
    inner = {'version': v, 'algorithm': 'SHA-256', 'note': NOTE,
             'files': {name: sha(blob) for name, blob in sorted(source.items())}}
    source[f'{WRAPPER}/MANIFEST.json'] = (json.dumps(inner, sort_keys=True, indent=2) + '\n').encode()
    archives[f'who-exactly-v{v}.zip'] = source

    for skill in SKILLS:
        base = root / 'skills' / skill
        if not (base / 'SKILL.md').is_file():
            raise ValueError(f'missing skills/{skill}/SKILL.md')
        archives[f'who-exactly-{skill}-v{v}.zip'] = {
            f'{skill}/{p.relative_to(base).as_posix()}': p.read_bytes() for p in members(base, root)}

    manifest = {'name': 'who-exactly', 'version': v, 'algorithm': 'SHA-256', 'note': NOTE, 'archives': {}}
    for name, files in archives.items():
        blob = zip_bytes(files)
        (out_dir / name).write_bytes(blob)
        manifest['archives'][name] = {'sha256': sha(blob), 'bytes': len(blob),
                                      'files': {f: sha(b) for f, b in sorted(files.items())}}
    manifest_name = f'who-exactly-v{v}-manifest.json'
    manifest_blob = (json.dumps(manifest, sort_keys=True, indent=2) + '\n').encode()
    (out_dir / manifest_name).write_bytes(manifest_blob)
    sums = {**{n: m['sha256'] for n, m in manifest['archives'].items()}, manifest_name: sha(manifest_blob)}
    (out_dir / f'who-exactly-v{v}-SHA256SUMS.txt').write_text(
        ''.join(f'{digest}  {name}\n' for name, digest in sorted(sums.items())), encoding='utf-8')
    return manifest


def verify(out_dir: Path, v: str) -> list[str]:
    problems = []
    manifest = json.loads((out_dir / f'who-exactly-v{v}-manifest.json').read_text(encoding='utf-8'))
    for line in (out_dir / f'who-exactly-v{v}-SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if sha((out_dir / name).read_bytes()) != digest:
            problems.append(f'{name}: SHA256SUMS mismatch')
    for name, meta in manifest['archives'].items():
        with zipfile.ZipFile(out_dir / name) as z:
            entries = z.namelist()
            if len(entries) != len(set(entries)):
                problems.append(f'{name}: duplicate entries')
            if set(entries) != set(meta['files']):
                problems.append(f'{name}: entries differ from manifest')
            for entry, digest in meta['files'].items():
                if sha(z.read(entry)) != digest:
                    problems.append(f'{name}: hash mismatch {entry}')
            bad = [e for e in entries if any(x in e for x in ('__pycache__', '.pytest_cache', '/.env', '/.git/', '..'))]
            if bad:
                problems.append(f'{name}: forbidden entries {bad}')
            skills = [e for e in entries if e.endswith('/SKILL.md')]
            if name == f'who-exactly-v{v}.zip':
                if len(skills) != 4 or not all(e.startswith(f'{WRAPPER}/') for e in entries):
                    problems.append(f'{name}: expected 4 skills under {WRAPPER}/')
                inner = json.loads(z.read(f'{WRAPPER}/MANIFEST.json'))
                if set(inner['files']) != set(entries) - {f'{WRAPPER}/MANIFEST.json'}:
                    problems.append(f'{name}: internal MANIFEST.json path mismatch')
            else:
                tops = {e.split('/', 1)[0] for e in entries}
                if len(skills) != 1 or len(tops) != 1 or skills[0] != f'{tops.pop()}/SKILL.md':
                    problems.append(f'{name}: must hold exactly one skill folder with SKILL.md at its root')
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='re-open and verify every artifact after building')
    ap.add_argument('--check-tag', help='fail unless this equals v<version>')
    ap.add_argument('--out-dir', type=Path, default=ROOT / 'dist')
    args = ap.parse_args(argv)
    try:
        v = version()
        if args.check_tag and args.check_tag != f'v{v}':
            print(f'FAIL: tag {args.check_tag} does not match version {v}', file=sys.stderr)
            return 1
        manifest = build(args.out_dir)
        problems = verify(args.out_dir, v) if args.check else []
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as err:
        print(f'FAIL: {err}', file=sys.stderr)
        return 1
    for p in problems:
        print('FAIL:', p, file=sys.stderr)
    if problems:
        return 1
    for name, meta in sorted(manifest['archives'].items()):
        print(f"{meta['sha256']}  {name}  ({meta['bytes']:,} bytes, {len(meta['files'])} files)")
    print(f'PASS: v{v} artifacts in {args.out_dir}' + (' (verified)' if args.check else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
