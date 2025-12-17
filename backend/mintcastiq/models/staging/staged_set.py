from django.db import models


class StagedSet(models.Model):
    """
    Raw ingest representation of a card set.
    This model is intentionally permissive and denormalized.
    Promotion services are responsible for validation and normalization.
    """

    # Raw ingest fields (may contain whitespace, inconsistent casing, etc.)
    set_name = models.CharField(max_length=128, blank=True, null=True)
    publisher = models.CharField(max_length=64, blank=True, null=True)
    set_year = models.CharField(max_length=32, blank=True, null=True)
    subset_name = models.CharField(max_length=128, blank=True, null=True)
    brand = models.CharField(max_length=64, blank=True, null=True)
    sport = models.CharField(max_length=32, blank=True, null=True)

    # Optional contributor-provided natural key
    set_code = models.CharField(max_length=128, blank=True, null=True)

    # Metadata for auditability
    source_file = models.CharField(max_length=256, blank=True, null=True)
    ingest_session_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Staged Set"
        verbose_name_plural = "Staged Sets"

    def __str__(self):
        return f"StagedSet({self.set_name}, {self.set_year}, {self.publisher})"
