import pytest
from mintcastiq.models import DimCard, DimCardHash, DimSet
from domain.ingest.scanner import hash_run
from domain.ingest.checklists import validate_config

@pytest.mark.django_db
def test_hash_run_inserts_all_hashes():
    # Create a minimal set + card
    cardset = DimSet.objects.create(set_code="TEST")
    card = DimCard.objects.create(
        name="Test Card",
        team_name="Test Team",
        card_number="123",
        cardset=cardset
    )

    # Fake 10 positional hashes
    hash_values = {
        "TOP_LEFT": "aaa",
        "TOP_RIGHT": "bbb",
        "MID_LEFT": "ccc",
        "MID_RIGHT": "ddd",
        "BOTTOM_LEFT": "eee",
        "BOTTOM_RIGHT": "fff",
        "EDGE_TOP": "ggg",
        "EDGE_BOTTOM": "hhh",
        "EDGE_LEFT": "iii",
        "EDGE_RIGHT": "jjj",
    }

    run_id = hash_run(card, hash_values)

    # Assert: all 10 hashes inserted
    rows = DimCardHash.objects.filter(card=card, hash_run=run_id)
    assert rows.count() == 10

    # Assert: values stored correctly
    stored = {row.hash_position: row.hash_value for row in rows}
    for pos, val in hash_values.items():
        assert stored[pos] == val.strip()

def test_validate_config_passes_for_valid_structure():
    config = {
        "Example-Checklist": {
            "meta": {
                "columns": {
                    "cards": {0: "card_number", 1: "player_name"}
                }
            },
            "column_sets": {
                "default": {0: "card_number", 1: "player_name"}
            },
            "sheets": {
                0: {"name": "Base", "columns": "default"}
            }
        }
    }

    assert validate_config(config) is True


def test_validate_config_detects_invalid_alias():
    config = {
        "Example-Checklist": {
            "meta": {},
            "column_sets": {},
            "sheets": {
                0: {"name": "Base", "columns": "does_not_exist"}
            }
        }
    }

    assert validate_config(config) is False
