#!/usr/bin/env python3
"""Install the four portable Who Exactly? skills into a chosen Grok Bot skill directory.

Dry-run by default. Requires an explicit destination. Never installs packages,
fetches the network, publishes, changes connectors, or enables a skill in the UI.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
SKILLS = ("job-evidence-map", "x-people-safari", "workaround-atlas", "cohort-assembly")


def digest_folder(folder: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(folder.rglob("*")):
        if f.is_file():
            if f.is_symlink():
                raise ValueError(f"Symlink not allowed: {f}")
            h.update(f.relative_to(folder).as_posix().encode("utf-8"))
            h.update(f.read_bytes())
    return h.hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--destination", required=True, help="Actual inspected private skill library directory")
    ap.add_argument("--apply", action="store_true", help="Make changes after inspecting the default dry-run")
    ap.add_argument("--replace", action="store_true", help="Replace changed existing skills, with required backups")
    ap.add_argument("--backup-dir", help="Directory outside the active skills directory to keep old versions")
    args = ap.parse_args(argv)
    raw_dest = Path(args.destination).expanduser().absolute()
    if raw_dest.is_symlink():
        ap.error("destination cannot be a symlink")
    dest = raw_dest.resolve(strict=False)
    if args.replace and not args.backup_dir:
        ap.error("--replace also requires --backup-dir outside the active skill tree")
    if args.backup_dir:
        backup = Path(args.backup_dir).expanduser().resolve(strict=False)
        if backup == dest or dest in backup.parents:
            ap.error("backup-dir must not be inside the active skill library")
    else:
        backup = None
    proposals = []
    for slug in SKILLS:
        source = SOURCE / slug
        target = dest / slug
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"Missing source skill: {slug}")
        if target.is_symlink() or (target.exists() and not target.is_dir()):
            raise SystemExit(f"Unsafe existing destination: {target}")
        if not target.exists():
            action = "INSTALL"
        elif digest_folder(source) == digest_folder(target):
            action = "UNCHANGED"
        else:
            action = "REPLACE" if args.replace else "BLOCKED (already installed with different files)"
        proposals.append((slug, source, target, action))
        print(f"{action:50} {target}")
    if any(a.startswith("BLOCKED") for _, _, _, a in proposals):
        print("No files changed; use --replace --backup-dir only after review.", file=sys.stderr)
        return 2
    if not args.apply:
        print("DRY-RUN ONLY. Confirm correct Grok Bot skill library, then add --apply.")
        return 0
    dest.mkdir(parents=True, exist_ok=True)
    for slug, source, target, action in proposals:
        if action == "UNCHANGED":
            continue
        if action == "REPLACE":
            assert backup is not None
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            archived = backup / f"{slug}-{stamp}"
            archived.parent.mkdir(parents=True, exist_ok=True)
            if archived.exists():
                raise SystemExit(f"Backup already exists: {archived}")
            shutil.move(target, archived)
            print(f"BACKUP {target} -> {archived}")
        shutil.copytree(source, target, symlinks=False)
        if digest_folder(source) != digest_folder(target):
            raise SystemExit(f"Verification failed after copy: {slug}")
        print(f"VERIFIED {slug} sha256:{digest_folder(target)}")
    print("Copied skills. NEXT: verify four names appear in the Bot's enabled / skills menu.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
