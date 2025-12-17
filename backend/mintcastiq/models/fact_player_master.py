from django.db import models
from .dim_card import DimCard
from .dim_parallel import DimParallel
from .base_identity import BaseIdentity
from .soft_delete_mixin import SoftDeleteMixin

class FactPlayerMaster(SoftDeleteMixin):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=128)
    player_name = models.CharField(max_length=64)

    card = models.ForeignKey(DimCard, on_delete=models.PROTECT, null=False)
    parallel = models.ForeignKey(DimParallel, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'fact_player_master'
