from django.db import models
from .soft_delete_mixin import SoftDeleteMixin
from .fact_inventory import FactInventory
from .fact_player_master import FactPlayerMaster
from .fact_team_master import FactTeamMaster
from .dim_grade import DimGrade
from .base_identity import BaseIdentity

class FactInventoryDetail(SoftDeleteMixin):
    detail_id = models.AutoField(primary_key=True)

    # Strict, non-nullable FKs
    inventory = models.ForeignKey(FactInventory, on_delete=models.PROTECT, null=False)
    player_master = models.ForeignKey(FactPlayerMaster, on_delete=models.PROTECT, null=False)
    team_master = models.ForeignKey(FactTeamMaster, on_delete=models.PROTECT, null=False)
    grade = models.ForeignKey(DimGrade, on_delete=models.PROTECT, null=False)

    quantity = models.IntegerField()
    acquired_at = models.DateTimeField()
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    identity_string = models.CharField(max_length=255, db_index=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    upc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'fact_inventory_detail'
