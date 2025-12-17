class StagedTeamMaster(models.Model):
    raw_full_name = models.CharField(max_length=128, null=True)
    raw_team_name = models.CharField(max_length=64, null=True)

    card = models.ForeignKey(DimCard, null=True, on_delete=models.SET_NULL)
    parallel = models.ForeignKey(DimParallel, null=True, on_delete=models.SET_NULL)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
