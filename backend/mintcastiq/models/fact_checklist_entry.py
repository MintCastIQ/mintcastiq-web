from django.db import models

class FactChecklistEntry(models.Model):
    """
    A fact table entry representing a single validated checklist row
    that has been loaded into canonical dimensions. Immutable and fully
    audit‑grade: stores raw contributor data and full provenance.
    """

    card_parallel = models.ForeignKey(
        "mintcastiq.DimCardParallel",
        on_delete=models.PROTECT,
        related_name="checklist_entries",
    )

    # Provenance
    source_file = models.CharField(max_length=255)
    source_sheet = models.CharField(max_length=255, null=True, blank=True)
    source_row = models.IntegerField()

    # Immutable raw contributor data
    raw_data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "fact_checklist_entry"
        verbose_name = "Checklist Entry"
        verbose_name_plural = "Checklist Entries"

    def __str__(self):
        return f"{self.card_parallel} @ row {self.source_row}"
