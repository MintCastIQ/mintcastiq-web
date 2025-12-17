from django.db import models
from .soft_delete_mixin import SoftDeleteMixin  
from .base_identity import BaseIdentity

class DimGrade(SoftDeleteMixin, BaseIdentity):
    grade_id = models.AutoField(primary_key=True)
    grading_standard = models.CharField(max_length=50, db_index=True, default="RAW")
    numeric_value = models.DecimalField(max_digits=10, decimal_places=1)
    grade_label = models.CharField(max_length=255)
    overlay_ref = models.CharField(max_length=100, blank=True, null=True)

    # -----------------------------
    # Identity fields (immutable)
    # -----------------------------
    identity_fields = (
        "grading_standard",
        "numeric_value",
        "grade_label",
    )

    class Meta:
        db_table = "dim_grade"
        constraints = [
            models.UniqueConstraint(
                fields=["grading_standard", "numeric_value", "grade_label"],
                name="unique_grade",
            )
        ]
