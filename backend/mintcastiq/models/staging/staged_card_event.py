class StagedCardEvent(models.Model):
    card = models.ForeignKey(DimCard, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(DimUsers, null=True, on_delete=models.SET_NULL)
    set = models.ForeignKey(DimSet, null=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey(DimGrade, null=True, on_delete=models.SET_NULL)

    raw_action_type = models.CharField(max_length=255, null=True)
    raw_timestamp = models.DateTimeField(null=True)
    raw_confidence_score = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    raw_processing_time_ms = models.IntegerField(null=True)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
