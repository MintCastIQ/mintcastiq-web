from django.test import TestCase
from mintcastiq.models import DimSet


class TestIdentityFields(TestCase):

    def setUp(self):
        self.dim = DimSet.create(
            set_name="Select",
            publisher="Panini",
            set_year="2024",
            subset_name="Base",
            sport="Football",
        )

    def test_identity_fields_exist(self):
        for field in self.dim.identity_fields:
            self.assertTrue(
                hasattr(self.dim, field),
                f"DimSet is missing identity field: {field}",
            )

    def test_identity_fields_are_used_in_hashing(self):
        identity_string = self.dim.identity_string
        for field in self.dim.identity_fields:
            value = getattr(self.dim, field)
            self.assertIn(
                f"{field}={value}",
                identity_string,
                f"Identity string missing field {field} with value {value}",
            )

    def test_missing_identity_field_raises_error(self):
        self.dim.sport = None
        with self.assertRaises(ValueError):
            self.dim.identity_string()

    def test_extra_identity_fields_raise_error(self):
        # Add a non-existent identity field
        self.dim.identity_fields = self.dim.identity_fields + ("non_existent_field",)
        with self.assertRaises(ValueError):
            self.dim.identity_string()