class StagedPlayerTeam(models.Model):
    player = models.ForeignKey(FactPlayerMaster, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(FactTeamMaster, null=True, on_delete=models.SET_NULL)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
