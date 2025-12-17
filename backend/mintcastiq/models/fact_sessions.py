from django.db import models
from django.utils import timezone   
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity
from .dim_users import DimUsers

class FactSessions(SoftDeleteMixin):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(DimUsers, on_delete=models.PROTECT, null=False)
    session_token = models.CharField(unique=True, max_length=255)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'fact_sessions'