from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "install_grok_bot_skills.py"


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *args], text=True, capture_output=True)


def test_dry_run_makes_no_files(tmp_path):
    dst = tmp_path / "workflows"
    p = run("--destination", str(dst))
    assert p.returncode == 0, p.stderr
    assert "DRY-RUN" in p.stdout
    assert not dst.exists()


def test_apply_and_idempotent(tmp_path):
    dst = tmp_path / "workflows"
    p = run("--destination", str(dst), "--apply")
    assert p.returncode == 0, p.stderr
    assert len(list(dst.glob("*/SKILL.md"))) == 4
    p2 = run("--destination", str(dst), "--apply")
    assert p2.returncode == 0, p2.stderr
    assert p2.stdout.count("UNCHANGED") == 4


def test_modified_existing_requires_explicit_replace_and_backup(tmp_path):
    dst = tmp_path / "workflows"
    assert run("--destination", str(dst), "--apply").returncode == 0
    f = dst / "x-people-safari" / "SKILL.md"
    f.write_text(f.read_text() + "\nmodified locally\n")
    p = run("--destination", str(dst), "--apply")
    assert p.returncode == 2
    assert "modified locally" in f.read_text()
    backup = tmp_path / "backups"
    p2 = run("--destination", str(dst), "--replace", "--backup-dir", str(backup), "--apply")
    assert p2.returncode == 0, p2.stderr
    assert "modified locally" not in f.read_text()
    assert any("modified locally" in x.read_text() for x in backup.glob("*/SKILL.md"))


def test_symlink_destination_is_rejected(tmp_path):
    actual = tmp_path / "real-workflows"
    actual.mkdir()
    symlink = tmp_path / "link-workflows"
    symlink.symlink_to(actual, target_is_directory=True)
    result = run("--destination", str(symlink), "--apply")
    assert result.returncode != 0
    assert not list(actual.iterdir())
