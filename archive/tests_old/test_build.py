import pytest
from mintcastiq.checklists import build, classify_row
from test_ingest_checklist import ws_fixture, cfg_fixture

def test_build(ws_fixture, cfg_fixture):
    ws = ws_fixture
    cfg = cfg_fixture
    meta = cfg["2024-Panini-Select-Football-Checklist"]["meta"]
    assert meta["year"] == 2024
    assert meta["brand"] == "Panini"
    assert meta["set_name"] == "Select"
    assert meta["sport"] == "Football"
    assert meta["source_file"] == "2024-Panini-Select-Football-Checklist.xlsx"

    assert ws.Title == "Inserts"
    assert len(ws['A']) == 10  # 10 rows
    rows = list(ws.values)
    is_parallel = False
    col_map = {0: "subset_name", 1: "card_number", 2: "player_name", 3: "team_name"}
    meta = {"year": 2024, "brand": "Panini", "set_name": "Select"}

    for i in range(len(rows)):
        row = rows[i - 1]
        if i == 0:
            assert i == 0
        mode, vals = classify_row(row, is_parallel)
        if mode == "card":
            artifact = build(vals, col_map, meta)

            key = "2024-Panini-Select-Rookies-12"
            assert key in artifact
            # artifact values are objects with to_dict()
            obj = artifact[key]
            data = obj.to_dict() if hasattr(obj, "to_dict") else obj
            assert data["player_name"] == "John Doe"
            assert data["team_name"] == "Yankees"
            # No cardset attached when building in isolation
            assert "cardset" not in data
            # Metadata fields are merged at top-level
            assert data["year"] == 2024
            assert data["brand"] == "Panini"
            assert data["set_name"] == "Select"
            assert data["subset_name"] == "Rookies"
            assert data["card_number"] == "12"
            break
    

    