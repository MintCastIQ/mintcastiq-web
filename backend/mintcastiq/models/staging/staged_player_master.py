from django.db import models
from mintcastiq.models.dim_card import DimCard
from mintcastiq.models.dim_parallel import DimParallel

class StagedPlayerMaster(models.Model):
    raw_full_name = models.CharField(max_length=128, null=True)
    raw_player_name = models.CharField(max_length=64, null=True)

    card = models.ForeignKey(DimCard, null=True, on_delete=models.SET_NULL)
    parallel = models.ForeignKey(DimParallel, null=True, on_delete=models.SET_NULL)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
