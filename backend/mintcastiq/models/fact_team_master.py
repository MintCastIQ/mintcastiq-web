from django.db import models
from .dim_card import DimCard
from .dim_parallel import DimParallel
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity

class FactTeamMaster(SoftDeleteMixin):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=128)
    team_name = models.CharField(max_length=64)

    card = models.ForeignKey(DimCard, on_delete=models.PROTECT, null=False)
    parallel = models.ForeignKey(DimParallel, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'fact_team_master'

