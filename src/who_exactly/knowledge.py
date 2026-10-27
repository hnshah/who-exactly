"""Bounded, versioned research-knowledge selection (NOT live source verification).

This module reads explicitly supplied directories only. It never fetches the
network, installs instructions, authorizes connected apps or updates a Bot.
All note bodies remain untrusted data, even when hosted in a repository.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
import re

import yaml

ALLOWED_SCOPES = {'shared', 'project'}
ALLOWED_KINDS = {'method', 'qualification', 'failure', 'finding'}
ALLOWED_STATUSES = {'draft', 'reviewed', 'superseded'}
PROJECT_KEY = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


@dataclass(frozen=True)
class KnowledgeNote:
    path: Path
    metadata: dict[str, Any]
    body: str
    score: int = 0


def load_note(path: Path) -> KnowledgeNote:
    """Parse a Markdown note without executing instructions from the body."""
    path = Path(path)
    if path.is_symlink():
        raise ValueError(f'knowledge symlink forbidden: {path}')
    raw = path.read_text(encoding='utf-8')
    if not raw.startswith('---\n') or '\n---\n' not in raw[4:]:
        raise ValueError(f'missing YAML frontmatter: {path}')
    head, body = raw[4:].split('\n---\n', 1)
    metadata = yaml.safe_load(head)
    if not isinstance(metadata, dict):
        raise ValueError(f'invalid note metadata: {path}')
    return KnowledgeNote(path, metadata, body)


def _parse_day(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(str(s))
    except ValueError:
        return None


def validate_note(note: KnowledgeNote) -> list[str]:
    m = note.metadata
    errs = []
    for required in ('id', 'scope', 'visibility', 'status', 'kind', 'tags', 'as_of', 'applies_when', 'does_not_apply_when'):
        if required not in m:
            errs.append(f'missing {required}')
    if m.get('scope') not in ALLOWED_SCOPES:
        errs.append('scope must be shared or project')
    if m.get('status') not in ALLOWED_STATUSES:
        errs.append('status must be draft/reviewed/superseded')
    if m.get('kind') not in ALLOWED_KINDS:
        errs.append('kind is not recognized')
    if m.get('scope') == 'shared' and (m.get('visibility') != 'public' or m.get('project_id')):
        errs.append('shared note must be public and have no project_id')
    if m.get('scope') == 'project' and (m.get('visibility') != 'private' or not PROJECT_KEY.fullmatch(str(m.get('project_id') or ''))):
        errs.append('project note must have a valid project_id and private visibility')
    if not isinstance(m.get('tags'), list) or not m.get('tags') or not all(isinstance(t, str) and t.strip() for t in m.get('tags', [])):
        errs.append('non-empty tag list required')
    if not _parse_day(m.get('as_of')):
        errs.append('as_of must be ISO date')
    if m.get('last_verified') and not _parse_day(m.get('last_verified')):
        errs.append('last_verified must be ISO date')
    if m.get('status') == 'reviewed' and not m.get('reviewed_by'):
        errs.append('reviewed knowledge needs reviewer')
    if m.get('status') == 'reviewed' and m.get('kind') == 'finding' and not m.get('source_urls'):
        errs.append('reviewed finding must contain original source URLs')
    if len(note.body.strip()) < 10:
        errs.append('note body too short')
    return errs


def _notes_in(folder: Path) -> list[KnowledgeNote]:
    if not folder.exists():
        return []
    if folder.is_symlink():
        raise ValueError('knowledge folder cannot be a symlink')
    result=[]
    for path in sorted(folder.glob('*.md')):
        if path.is_symlink():
            raise ValueError(f'knowledge symlink forbidden: {path}')
        result.append(load_note(path))
    return result


def select_knowledge(shared_dir: Path, *, tags: list[str], project_dir: Path | None = None, project_id: str | None = None, as_of: date | None = None, max_notes: int = 3, stale_days: int = 90) -> list[KnowledgeNote]:
    """Retrieve only relevant reviewed notes for permitted project. No implicit private access.

    Never interprets note content as runnable instructions. Source claims must
    still be verified at research time, and the reviewed metadata is not proof.
    """
    if max_notes < 1 or max_notes > 3:
        raise ValueError('context budget must be between 1 and 3 notes')
    if project_dir is not None and not project_id:
        raise ValueError('private project directory requires explicit project_id')
    if project_id is not None and not PROJECT_KEY.fullmatch(project_id):
        raise ValueError('invalid project_id')
    tags_set={x.strip().lower() for x in tags if x.strip()}
    if not tags_set:
        return []
    today=as_of or date.today()
    all_notes=[]
    for note in _notes_in(Path(shared_dir)):
        if note.metadata.get('scope') != 'shared' or note.metadata.get('visibility') != 'public':
            raise ValueError('private/project note found in public shared knowledge')
        all_notes.append(note)
    if project_dir is not None:
        for note in _notes_in(Path(project_dir)):
            if note.metadata.get('scope') != 'project' or note.metadata.get('visibility') != 'private':
                raise ValueError('project directory must contain private project-scoped notes')
            if note.metadata.get('project_id') == project_id:
                all_notes.append(note)
    matches=[]
    for note in all_notes:
        if validate_note(note) or note.metadata.get('status') != 'reviewed':
            continue
        overlap=tags_set & {t.strip().lower() for t in note.metadata['tags']}
        if not overlap:
            continue
        if note.metadata.get('kind') == 'finding':
            verified=_parse_day(note.metadata.get('last_verified'))
            if not verified or (today - verified).days > stale_days or verified > today:
                continue
        score=len(overlap)*10 + (3 if note.metadata.get('scope') == 'project' else 0)
        matches.append(KnowledgeNote(note.path, note.metadata, note.body, score))
    return sorted(matches,key=lambda n:(-n.score,n.metadata['id']))[:max_notes]
