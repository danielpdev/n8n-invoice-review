import json
from pathlib import Path


def test_export_has_no_credentials_and_all_connections_resolve():
    w = json.loads(Path("workflows/main.json").read_text())
    names = {n["name"] for n in w["nodes"]}
    assert len(names) == len(w["nodes"])
    assert w["active"] is False
    for node in w["nodes"]:
        assert not node.get("credentials")
        if node["type"].endswith("httpRequest"):
            assert node["parameters"]["url"].startswith("http://mock:8000/")
    for source, outputs in w["connections"].items():
        assert source in names
        for branch in outputs["main"]:
            for target in branch:
                assert target["node"] in names
