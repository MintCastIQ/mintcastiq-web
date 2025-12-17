from django.db import models
from mintcastiq.models.base_identity import BaseIdentity
from mintcastiq.models.soft_delete_mixin import SoftDeleteMixin   


class DimSet(SoftDeleteMixin, BaseIdentity):
    """
    Canonical dimension representing a sports card set.
    This is intentionally denormalized for fast lookups and stable identity.
    """

    # -----------------------------
    # Denormalized identity fields
    # -----------------------------
    set_name = models.CharField(max_length=128)
    publisher = models.CharField(max_length=64)
    set_year = models.CharField(max_length=32)  # e.g. "2023-24", "2024 Update"
    subset_name = models.CharField(max_length=128, blank=True, null=True)
    sport = models.CharField(max_length=32, blank=True, null=True)

    # Optional but highly recommended for analytics + contributor clarity
    set_code = models.CharField(max_length=128, unique=True)

    # -----------------------------
    # Identity + friendly name
    # -----------------------------
    identity_fields = (
        "set_name",
        "publisher",
        "set_year",
        "subset_name",
        "sport",
    )

    friendly_name_template = (
        "{set_year} {publisher} {set_name} {subset_name}"
    )

    # -----------------------------
    # Canonicalization
    # -----------------------------
    def canonicalize(self):
        """
        Normalize fields for deterministic identity:
        - Trim whitespace
        - Normalize hyphens in set_year
        - Collapse double spaces
        - Ensure subset formatting is consistent
        """
        for field in (
            "set_name",
            "publisher",
            "set_year",
            "subset_name",
            "sport",
        ):
            value = getattr(self, field, None)
            if isinstance(value, str):
                cleaned = " ".join(value.strip().split())
                setattr(self, field, cleaned)

        # Normalize set_year hyphens: "2023 - 24" → "2023-24"
        if self.set_year:
            self.set_year = (
                self.set_year.replace(" ", "")
                .replace("–", "-")
            )

        return self

    # -----------------------------
    # Friendly name helpers
    # -----------------------------
    @property
    def subset_suffix(self):
        if self.subset_name:
            return f" ({self.subset_name})"
        return ""

