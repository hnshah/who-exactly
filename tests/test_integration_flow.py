"""Synthetic end-to-end demonstration of *context selection*, not native Grok execution."""
from copy import deepcopy
from datetime import date
from pathlib import Path
import json
import subprocess
import sys

from who_exactly.knowledge import load_note, select_knowledge
from who_exactly.records import verify_episode, verify_candidate

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=json.loads((ROOT/'fixtures/remote-mac-synthetic.json').read_text())


def make_private_note(folder, state='draft'):
    folder.mkdir(parents=True,exist_ok=True)
    p=folder/'beam-ssh-is-not-a-gui-job.md'
    p.write_text('\n'.join([
        '---',
        'id: beam-ssh-is-not-a-gui-job','scope: project','project_id: beam',
        'visibility: private',f'status: {state}','kind: qualification',
        'tags: [remote-gui, qualification, ssh]','as_of: "2026-10-27"',
        'last_verified: null','reviewed_by: [fixture-reviewer]' if state=='reviewed' else 'reviewed_by: []',
        'source_urls: []',"applies_when: 'Beam GUI job'", "does_not_apply_when: 'terminal-only jobs'",
        '---','# Draft hypothetical',
        'SSH-only users without GUI needs are not qualified for this particular job.',
    ])+'\n')
    return p


def test_private_correction_requires_review_and_survives_new_research_call(tmp_path):
    shared=tmp_path/'shared'; shared.mkdir()
    private=tmp_path/'beam'; p=make_private_note(private,'draft')
    assert select_knowledge(shared,tags=['remote-gui'],project_dir=private,project_id='beam',as_of=date(2026,10,27)) == []
    p=make_private_note(private,'reviewed')
    assert 'SSH-only' in select_knowledge(shared,tags=['remote-gui'],project_dir=private,project_id='beam',as_of=date(2026,10,27))[0].body
    # A separate call represents reloading files on the next research mission.
    again=select_knowledge(shared,tags=['remote-gui'],project_dir=private,project_id='beam',as_of=date(2026,10,27))
    assert again[0].metadata['id']=='beam-ssh-is-not-a-gui-job'
    assert not select_knowledge(shared,tags=['remote-gui'],project_dir=private,project_id='other-product',as_of=date(2026,10,27))
    assert p.exists()  # retrieve does not rewrite local notes or promote them


def test_fixture_cannot_be_recast_as_qualified_live_candidate():
    synthetic=deepcopy(FIXTURE)
    assert all(not verify_episode(x) for x in synthetic['episodes'])
    assert not verify_candidate(synthetic['candidates'][0],synthetic['episodes'])  # valid synthetic shape
    assert verify_candidate(synthetic['candidates'][0],synthetic['episodes'],require_verified_qualification=True)
    assert synthetic['candidates'][1]['category']=='rejected'
    assert synthetic['candidates'][2]['category']=='unknown'


def test_public_context_cli_excludes_draft_knowledge():
    proc=subprocess.run([sys.executable,str(ROOT/'scripts/knowledge_cli.py'),'select','--tags','qualification,firsthand-evidence'],text=True,capture_output=True,check=True)
    result=json.loads(proc.stdout)
    assert result['status']=='context_only_not_source_verification'
    assert result['notes']==[]
