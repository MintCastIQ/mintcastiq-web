from django.db import models
from django.utils import timezone   
from .soft_delete_mixin import SoftDeleteMixin
from .base_identity import BaseIdentity

class DimUsers(SoftDeleteMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=False)
    role = models.CharField(max_length=255, blank=True, null=True)

    join_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'dim_users'
