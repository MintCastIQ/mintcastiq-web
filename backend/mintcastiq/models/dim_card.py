from django.db import models
from .dim_set import DimSet
from .soft_delete_mixin import SoftDeleteMixin  
from .base_identity import BaseIdentity



"""
DimCard model represents a card entity with various attributes and relationships.
It includes fields for card details, foreign key relationships to DimSet and DimParallel,
and methods for generating a friendly name and saving the model with an identity string.
"""
class DimCard(SoftDeleteMixin, BaseIdentity):
    card_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    team_name = models.CharField(max_length=64)
    card_number = models.CharField(max_length=25)

    cardset = models.ForeignKey(
        DimSet,
        on_delete=models.PROTECT,
        null=False,
        related_name="cards",
    )

    stock_image_path = models.CharField(max_length=255, blank=True, null=True)
    stock_image_name = models.CharField(max_length=255, blank=True, null=True)

    # -----------------------------
    # Identity fields (immutable)
    # -----------------------------
    identity_fields = (
        "cardset",
        "card_number",
    )

    class Meta:
        db_table = "dim_card"
        constraints = [
            models.UniqueConstraint(
                fields=["cardset", "card_number"],
                name="unique_card_identity",
            )
        ]

    # -----------------------------
    # Friendly name
    # -----------------------------
    @property
    def friendly_name(self):
        parts = [
            self.cardset.friendly_name if self.cardset else "",
            self.card_number or "",
            self.name or "",
        ]
        return " - ".join(filter(None, parts))
