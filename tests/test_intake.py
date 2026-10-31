import pytest
from app.core import Intake, SAMPLE


def test_duplicate_human_review_and_archive(tmp_path):
    s = Intake("sqlite:///" + str(tmp_path / "i.sqlite"))
    a = s.receive(SAMPLE)
    assert s.receive(SAMPLE)["id"] == a["id"]
    with pytest.raises(PermissionError):
        s.approve(a["id"], a["fingerprint"], "reviewer")
    s.approve(a["id"], a["fingerprint"], "reviewer", True)
    s.approve(a["id"], a["fingerprint"], "reviewer", True)
    assert len(s.archive()) == 1


def test_bad_total_never_archived(tmp_path):
    s = Intake("sqlite:///" + str(tmp_path / "i.sqlite"))
    a = s.receive(dict(SAMPLE, total_cents=10))
    with pytest.raises(ValueError):
        s.approve(a["id"], a["fingerprint"], "reviewer", True)
    assert not s.archive()
