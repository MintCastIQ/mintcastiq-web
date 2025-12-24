from django.db import models
from mintcastiq.models.fact_inventory import FactInventory
from mintcastiq.models.fact_player_master import FactPlayerMaster
from mintcastiq.models.fact_team_master import FactTeamMaster
from mintcastiq.models.dim_grade import DimGrade

class StagedInventoryDetail(models.Model):
    # Nullable FKs
    inventory = models.ForeignKey(FactInventory, null=True, on_delete=models.SET_NULL)
    player_master = models.ForeignKey(FactPlayerMaster, null=True, on_delete=models.SET_NULL)
    team_master = models.ForeignKey(FactTeamMaster, null=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey(DimGrade, null=True, on_delete=models.SET_NULL)

    # Raw ingest fields
    raw_quantity = models.IntegerField(null=True)
    raw_acquired_at = models.DateTimeField(null=True)
    raw_source = models.TextField(null=True)
    raw_notes = models.TextField(null=True)
    raw_upc = models.CharField(max_length=255, null=True)

    ingest_batch_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
