"""Repository guards: shared-policy sync, validator negatives, version consistency."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build  # noqa: E402
import validate  # noqa: E402


def copy_repo(tmp_path):
    dst = tmp_path / 'repo'
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', '.git', 'dist'))
    return dst


def test_repository_validates_clean():
    assert validate.validate(ROOT) == []


def test_vendored_references_match_policies():
    assert build.drift(ROOT) == []


def test_build_check_detects_and_build_repairs_drift(tmp_path):
    repo = copy_repo(tmp_path)
    (repo / 'policies/QUALITY.md').write_text('edited canonical policy\n')
    assert len(build.drift(repo)) == 4
    assert any('differs from policies/QUALITY.md' in p for p in validate.validate(repo))
    build.build(repo)
    assert build.drift(repo) == []


def test_validator_rejects_per_skill_version_and_missing_license(tmp_path):
    repo = copy_repo(tmp_path)
    p = repo / 'skills/workaround-atlas/SKILL.md'
    p.write_text(p.read_text().replace('license: MIT\n', '').replace(
        'author: Hiten Shah\n', 'author: Hiten Shah\n  version: "9"\n'))
    problems = validate.validate(repo)
    assert any('license must be MIT' in x for x in problems)
    assert any('metadata may only contain' in x for x in problems)


def test_validator_rejects_orphans_strays_and_extra_skills(tmp_path):
    repo = copy_repo(tmp_path)
    (repo / 'skills/job-evidence-map/references/NOTES.md').write_text('stray\n')
    shutil.copytree(repo / 'skills/job-evidence-map', repo / 'skills/fifth-skill')
    problems = validate.validate(repo)
    assert any('ships but SKILL.md never references it' in x for x in problems)
    assert any('no canonical source in policies/' in x for x in problems)
    assert any('must contain exactly' in x for x in problems)


def test_validator_rejects_version_drift_secret_and_broken_link(tmp_path):
    repo = copy_repo(tmp_path)
    init = repo / 'src/who_exactly/__init__.py'
    init.write_text(init.read_text().replace("__version__ = '", "__version__ = '9."))
    (repo / 'docs/BAD.md').write_text('[x](missing.md)\ntoken ghp_' + 'A' * 36 + '\n')
    problems = validate.validate(repo)
    assert any('version mismatch' in x for x in problems)
    assert any('broken relative link missing.md' in x for x in problems)
    assert any('possible secret' in x for x in problems)


def test_build_check_cli_passes():
    proc = subprocess.run([sys.executable, str(ROOT / 'scripts/build.py'), '--check'], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
