from mintcastiq.checklists import load_config

def test_load_config(tmp_path):
    yaml_content = """
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
    DemoChecklist:
      meta:
        sport: Football
        year: 2025
        brand: Demo
        set_name: DemoSet
        source_file: demo.xlsx
        last_modified: 2025-12-01T00:00:00Z
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
      column_sets:
        with_subset:
          0: subset_name
          1: card_number
          2: player_name
          3: team_name
          4: print_run
      sheets:
        0: {name: Base}
    """
    path = tmp_path / "config.yaml"
    path.write_text(yaml_content)

    cfg = load_config(str(path))
    assert "DemoChecklist" in cfg
    assert cfg["DemoChecklist"]["meta"]["brand"] == "Demo"
