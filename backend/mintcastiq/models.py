from django.db import models
from django.utils import timezone


# -----------------------------
# Shared Enums & Mixins
# -----------------------------

class Status(models.TextChoices):
    ACTIVE = 'a', 'active'
    INACTIVE = 'i', 'inactive'

class ActiveManager(models.Manager):
    """Custom manager that only returns active records."""
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.ACTIVE)


class SoftDeleteMixin(models.Model):
    """
    Mixin that adds a status field and soft delete behavior.
    Ensures rows are never physically deleted, only marked inactive.
    """
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.ACTIVE,
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


# -----------------------------
# Dimension Tables
# -----------------------------

class DimSet(SoftDeleteMixin):
    """Represents a production set/subset combination."""
    set_id = models.AutoField(primary_key=True)
    set_name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    set_year = models.CharField(max_length=10, blank=True, null=True)
    subset_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'dim_set'
        constraints = [
            models.UniqueConstraint(
                fields=['set_name', 'subset_name', 'publisher', 'set_year'],
                name='unique_set_subset'
            )
        ]

class DimParallel(SoftDeleteMixin):
    parallel_id = models.AutoField(primary_key=True)
    parallel_name = models.CharField(max_length=255)
    print_run = models.IntegerField(blank=True, null=True)
    set = models.ForeignKey(DimSet, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'dim_parallel'
        constraints = [
            models.UniqueConstraint(
                fields=['set', 'parallel_name'],
                name='unique_set_parallel'
            )
        ]

class DimCard(SoftDeleteMixin):
    card_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    card_number = models.CharField(max_length=25, blank=True, null=True)
    parallel = models.ForeignKey(DimParallel, on_delete=models.CASCADE, blank=True, null=True)
    set = models.ForeignKey(DimSet, on_delete=models.CASCADE, blank=True, null=True)
    identity_string = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    stock_image_path = models.CharField(max_length=255, blank=True, null=True)
    stock_image_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'dim_card'
        constraints = [
            models.UniqueConstraint(
                fields=['identity_string'],
                name='unique_card_identity'
            )
        ]

    def save(self, *args, **kwargs):
        parts = [
            str(self.set.set_year).strip() if self.set and self.set.set_year else "",
            str(self.set.publisher).strip() if self.set and self.set.publisher else "",
            str(self.set.set_name).strip() if self.set and self.set.set_name else "",
            str(self.set.subset_name).strip() if self.set and self.set.subset_name else "",
            str(self.card_number).strip() if self.card_number else "",
            str(self.parallel.parallel_name).strip() if self.parallel and self.parallel.parallel_name else "",
            str(self.name).strip() if self.name else "",
        ]
        self.identity_string = " ".join([p for p in parts if p])
        super().save(*args, **kwargs)

class DimGrade(SoftDeleteMixin):
    grade_id = models.AutoField(primary_key=True)
    grading_standard = models.CharField(max_length=50, db_index=True, default='RAW')
    numeric_value = models.DecimalField(max_digits=10, decimal_places=1)
    grade_label = models.CharField(max_length=255)
    overlay_ref = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'dim_grade'
        constraints = [
            models.UniqueConstraint(
                fields=['grading_standard', 'numeric_value', 'grade_label'],
                name='unique_grade'
            )
        ]

class DimUsers(SoftDeleteMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    otp_delivery = models.CharField(max_length=10, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=False)
    invited = models.BooleanField(default=False)
    join_date = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'dim_users'

class DimSessions(SoftDeleteMixin):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(DimUsers, on_delete=models.CASCADE, blank=True, null=True)
    session_token = models.CharField(unique=True, max_length=255)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'dim_sessions'

# -----------------------------
# Fact Tables
# -----------------------------
class FactCardEvents(SoftDeleteMixin):
    event_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(DimCard, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(DimUsers, on_delete=models.CASCADE, blank=True, null=True)
    set = models.ForeignKey(DimSet, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(DimGrade, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    action_type = models.CharField(max_length=255)
    confidence_score = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    processing_time_ms = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'fact_card_events'

class FactInventory(SoftDeleteMixin):
    inventory_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(DimUsers, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        db_table = 'fact_inventory'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class FactInventoryDetail(SoftDeleteMixin):
    detail_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(FactInventory, on_delete=models.DO_NOTHING, blank=True, null=True)
    card = models.ForeignKey(DimCard, on_delete=models.DO_NOTHING, blank=True, null=True)
    grade = models.ForeignKey(DimGrade, on_delete=models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True )
    acquired_at = models.DateTimeField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    identity_string = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    upc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'fact_inventory_detail'
        constraints = [
            models.UniqueConstraint(
                fields=['identity_string'],
                name='unique_inventory_detail'
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.inventory:
            self.inventory.save()
        if self.card:
            self.identity_string = self.card.identity_string
        super().save(*args, **kwargs)
