"""Check research record syntax/provenance; never claim remote URL truth.

IMPORTANT: A syntactically valid public X URL is not evidence a post exists.
Actual live retrieval + human source adjudication is required separately.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
URL_PATTERN = re.compile(r'^https://(?:www\.)?(?:x\.com|twitter\.com)/([A-Za-z0-9_]{1,15})/status/(\d+)(?:[/?#].*)?$', re.I)
CATEGORIES = {'included', 'possible', 'rejected', 'unknown'}


def canonical_post_url(url: str) -> str | None:
    """Normalize public X/Twitter post links. Offline syntax check only."""
    m = URL_PATTERN.fullmatch(url or '')
    return f'https://x.com/{m.group(1).lower()}/status/{m.group(2)}' if m else None


def post_id(url: str) -> str | None:
    normalized = canonical_post_url(url)
    return normalized.rsplit('/', 1)[-1] if normalized else None


def verify_episode(record: dict, require_live_receipt: bool = True) -> list[str]:
    """Validate shape and internal claims. Does not fetch or independently verify post."""
    schema = json.loads((ROOT / 'schemas' / 'episode.schema.json').read_text())
    errors = [f'schema: {e.message}' for e in Draft202012Validator(schema).iter_errors(record)]
    kind = record.get('source_kind')
    if kind in {'public_x', 'connected_x'}:
        normalized_url = canonical_post_url(record.get('source_url', ''))
        if not normalized_url:
            errors.append('source_url: not an individual X post URL')
        else:
            linked_handle = normalized_url.split('/')[3].lower()
            declared_handle = str(record.get('author_handle', '')).lstrip('@').lower()
            if linked_handle != declared_handle:
                errors.append('author_handle: original X post URL author does not match declared author; verify possible handle change')
        if require_live_receipt and record.get('retrieval_status') != 'retrieved':
            errors.append('retrieval_status: live source has not been retrieved')
        if record.get('evidence_type') == 'fixture':
            errors.append('evidence_type: a real X source cannot be a fixture')
    if kind == 'fixture':
        if record.get('retrieval_status') != 'fixture':
            errors.append('fixtures must have retrieval_status=fixture')
        if record.get('evidence_type') != 'fixture':
            errors.append('fixtures must have evidence_type=fixture')
    if record.get('retrieval_status') == 'retrieved' and not record.get('retrieved_at'):
        errors.append('retrieved source needs retrieved_at')
    if kind in {'public_x', 'connected_x'} and record.get('retrieved_at'):
        try:
            when = datetime.fromisoformat(record['retrieved_at'].replace('Z', '+00:00'))
            posted = datetime.fromisoformat(record['posted_at'].replace('Z', '+00:00'))
            if posted.tzinfo and when.tzinfo and posted > when:
                errors.append('posted_at later than retrieved_at')
        except (ValueError, TypeError, KeyError):
            errors.append('invalid source timestamp')
    return errors


def verify_candidate(candidate: dict, episodes: list[dict], require_verified_qualification: bool = False) -> list[str]:
    schema = json.loads((ROOT / 'schemas' / 'candidate.schema.json').read_text())
    errors = [f'schema: {e.message}' for e in Draft202012Validator(schema).iter_errors(candidate)]
    ids = {e.get('episode_id') for e in episodes}
    referenced = candidate.get('episode_ids', [])
    if any(i not in ids for i in referenced):
        errors.append('candidate references absent episode ids')
    if candidate.get('category') == 'included' and not referenced:
        errors.append('included candidates require source episodes')
    if require_verified_qualification and candidate.get('category') == 'included':
        matched = [e for e in episodes if e.get('episode_id') in referenced]
        if not matched:
            errors.append('included candidates require attributable source episodes')
        for ep in matched:
            if ep.get('source_kind') not in {'public_x', 'connected_x'} or ep.get('retrieval_status') != 'retrieved':
                errors.append('qualification: source is not a retrieved, real X post (fixtures do not qualify)')
            if ep.get('evidence_type') != 'firsthand_report' or not ep.get('actual_action'):
                errors.append('qualification: firsthand report of a specific action required')
            if ep.get('author_handle', '').lstrip('@').lower() != str(candidate.get('person_handle', '')).lstrip('@').lower():
                errors.append('qualification: candidate author does not match source author')
            if ep.get('author_attribution_checked') is not True:
                errors.append('qualification: original author attribution must be checked')
            errors.extend('qualification: ' + e for e in verify_episode(ep))
    return errors


def dedupe_episodes(episodes: list[dict]) -> list[dict]:
    """Keep earliest episode per post ID; other source types use stable episode ID."""
    seen = set()
    out = []
    for e in episodes:
        marker = post_id(e.get('source_url', '')) or f"episode:{e.get('episode_id')}"
        if marker not in seen:
            out.append(e)
            seen.add(marker)
    return out
