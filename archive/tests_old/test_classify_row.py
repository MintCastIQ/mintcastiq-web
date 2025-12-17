import pytest
from mintcastiq.checklists import classify_row

def test_subset_row():
    row = ["Rookies", None, None]
    mode, vals = classify_row(row, is_parallel=False)
    assert mode == "subset"
    assert vals["subset_name"] == "Rookies"

def test_parallel_marker():
    row = ["Parallel Inserts", None, None]
    mode, vals = classify_row(row, is_parallel=False)
    assert mode == "parallel_marker"
    assert "parallel" in vals["parallel_name"].lower()

def test_parallel_row_in_mode():
    row = ["Gold Foil", None, None]
    mode, vals = classify_row(row, is_parallel=True)
    assert mode == "parallel"
    assert vals["parallel_name"] == "Gold Foil"

def test_card_row():
    row = ["Rookies", "12", "John Doe", "Yankees"]
    mode, vals = classify_row(row, is_parallel=False)
    assert mode == "card"
    assert vals["card_number"] == "12"

def test_master_row():
    row = ["Rookies", "12", "John Doe", "Yankees", "500"]
    mode, vals = classify_row(row, is_parallel=False)
    assert mode == "master"
    assert vals["print_run"] == "500"
