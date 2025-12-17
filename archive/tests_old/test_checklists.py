import pytest
from mintcastiq.checklists import classify_row, ingest_checklist
from tests.test_ingest_checklist import ws_fixture, cfg_fixture

def test_classify_row(ws_fixture, cfg_fixture):
    row = ws_fixture[0]
    mode, vals = classify_row(row, False)
    assert mode == "subset"
    assert vals == {"subset_name": "Rookies"}
    row = ws_fixture[1]
    

def test_parallel_marker_classification():
    row = ["Parallel Inserts", None, None]
    mode, vals = classify_row(row, False)
    assert mode == "parallel_marker"
    assert "parallel" in vals["parallel_name"].lower()

def test_card_classification():
    row = ["Rookies", "12", "John Doe", "Yankees"]
    mode, vals = classify_row(row, False)
    assert mode == "card"
    assert vals["card_number"] == "12"

def test_master_classification():
    row = ["Rookies", "12", "John Doe", "Yankees", "500"]
    mode, vals = classify_row(row, False)
    assert mode == "master"
    assert vals["print_run"] == "500"

def test_ingest_pipeline_end_to_end(ws_fixture, cfg_fixture):
    result = ingest_checklist(ws_fixture, "file.xlsx", "Sheet1", cfg_fixture)
    assert "cards" in result
    assert "parallels" in result
    assert all("cardset" in v for v in result["cards"].values())
