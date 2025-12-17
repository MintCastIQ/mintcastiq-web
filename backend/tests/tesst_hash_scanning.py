import pytest

from mintcastiq.models import DimCard, DimCardHash, DimSet
from domain.ingest.scanner import hash_run
from domain.enums import HashPosition


@pytest.mark.django_db
class TestHashScanning:

    def setUp(self):
        # Minimal canonical set for FK
        self.set = DimSet.create(
            set_name="Select",
            publisher="Panini",
            set_year="2023-24",
            subset_name="Base",
            brand="Select",
            sport="Football",
            set_code="2023-24-Select-Football-Base",
        )

        # Minimal canonical card
        self.card = DimCard.create(
            card_number="123",
            player_name="Test Player",
            team_name="Test Team",
            set=self.set,
        )

    def test_hash_run_inserts_all_positions(self):
        # 10 positional hashes (messy on purpose)
        hash_values = {
            HashPosition.TOP_LEFT: "aaa ",
            HashPosition.TOP_RIGHT: " bbb",
            HashPosition.MID_LEFT: "ccc",
            HashPosition.MID_RIGHT: "ddd",
            HashPosition.BOTTOM_LEFT: "eee",
            HashPosition.BOTTOM_RIGHT: "fff",
            HashPosition.EDGE_TOP: "ggg",
            HashPosition.EDGE_BOTTOM: "hhh",
            HashPosition.EDGE_LEFT: "iii",
            HashPosition.EDGE_RIGHT: "jjj",
        }

        run_id = hash_run(self.card, hash_values)

        # All 10 hashes must be inserted
        rows = DimCardHash.objects.filter(card=self.card, hash_run=run_id)
        assert rows.count() == 10

        # Values must be stored trimmed and deterministic
        stored = {row.hash_position: row.hash_value for row in rows}
        for pos, val in hash_values.items():
            assert stored[pos] == val.strip()

    def test_hash_run_creates_unique_run_ids(self):
        # Two separate scans must produce two separate run IDs
        run1 = hash_run(self.card, {pos: f"val{idx}" for idx, pos in enumerate(HashPosition)})
        run2 = hash_run(self.card, {pos: f"val{idx+10}" for idx, pos in enumerate(HashPosition)})

        assert run1 != run2

        # Each run must have exactly 10 hashes
        assert DimCardHash.objects.filter(card=self.card, hash_run=run1).count() == 10
        assert DimCardHash.objects.filter(card=self.card, hash_run=run2).count() == 10
