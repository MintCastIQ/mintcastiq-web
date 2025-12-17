from django.db import models
from django.utils import timezone
from .dim_card import DimCard
from .dim_users import DimUsers
from .dim_set import DimSet
from .dim_grade import DimGrade
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity

class FactCardEvents(SoftDeleteMixin):
    event_id = models.AutoField(primary_key=True)

    card = models.ForeignKey(DimCard, on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(DimUsers, on_delete=models.PROTECT, null=False)
    set = models.ForeignKey(DimSet, on_delete=models.PROTECT, null=False)
    grade = models.ForeignKey(DimGrade, on_delete=models.PROTECT, null=False)

    timestamp = models.DateTimeField(default=timezone.now)
    action_type = models.CharField(max_length=255)
    confidence_score = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    processing_time_ms = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "fact_card_events"

