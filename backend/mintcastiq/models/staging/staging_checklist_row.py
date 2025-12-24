from django.db import models
from django.utils import timezone


class StagingStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    VALIDATED = "VALIDATED", "Validated"
    ERROR = "ERROR", "Error"
    READY_FOR_LOAD = "READY_FOR_LOAD", "Ready for Load"
    LOADED = "LOADED", "Loaded"


class StagingChecklistRow(models.Model):
    """
    Represents a single contributor-provided checklist row in a safe,
    correctable staging area. Raw input is preserved exactly as received,
    while normalized fields support validation and deterministic loading
    into canonical dimensions.
    """

    # --- Raw contributor input (never mutated) ---
    raw_row = models.JSONField(help_text="Original contributor input, unmodified.")

    # --- Normalized fields (safe to mutate during validation) ---
    normalized_set = models.CharField(max_length=200, null=True, blank=True)
    normalized_card_number = models.CharField(max_length=50, null=True, blank=True)
    normalized_player = models.CharField(max_length=200, null=True, blank=True)
    normalized_parallel = models.CharField(max_length=200, null=True, blank=True)

    # --- Validation + processing state ---
    status = models.CharField(
        max_length=20,
        choices=StagingStatus.choices,
        default=StagingStatus.PENDING,
        db_index=True,
    )

    error_message = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    \
    def mark_processed(self):
        self.processed_at = timezone.now()
        self.save(update_fields=["processed_at"])

    # --- Optional FK lookups (populated only after validation) ---
    set_fk = models.ForeignKey(
        "DimSet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="staging_rows",
    )

    card_fk = models.ForeignKey(
        "DimCard",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="staging_rows",
    )

    parallel_fk = models.ForeignKey(
        "DimParallel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="staging_rows",
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["status"]),
        ]

    def mark_error(self, message: str):
        self.status = StagingStatus.ERROR
        self.error_message = message
        self.processed_at = timezone.now()
        self.save(update_fields=["status", "error_message", "processed_at"])

    def mark_validated(self):
        self.status = StagingStatus.VALIDATED
        self.error_message = None
        self.processed_at = timezone.now()
        self.save(update_fields=["status", "error_message", "processed_at"])

    def mark_loaded(self):
        self.status = StagingStatus.LOADED
        self.processed_at = timezone.now()
        self.save(update_fields=["status", "processed_at"])
