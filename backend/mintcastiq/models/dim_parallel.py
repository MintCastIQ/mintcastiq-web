from django.db import models
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity
from .dim_set import DimSet

class DimParallel(SoftDeleteMixin, BaseIdentity):
    parallel_name = models.CharField(max_length=50)

    identity_fields = (
        "parallel_name",
    )

    class Meta:
        db_table = "dim_parallel"
        constraints = [
            models.UniqueConstraint(
                fields=["parallel_name"],
                name="uq_parallel_name",
            )
        ]

    def __str__(self):
        return self.parallel_name

