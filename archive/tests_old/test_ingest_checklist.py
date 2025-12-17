import pytest
import openpyxl
from mintcastiq.checklists import ingest_checklist
import yaml

@pytest.fixture
def ws_fixture():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inserts"
    ws.append(["Rookies", None, None, None, None, None])  # subset
    ws.append([None, None, None, None, None, None])  # blank
    ws.append(["Parallels", None, None, None, None, None])  # parallel marker
    ws.append([None, None, None, None, None, None])  # blank
    ws.append(["Gold Foil", None, None, None, None, None])  # parallel
    ws.append(["Black Prizm", None, None, None, None, None])  # parallel
    ws.append([None, None, None, None, None, None])  # blank
    ws.append(["1", "Tory Taylor", "Chicago Bears", None, None, None])  # card
    ws.append(["Alter Ego", "15", "Marvin Harrison Jr", "Arizona Cardinals", "/", "500"])  # teams
    ws.append(["2025 XRC Black Prizm", "501", "Cam Ward", "Tennessee Titans", 1, None])  # master
    return ws

@pytest.fixture
def cfg_fixture():
    return 
"""
defaults:
  columns:
    cards:
      0: card_number
      1: player_name
      2: team_name
      3: print_run
    subset:
      0: subset_name
    parallel:
      0: parallel_name

2024-Panini-Select-Football-Checklist:
  meta:
    sport: Football
    year: 2024
    brand: Panini
    set_name: Select
    source_file: 2024-Panini-Select-Football-Checklist.xlsx
    last_modified: "2024-09-15T12:34:56Z"
    columns:
      cards:
        0: card_number
        1: player_name
        2: team_name
        3: print_run
      subset:
        0: subset_name
      parallel:
        0: parallel_name
    checksum: "sha256:sbfe6aac71f6763ccfb707e04d1749f30ab9e02781854a37e812c048e0bf9f5d0"
  column_sets:
    with_subset_skip4:
      0: subset_name
      1: card_number
      2: player_name
      3: team_name
      5: print_run
    with_subset:
      0: subset_name
      1: card_number
      2: player_name
      3: team_name
      4: print_run
  sheets:
    0:
      name: Base
    1:
      name: Autographs
    2:
      name: Memorabilia
    3:
      name: Inserts
    4:
      name: XRC Redemptions
    5:
      name: Teams
      columns: with_subset_skip4
      intentional_gaps:
        - 4
    6:
      name: Master Checklist
      columns: with_subset
        """

def test_ingest_pipeline_end_to_end(ws_fixture, cfg_fixture):
    cfg = yaml.safe_load(cfg_fixture)

    result = ingest_checklist(ws_fixture, "file.xlsx", "Sheet1", cfg)

    assert "cards" in result
    assert "parallels" in result
    assert any("cardset" in v for v in result["cards"].values())
    assert any("cardset" in v for v in result["parallels"].values())


