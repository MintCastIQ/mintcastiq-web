from django.db import models
from django.utils import timezone   
from .soft_delete_mixin import SoftDeleteMixin
from .dim_users import DimUsers

class FactUsersOTP(SoftDeleteMixin):
    otp_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(DimUsers, on_delete=models.PROTECT, null=False)

    otp_hash = models.CharField(max_length=128, null=False)
    delivery_method = models.CharField(max_length=20)  # sms, email, etc.

    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "fact_user_otp"
