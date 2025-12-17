class StagedInventory(models.Model):
    user = models.ForeignKey(DimUsers, null=True, on_delete=models.SET_NULL)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
