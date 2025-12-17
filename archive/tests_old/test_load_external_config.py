def test_load_external_config():
    from mintcastiq import checklists

    # Ensure the repository's external YAML config can be loaded
    cfg = checklists.load_config(checklists.CONFIG_FILE)

    # Basic sanity checks
    assert "defaults" in cfg
    assert "2024-Panini-Select-Football-Checklist" in cfg
    assert "2024-Panini-Illusions-Football-Checklist" in cfg
