# mintcastiq/models/staging/staged_parallel.py

from django.db import models
from ..dim_set import DimSet

class StagedParallel(models.Model):
    card_set = models.ForeignKey(DimSet, null=True, on_delete=models.SET_NULL)
    raw_parallel_name = models.CharField(max_length=64, null=True)
    raw_print_run = models.PositiveBigIntegerField(null=True)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

