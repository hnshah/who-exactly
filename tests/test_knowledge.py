"""Knowledge retrieval must be scoped, curated, and testable offline."""
from pathlib import Path
from datetime import date
import pytest

from who_exactly.knowledge import select_knowledge, validate_note, load_note


def note(directory: Path, slug: str, *, status="reviewed", scope="shared", project="", tags="remote-gui,qualification", evidence="method", reviewer="maintainer", last_verified="2026-10-10", source=""):
    directory.mkdir(parents=True, exist_ok=True)
    lines = [
        "---", f"id: {slug}", f"scope: {scope}", f"project_id: {project or 'null'}",
        "visibility: public" if scope == "shared" else "visibility: private",
        f"status: {status}", f"kind: {evidence}",
        f"tags: [{tags}]", "as_of: '2026-10-01'", f"last_verified: '{last_verified}'",
        f"reviewed_by: [{reviewer}]" if reviewer else "reviewed_by: []",
        f"source_urls: [{source}]" if source else "source_urls: []",
        "applies_when: 'research about this particular situation'",
        "does_not_apply_when: 'unrelated jobs'", "---", "# Lesson", "This is a synthetic test note.",
    ]
    p = directory / f"{slug}.md"
    p.write_text("\n".join(lines) + "\n")
    return p


def test_retrieves_reviewed_relevant_notes_not_drafts(tmp_path):
    shared = tmp_path / "shared"
    note(shared, "good", tags="remote-gui,qualification")
    note(shared, "draft", status="draft", tags="remote-gui,qualification", reviewer="")
    note(shared, "unrelated", tags="ecommerce,merchants")
    found = select_knowledge(shared, tags=["remote-gui"], as_of=date(2026,10,27))
    assert [n.metadata["id"] for n in found] == ["good"]


def test_project_context_never_leaks_across_projects(tmp_path):
    shared = tmp_path / "shared"
    private = tmp_path / "private"
    note(shared, "general", tags="remote-gui,qualification")
    note(private, "beam-only", scope="project", project="beam", tags="remote-gui,qualification")
    beam = select_knowledge(shared, tags=["remote-gui"], project_dir=private, project_id="beam", as_of=date(2026,10,27))
    other = select_knowledge(shared, tags=["remote-gui"], project_dir=private, project_id="other-product", as_of=date(2026,10,27))
    assert "beam-only" in [n.metadata["id"] for n in beam]
    assert "beam-only" not in [n.metadata["id"] for n in other]


def test_stale_finding_not_loaded_as_current_fact(tmp_path):
    shared = tmp_path / "shared"
    note(shared, "old", evidence="finding", tags="remote-gui", last_verified="2025-03-01",source="https://example.org/evidence")
    assert not select_knowledge(shared, tags=["remote-gui"], as_of=date(2026,10,27))


def test_previously_approved_method_still_available(tmp_path):
    shared=tmp_path/"shared"
    note(shared,"method",evidence="method",tags="remote-gui",last_verified="2025-03-01")
    assert len(select_knowledge(shared,tags=["remote-gui"],as_of=date(2026,10,27))) == 1


def test_unreviewed_note_cannot_self_promote(tmp_path):
    path=note(tmp_path,"unreviewed",reviewer="")
    assert any("review" in e for e in validate_note(load_note(path)))


def test_public_research_finding_requires_source(tmp_path):
    path=note(tmp_path,"finding",evidence="finding",source="")
    assert any("source" in e for e in validate_note(load_note(path)))


def test_private_data_in_public_dir_is_rejected(tmp_path):
    shared=tmp_path/"public"
    note(shared,"private",scope="project",project="beam")
    with pytest.raises(ValueError,match="private|scope"):
        select_knowledge(shared,tags=["remote-gui"],as_of=date(2026,10,27))


def test_only_max_three_context_notes_are_loaded(tmp_path):
    shared=tmp_path/"shared"
    for x in range(6): note(shared,f"rule{x}",tags="remote-gui")
    result=select_knowledge(shared,tags=["remote-gui"],as_of=date(2026,10,27))
    assert len(result)==3


def test_never_read_symlinked_knowledge(tmp_path):
    shared=tmp_path/"shared"; external=tmp_path/"secret.md"
    note(tmp_path,"secret",scope="project",project="beam")
    (tmp_path/"secret.md").write_text("sensitive")
    shared.mkdir(); (shared/"evil.md").symlink_to(external)
    with pytest.raises(ValueError,match="symlink"):
        select_knowledge(shared,tags=["remote-gui"],as_of=date(2026,10,27))
