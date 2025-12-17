from django.test import TestCase
from mintcastiq.models import DimSet


class TestFriendlyName(TestCase):

    def setUp(self):
        self.dim = DimSet.create(
            set_name="Select",
            publisher="Panini",
            set_year="2024",
            subset_name="Base",
            sport="Football",
            set_code="2024-Panini-Select-Football-Base",
        )

    def test_friendly_name_format(self):
        expected = "2024 Panini Select Base"
        self.assertEqual(self.dim.friendly_name, expected)

    def test_friendly_name_throws_error_on_identity_change(self):
        self.dim.set_name = "Updated Select"
        with self.assertRaises(ValueError):
            self.dim.save()

    def test_friendly_name_does_not_update_on_lifecycle_change(self):
        original_friendly_name = self.dim.friendly_name
        self.dim.status = "INACTIVE"
        self.dim.save()
        self.assertEqual(self.dim.friendly_name, original_friendly_name)

    def test_friendly_name_is_deterministic(self):
        friendly_name_1 = self.dim.friendly_name
        friendly_name_2 = self.dim.friendly_name
        self.assertEqual(friendly_name_1, friendly_name_2)
