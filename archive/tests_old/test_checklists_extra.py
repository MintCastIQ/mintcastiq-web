import os
import openpyxl
import pytest

from mintcastiq import checklists


def test_safe_get_bounds_and_none():
    row = [None, 'A', 'B']
    assert checklists.safe_get(row, 0) == ""
    assert checklists.safe_get(row, 1) == 'A'
    assert checklists.safe_get(row, 2) == 'B'
    assert checklists.safe_get(row, 3) == ""


def test_resolve_columns_priority():
    # column_sets alias should win when provided as a string
    sheet_def = {"columns": "alias_set"}
    column_sets = {"alias_set": {0: "x", 1: "y"}}
    meta = {"columns": {"cards": {0: "a"}}}
    defaults = {"columns": {"cards": {0: "d"}}}
    resolved = checklists.resolve_columns(sheet_def, column_sets, meta, defaults, row_type="cards")
    assert resolved == column_sets["alias_set"]

    # explicit dict on sheet_def should win over meta
    sheet_def = {"columns": {0: "explicit"}}
    resolved2 = checklists.resolve_columns(sheet_def, column_sets, meta, defaults, row_type="cards")
    assert resolved2 == {0: "explicit"}

    # fallback to meta
    sheet_def = {}
    resolved3 = checklists.resolve_columns(sheet_def, column_sets, meta, defaults, row_type="cards")
    assert resolved3 == meta["columns"]["cards"]


def test_validate_config_unknown_alias_and_gap_conflict(tmp_path, caplog):
    # Build a config where a sheet references an unknown alias and declares a gap that conflicts
    cfg = {
        "Demo": {
            "meta": {"columns": {"cards": {0: "card_number"}}},
            "column_sets": {},
            "sheets": {
                0: {"name": "S", "columns": "missing_alias", "intentional_gaps": [0]}
            },
        }
    }

    caplog.set_level("ERROR")
    ok = checklists.validate_config(cfg)
    assert ok is False
    # Expect an error about unknown alias
    assert any("Unknown column alias" in r.message for r in caplog.records)


def test_load_config_fails_on_invalid(tmp_path):
    bad = tmp_path / "bad.yaml"
    # missing expected structures (no defaults or sheets)
    bad.write_text("not: a valid config for checklists")
    with pytest.raises(RuntimeError):
        checklists.load_config(str(bad))


def test_ingest_workbook_missing_key_returns_empty():
    wb = openpyxl.Workbook()
    wb.active.title = "Sheet1"
    # provide an all_cfg that does not include the filename key
    result = checklists.ingest_workbook(wb, "missing.xlsx", all_cfg={})
    assert result == {"cards": {}, "parallels": {}}


def test_ingest_checklist_card_and_parallel_assignment():
    # Build a worksheet with subset, marker, parallel, card, master
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["Rookies", None, None])
    ws.append(["Parallel Inserts", None, None])
    ws.append(["Gold Foil", None, None])
    ws.append(["Rookies", "12", "John Doe", "Yankees"])
    ws.append(["Rookies", "13", "Jane Smith", "Cowboys", "500"])

    cfg = {
        "meta": {"year": 2025, "brand": "Demo", "set_name": "DemoSet"},
        "sheets": {0: {"name": "Sheet1"}},
        "column_sets": {},
        "defaults": {"columns": {"subset": {0: "subset_name"}, "parallel": {0: "parallel_name"}, "cards": {0: "subset_name", 1: "card_number", 2: "player_name", 3: "team_name", 4: "print_run"}}}
    }

    result = checklists.ingest_checklist(ws, "file.xlsx", "Sheet1", cfg)
    assert "cards" in result and "parallels" in result
    assert any(v.get("cardset") is not None for v in result["cards"].values())
    assert any(v.get("cardset") is not None for v in result["parallels"].values())
