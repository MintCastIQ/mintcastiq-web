from django.db import models
from enum import Enum
from .managers.active_manager import ActiveManager
from domain.enums import Status

class SoftDeleteMixin(models.Model):
    """
    Mixin that adds a status field and soft delete behavior.
    Ensures rows are never physically deleted, only marked inactive.
    """
    status = models.CharField(
        max_length=16,
        default=Status.ACTIVE.value,
        db_index=True
    )
    objects = models.Manager()   # default manager (all records)
    active = ActiveManager()     # filtered manager (only active records)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.status = Status.INACTIVE
        self.save(update_fields=["status"])

    def restore(self):
        self.status = Status.ACTIVE
        self.save(update_fields=["status"])

    def delete(self, *args, **kwargs):
        self.soft_delete()