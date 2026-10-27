"""New regression cases found while testing the v0.1.1 release candidate."""
import copy
import json
from pathlib import Path

from who_exactly.records import verify_candidate, verify_episode

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "fixtures" / "remote-mac-synthetic.json").read_text())


def example_real_episode():
    rec = copy.deepcopy(DATA["episodes"][0])
    rec.update(
        source_kind="public_x",
        source_url="https://x.com/exampleauthor/status/123456",
        author_handle="exampleauthor",
        retrieved_at="2026-10-06T10:00:00Z",
        posted_at="2026-10-05T10:00:00Z",
        retrieval_status="retrieved",
        evidence_type="firsthand_report",
        author_attribution_checked=True,
    )
    return rec


def test_production_review_does_not_qualify_a_synthetic_person():
    candidate = copy.deepcopy(DATA["candidates"][0])
    assert verify_candidate(candidate, DATA["episodes"], require_verified_qualification=True)


def test_production_review_rejects_promotional_episode_as_proof():
    ep = example_real_episode()
    ep["evidence_type"] = "promotion"
    candidate = copy.deepcopy(DATA["candidates"][0])
    candidate.update(person_handle="exampleauthor", episode_ids=[ep["episode_id"]])
    assert any("firsthand" in msg for msg in verify_candidate(candidate, [ep], require_verified_qualification=True))


def test_production_review_rejects_wrong_author():
    ep = example_real_episode()
    candidate = copy.deepcopy(DATA["candidates"][0])
    candidate.update(person_handle="anotherperson", episode_ids=[ep["episode_id"]])
    assert any("author" in msg for msg in verify_candidate(candidate, [ep], require_verified_qualification=True))


def test_production_review_requires_retrieval_and_attribution_check():
    ep = example_real_episode()
    ep["author_attribution_checked"] = False
    candidate = copy.deepcopy(DATA["candidates"][0])
    candidate.update(person_handle="exampleauthor", episode_ids=[ep["episode_id"]])
    assert any("attribution" in msg for msg in verify_candidate(candidate, [ep], require_verified_qualification=True))


def test_production_review_accepts_valid_shape_only_with_explicit_caveat():
    ep = example_real_episode()
    candidate = copy.deepcopy(DATA["candidates"][0])
    candidate.update(person_handle="exampleauthor", episode_ids=[ep["episode_id"]])
    assert verify_candidate(candidate, [ep], require_verified_qualification=True) == []
    # This only checks the consistency of a manually supplied receipt. It does not
    # prove the linked X post exists; that requires independently opening it.


def test_episode_rejects_mismatched_url_author():
    ep = example_real_episode()
    ep["author_handle"] = "someoneelse"
    assert any("author" in msg for msg in verify_episode(ep))
