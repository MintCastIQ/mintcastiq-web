import pytest

from domain.ingest.checklists import validate_config
from mintcastiq.models.staging.staged_set import StagedSet
from domain.services.set_promotion import DimSetPromotionService


@pytest.mark.django_db
class TestChecklistIngest:

    def test_valid_config_passes(self):
        config = {
            "Example-Checklist": {
                "meta": {
                    "columns": {
                        "sets": {
                            0: "set_name",
                            1: "publisher",
                            2: "set_year",
                            3: "subset_name",
                        }
                    }
                },
                "column_sets": {
                    "default": {
                        0: "set_name",
                        1: "publisher",
                        2: "set_year",
                        3: "subset_name",
                    }
                },
                "sheets": {
                    0: {"name": "Base", "columns": "default"}
                }
            }
        }

        assert validate_config(config) is True

    def test_invalid_config_fails(self):
        config = {
            "Example-Checklist": {
                "meta": {},
                "column_sets": {},
                "sheets": {
                    0: {"name": "Base", "columns": "missing_alias"}
                }
            }
        }

        assert validate_config(config) is False

    def test_staging_and_promotion_flow(self):
        pass
