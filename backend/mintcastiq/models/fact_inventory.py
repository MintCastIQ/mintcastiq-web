from django.db import models
from .dim_users import DimUsers
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity

class FactInventory(SoftDeleteMixin):
    inventory_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(DimUsers, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        db_table = 'fact_inventory'
