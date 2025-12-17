from django.test import TestCase
from mintcastiq.models import DimSet
from domain.hashing import hash_object


class TestIdentityHashing(TestCase):

    def setUp(self):
        self.dim = DimSet.create(
            set_name="Select",
            publisher="Panini",
            set_year="2024",
            subset_name="Base",
            sport="Football",
            set_code="2024-Panini-Select-Football-Base",
        )

    def test_hash_is_64_chars(self):
        self.assertEqual(len(self.dim.checksum), 64)

    def test_hash_changes_when_identity_field_changes(self):
        original_hash = self.dim.checksum
        self.dim.subset_name = "Updated Base"
        self.dim._compute_checksum()
        self.assertNotEqual(self.dim.checksum, original_hash)

    def test_hash_does_not_change_when_lifecycle_field_changes(self):
        original_hash = self.dim.checksum
        self.dim.status = "INACTIVE"
        self.dim._compute_checksum()
        self.assertEqual(self.dim.checksum, original_hash)

    def test_hash_does_not_change_when_friendly_name_changes(self):
        original_hash = self.dim.checksum
        self.dim.friendly_name_template = "{set_year} {publisher} {set_name} {subset_name}"
        self.dim._compute_checksum()
        self.assertEqual(self.dim.checksum, original_hash)

    def test_hash_is_deterministic(self):
        hash1 = self.dim.checksum
        self.dim._compute_checksum()
        hash2 = self.dim.checksum
        self.assertEqual(hash1, hash2)

    def test_hash_ignores_non_identity_fields(self):
        original_hash = self.dim.checksum
        # Change a non-identity field
        self.dim.status = "INACTIVE"
        self.assertEqual(self.dim.checksum, original_hash)
