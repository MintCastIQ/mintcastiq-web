from django.db import models
from domain.enums import Status

class ActiveManager(models.Manager):
    """Custom manager that only returns active records."""
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.ACTIVE)