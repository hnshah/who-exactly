"""Offline release artifact integrity, without claiming cryptographic signing."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import package_release  # noqa: E402

V = package_release.version()
SKILLS = package_release.SKILLS


def run(out, *extra, root=ROOT):
    return subprocess.run([sys.executable, str(root / 'scripts/package_release.py'), '--check',
                           '--out-dir', str(out), *extra], capture_output=True, text=True)


def test_full_package_has_verified_internal_manifest(tmp_path):
    proc = run(tmp_path)
    assert proc.returncode == 0, proc.stderr
    with zipfile.ZipFile(tmp_path / f'who-exactly-v{V}.zip') as z:
        inner = json.loads(z.read('who-exactly/MANIFEST.json'))
        assert inner['version'] == V
        assert len(inner['files']) >= 50
        for name, digest in inner['files'].items():
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
        assert sum(x.endswith('/SKILL.md') for x in z.namelist()) == 4
        assert not any('/dist/' in n or '/.git/' in n for n in z.namelist())


def test_each_skill_zip_is_standalone(tmp_path):
    assert run(tmp_path).returncode == 0
    for skill in SKILLS:
        with zipfile.ZipFile(tmp_path / f'who-exactly-{skill}-v{V}.zip') as z:
            names = z.namelist()
            assert {n.split('/', 1)[0] for n in names} == {skill}
            assert f'{skill}/SKILL.md' in names
            for policy in (ROOT / 'policies').glob('*.md'):
                assert z.read(f'{skill}/references/{policy.name}') == policy.read_bytes()


def test_sha256sums_and_manifest_cover_every_archive(tmp_path):
    assert run(tmp_path).returncode == 0
    sums = dict(reversed(line.split('  ', 1)) for line in
                (tmp_path / f'who-exactly-v{V}-SHA256SUMS.txt').read_text().splitlines())
    expected = {f'who-exactly-v{V}.zip', f'who-exactly-v{V}-manifest.json',
                *(f'who-exactly-{s}-v{V}.zip' for s in SKILLS)}
    assert set(sums) == expected
    for name, digest in sums.items():
        assert hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() == digest


def test_release_is_byte_reproducible(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    assert run(a).returncode == 0 and run(b).returncode == 0
    for p in sorted(a.iterdir()):
        assert p.read_bytes() == (b / p.name).read_bytes(), p.name


def test_tag_must_match_version(tmp_path):
    assert run(tmp_path, '--check-tag', f'v{V}').returncode == 0
    bad = run(tmp_path / 'x', '--check-tag', 'v9.9.9')
    assert bad.returncode == 1 and 'does not match' in bad.stderr


def test_repackage_from_fresh_extraction(tmp_path):
    """Regression: an unpacked release already contains MANIFEST.json."""
    source = tmp_path / 'who-exactly'
    shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', '.git', 'dist'))
    (source / 'MANIFEST.json').write_text('{"from":"previous release"}')
    out = tmp_path / 'out'
    proc = run(out, root=source)
    assert proc.returncode == 0, proc.stderr
    with zipfile.ZipFile(out / f'who-exactly-v{V}.zip') as archive:
        assert archive.namelist().count('who-exactly/MANIFEST.json') == 1
        doc = json.loads(archive.read('who-exactly/MANIFEST.json'))
        assert 'who-exactly/MANIFEST.json' not in doc['files']
