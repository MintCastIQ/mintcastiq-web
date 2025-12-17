from .base_identity import BaseIdentity
from django.db import models
from .soft_delete_mixin import SoftDeleteMixin

PARALLEL_SET_IDENTITY_FIELDS = (
    "parallel",
    "card_set",
)

class DimParallelSet(SoftDeleteMixin, BaseIdentity):
    parallel = models.ForeignKey(
        "DimParallel",
        on_delete=models.PROTECT,
        related_name="parallel_sets",
    )
    card_set = models.ForeignKey(
        "DimSet",
        on_delete=models.PROTECT,
        related_name="set_parallels",
    )

    identity_fields = PARALLEL_SET_IDENTITY_FIELDS

    class Meta:
        db_table = "dim_parallel_set"
        constraints = [
            models.UniqueConstraint(
                fields=PARALLEL_SET_IDENTITY_FIELDS,
                name="uq_parallel_set_pair",
            )
        ]

    def __str__(self):
        return f"{self.parallel_id} @ {self.card_set_id}"

