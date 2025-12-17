from django.db import models
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity

CARD_PARALLEL_IDENTITY_FIELDS = (
    "card",
    "parallel",
)

class DimCardParallel(SoftDeleteMixin, BaseIdentity):
    card = models.ForeignKey(
        "DimCard",
        on_delete=models.PROTECT,
        related_name="card_parallels",
    )
    parallel = models.ForeignKey(
        "DimParallel",
        on_delete=models.PROTECT,
        related_name="parallel_cards",
    )

    identity_fields = CARD_PARALLEL_IDENTITY_FIELDS

    class Meta:
        db_table = "dim_card_parallel"
        constraints = [
            models.UniqueConstraint(
                fields=CARD_PARALLEL_IDENTITY_FIELDS,
                name="uq_card_parallel_pair",
            )
        ]

    def __str__(self):
        return f"{self.card_id} :: {self.parallel_id}"
