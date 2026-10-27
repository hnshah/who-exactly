import json
from pathlib import Path
from copy import deepcopy

from who_exactly.records import canonical_post_url, post_id, dedupe_episodes, verify_episode, verify_candidate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / 'fixtures/remote-mac-synthetic.json').read_text())


def test_canonical_public_x():
    assert canonical_post_url('https://x.com/SomeUser/status/123456?s=20') == 'https://x.com/someuser/status/123456'


def test_canonical_twitter():
    assert canonical_post_url('https://twitter.com/ExampleAuthor/status/987') == 'https://x.com/exampleauthor/status/987'


def test_rejects_profile_only_url():
    assert canonical_post_url('https://x.com/example') is None


def test_rejects_disguised_domain():
    assert canonical_post_url('https://x.com.evil.test/user/status/123') is None


def test_post_id():
    assert post_id('https://x.com/u/status/12345') == '12345'


def test_fixtures_never_count_as_live():
    assert all(not verify_episode(x) for x in FIXTURE['episodes'])
    assert all(x['source_kind'] == 'fixture' for x in FIXTURE['episodes'])


def test_prevents_fixture_claimed_as_real():
    bad = deepcopy(FIXTURE['episodes'][0])
    bad['source_kind'] = 'public_x'
    bad['retrieval_status'] = 'retrieved'
    assert verify_episode(bad)


def test_unverified_real_post_never_passes_live_gate():
    record = deepcopy(FIXTURE['episodes'][0])
    record.update(source_kind='public_x', retrieval_status='unverified', source_url='https://x.com/someone/status/123456', evidence_type='firsthand_report')
    assert any('not been retrieved' in e for e in verify_episode(record))


def test_valid_syntax_is_not_remote_truth():
    record = deepcopy(FIXTURE['episodes'][0])
    record.update(source_kind='public_x', retrieval_status='retrieved', source_url='https://x.com/someone/status/123456', author_handle='someone', evidence_type='firsthand_report', retrieved_at='2026-10-05T12:00:00Z')
    assert not verify_episode(record)  # proves shape ONLY; never that a tweet was opened


def test_candidate_ids_exist():
    for c in FIXTURE['candidates']:
        assert not verify_candidate(c, FIXTURE['episodes'])


def test_broken_candidate_source_reference():
    c = deepcopy(FIXTURE['candidates'][0])
    c['episode_ids'] = ['no-such-episode']
    assert verify_candidate(c, FIXTURE['episodes'])


def test_included_without_receipt_is_rejected():
    c = deepcopy(FIXTURE['candidates'][0])
    c['episode_ids'] = []
    assert verify_candidate(c, FIXTURE['episodes'])


def test_dedupe_shared_post_id():
    a = {**FIXTURE['episodes'][0], 'source_url': 'https://twitter.com/user/status/555'}
    b = {**FIXTURE['episodes'][1], 'source_url': 'https://x.com/user/status/555'}
    assert len(dedupe_episodes([a, b])) == 1


def test_dedupe_distinct_fixture_ids():
    assert len(dedupe_episodes(FIXTURE['episodes'])) == 3


def test_future_source_date_invalid():
    record = deepcopy(FIXTURE['episodes'][0])
    record.update(source_kind='public_x',retrieval_status='retrieved',source_url='https://x.com/u/status/123',evidence_type='firsthand_report',retrieved_at='2026-09-30T12:00:00Z')
    assert any('later than' in e for e in verify_episode(record))
