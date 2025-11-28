from django.db import models
from django.utils import timezone


# -----------------------------
# Shared Enums & Mixins
# -----------------------------

class Status(models.TextChoices):
    ACTIVE = 'a', 'active'
    INACTIVE = 'i', 'inactive'


class HashPosition(models.TextChoices):
    FULL_CARD = "full_card", "Full Card"
    NE = "NE", "Northeast"
    N = "N", "North"
    NW = "NW", "Northwest"
    W = "W", "West"
    SW = "SW", "Southwest"
    S = "S", "South"
    SE = "SE", "Southeast"
    E = "E", "East"
    CENTER = "Center", "Center"


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
    parallel_type = models.CharField(max_length=255, blank=True, null=True)
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
    release_year = models.IntegerField(blank=True, null=True)
    parallel = models.ForeignKey(DimParallel, on_delete=models.CASCADE, blank=True, null=True)
    set = models.ForeignKey(DimSet, on_delete=models.CASCADE, blank=True, null=True)
    identity_string = models.CharField(max_length=255, blank=True, null=True, db_index=True)

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
            str(self.release_year).strip() if self.release_year else "",
            str(self.set.set_name).strip() if self.set and self.set.set_name else "",
            str(self.parallel.parallel_name).strip() if self.parallel and self.parallel.parallel_name else "",
            str(self.set.subset_name).strip() if self.set and self.set.subset_name else "",
            str(self.card_number).strip() if self.card_number else "",
            str(self.name).strip() if self.name else "",
        ]
        self.identity_string = " ".join([p for p in parts if p])
        super().save(*args, **kwargs)


class DimCardHash(SoftDeleteMixin):
    hash_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(DimCard, on_delete=models.CASCADE, blank=True, null=True)
    hash_value = models.CharField(max_length=64, db_index=True)
    hash_type = models.CharField(max_length=50)
    hash_run = models.PositiveIntegerField(default=1)
    hash_position = models.CharField(
        max_length=20,
        choices=HashPosition.choices,
        db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'dim_card_hash'
        constraints = [
            models.UniqueConstraint(
                fields=["card", "hash_run", "hash_position"],
                name="unique_card_run_position"
            )
        ]


class DimCardParallel(models.Model):
    set = models.ForeignKey(DimSet, on_delete=models.CASCADE)
    parallel = models.ForeignKey(DimParallel, on_delete=models.CASCADE)
    hash_run = models.PositiveIntegerField()


class DimGrade(SoftDeleteMixin):
    grade_id = models.AutoField(primary_key=True)
    grading_company = models.CharField(max_length=50, default='RAW')
    numeric_value = models.DecimalField(max_digits=10, decimal_places=1)
    grade_label = models.CharField(max_length=255)

    class Meta:
        db_table = 'dim_grade'
        constraints = [
            models.UniqueConstraint(
                fields=['grading_company', 'numeric_value'],
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

class FactChecklistItem(SoftDeleteMixin):
    checklist_item_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(DimCard, on_delete=models.CASCADE)
    set = models.ForeignKey(DimSet, on_delete=models.CASCADE)
    parallel = models.ForeignKey(DimParallel, on_delete=models.CASCADE)
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    identity_string = models.CharField(max_length=255, db_index=True, blank=True, null=True)

    class Meta:
        db_table = 'fact_checklist_item'
        constraints = [
            models.UniqueConstraint(
                fields=['identity_string'],
                name='unique_checklist_identity'
            )
        ]

    def save(self, *args, **kwargs):
        if self.card:
            self.identity_string = self.card.identity_string
        super().save(*args, **kwargs)


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
    card = models.ForeignKey(DimCard, on_delete=models.DO_NOTHING, blank=True, null=True)
    checklist_item = models.ForeignKey(FactChecklistItem, on_delete=models.DO_NOTHING, blank=True, null=True)
    grade = models.ForeignKey(DimGrade, on_delete=models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    acquired_at = models.DateTimeField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    identity_string = models.CharField(max_length=255, db_index=True, blank=True, null=True)

    class Meta:
        db_table = 'fact_inventory'
        constraints = [
            models.UniqueConstraint(
                fields=['identity_string'],
                name='unique_inventory'
            )
        ]

    def save(self, *args, **kwargs):
        if self.card:
            self.identity_string = self.card.identity_string
        super().save(*args, **kwargs)

