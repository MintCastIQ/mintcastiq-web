from django.test import TestCase
from mintcastiq.models import DimSet
from domain.enums import Status

class ClosenessTestMixin:
    """
    Reusable tests for BaseIdentityModel.closeness() and closeness_with_diff().
    Subclasses must define:
        - model_class
        - base_kwargs (identity fields)
    """

    def create_instance(self, **overrides):
        data = {**self.base_kwargs, **overrides}
        return self.model_class.create(**data)

    def test_closeness_identical(self):
        a = self.create_instance()
        b = self.create_instance()
        self.assertEqual(a.closeness(b), 1.0)

    def test_closeness_one_field_differs(self):
        a = self.create_instance()
        b = self.create_instance(subset_name="Different")
        score = a.closeness(b)

        # 1 field differs out of len(identity_fields)
        expected = (len(a.identity_fields) - 1) / len(a.identity_fields)
        self.assertEqual(score, expected)

    def test_closeness_completely_different(self):
        a = self.create_instance()
        b = self.create_instance(
            set_name="X",
            publisher="Y",
            set_year="Z",
            subset_name="Q",
            print_run=999,
            type="Other"
        )
        self.assertEqual(a.closeness(b), 0.0)

    def test_closeness_with_diff(self):
        a = self.create_instance()
        b = self.create_instance(subset_name="Different")

        score, diff = a.closeness_with_diff(b)

        # Score should reflect 1 mismatch
        expected = (len(a.identity_fields) - 1) / len(a.identity_fields)
        self.assertEqual(score, expected)

        # Diff should contain exactly the mismatched field
        self.assertIn("subset_name", diff)
        self.assertEqual(diff["subset_name"]["self"], a.subset_name)
        self.assertEqual(diff["subset_name"]["other"], b.subset_name)

    def test_closeness_wrong_type(self):
        a = self.create_instance()
        self.assertEqual(a.closeness("not a model"), 0.0)
        score, diff = a.closeness_with_diff("not a model")
        self.assertEqual(score, 0.0)
        self.assertEqual(diff, {})


class TestDimSet(TestCase):

    def setUp(self):
        self.dim_set = DimSet.create(
            set_name="Select",
            publisher="Panini",
            set_year="2024",
            subset_name="Base",
        )

    # -----------------------------
    # Basic instantiation
    # -----------------------------
    def test_instantiation(self):
        self.assertIsNotNone(self.dim_set)

    # -----------------------------
    # Field initialization + friendly_name + checksum
    # -----------------------------
    def test_model_fields(self):
        self.assertEqual(self.dim_set.set_name, "Select")
        self.assertEqual(self.dim_set.publisher, "Panini")
        self.assertEqual(self.dim_set.set_year, "2024")
        self.assertEqual(self.dim_set.subset_name, "Base")
        self.assertEqual(self.dim_set.friendly_name, "2024-Panini-Select-Base")

        # Checksum created on save()
        self.assertIsNotNone(self.dim_set.checksum)
        self.assertEqual(len(self.dim_set.checksum), 64)

        # Lifecycle field initialized
        self.assertEqual(self.dim_set.status, Status.ACTIVE.value)

    # -----------------------------
    # Identity change → rehash
    # -----------------------------
    def test_save_rehashes_on_identity_change(self):
        original = self.dim_set.checksum
        self.dim_set.set_name = "Illusions"
        self.dim_set.save(update_fields=["set_name"])
        self.assertNotEqual(self.dim_set.checksum, original)

    # -----------------------------
    # Lifecycle change → NO rehash
    # -----------------------------
    def test_save_does_not_rehash_on_lifecycle_change(self):
        original = self.dim_set.checksum
        self.dim_set.status = Status.INACTIVE
        self.dim_set.save(update_fields=["status"])
        self.assertEqual(self.dim_set.checksum, original)

    # -----------------------------
    # Friendly name is computed, not persisted
    # -----------------------------
    def test_friendly_name_computes_correctly(self):
        self.assertEqual(self.dim_set.friendly_name, "2024-Panini-Select-Base")
        self.dim_set.subset_name = "Premium"
        self.assertEqual(self.dim_set.friendly_name, "2024-Panini-Select-Premium")

    # -----------------------------
    # Full save with no changes → NO rehash
    # -----------------------------
    def test_save_does_not_rehash_when_no_fields_change(self):
        original = self.dim_set.checksum
        self.dim_set.save()
        self.assertEqual(self.dim_set.checksum, original)

    # -----------------------------
    # Deterministic hashing
    # -----------------------------
    def test_checksum_is_deterministic(self):
        original = self.dim_set.checksum

        # No identity change → stable
        self.dim_set.save()
        self.assertEqual(self.dim_set.checksum, original)

        # Identity change → new checksum
        self.dim_set.set_year = "2025"
        self.dim_set.save()
        self.assertNotEqual(self.dim_set.checksum, original)
        self.assertEqual(len(self.dim_set.checksum), 64)

    # -----------------------------
    # Closeness tests
    # -----------------------------
    from django.test import TestCase
from mintcastiq.models import DimSet
from .mixins import ClosenessTestMixin  # wherever you store it


class TestDimSetCloseness(ClosenessTestMixin, TestCase):
    model_class = DimSet
    base_kwargs = {
        "set_name": "Select",
        "publisher": "Panini",
        "set_year": "2024",
        "subset_name": "Base",
        "print_run": 1000,
        "type": "Hobby",
    }

