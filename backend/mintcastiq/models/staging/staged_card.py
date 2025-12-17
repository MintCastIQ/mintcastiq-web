class StagedCard(models.Model):
    # Nullable FKs
    cardset = models.ForeignKey(DimSet, null=True, on_delete=models.SET_NULL)
    parallel = models.ForeignKey(DimParallel, null=True, on_delete=models.SET_NULL)

    # Raw ingest fields
    raw_name = models.CharField(max_length=64, null=True)
    raw_team_name = models.CharField(max_length=64, null=True)
    raw_card_number = models.CharField(max_length=25, null=True)
    raw_parallel_name = models.CharField(max_length=64, null=True)
    raw_set_name = models.CharField(max_length=64, null=True)

    # Optional: ingest metadata
    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
