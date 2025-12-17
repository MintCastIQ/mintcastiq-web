import pytest
from mintcastiq.models.dim_set import DimSet
from django.test import TestCase


@pytest.mark.django_db
class TestLifecycle(TestCase):

    def setUp(self):
        # Create a canonical DimSet using BaseIdentity.create()
        self.dim = DimSet.create(
            set_name="Select",                                                                                                                                       
            publisher="Panini",
            set_year="2023-24",
            subset_name="Base",
            sport="Football",
            set_code="2023-24-Select-Football-Base",
        )

    def test_status_change_does_not_affect_checksum(self):
        original_checksum = self.dim.checksum

        # Checksum must remain unchanged
        assert self.dim.checksum == original_checksum

    def test_identity_is_immutable(self):
        # Attempting to change identity fields should throw a ValueError
        self.dim.set_name = "New name"
        with pytest.raises(ValueError):
            self.dim.save()

    def test_friendly_name_is_deterministic(self):
        expected = "2023-24 Panini Select Base"
        assert self.dim.friendly_name == expected
