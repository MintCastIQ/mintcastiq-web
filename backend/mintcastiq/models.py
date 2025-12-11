from django.db import models
from django.utils import timezone
import hashlib
from mintcastiq.serializers import serialize_for_hash
from domain.enums import Status, CardType

# -----------------------------
# Shared Enums & Mixins
# -----------------------------

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


def hash_object(instance) -> str:
    """
    Generate a stable hash string for a Django model instance.
    Uses the serialize_for_hash function to get a JSON representation.
    """
    json_str = serialize_for_hash(instance)
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()

# -----------------------------
# Dimension Tables
# -----------------------------

class DimSet(SoftDeleteMixin, models.Model):
    """Represents a production set/subset combination."""
    set_id = models.AutoField(primary_key=True)
    set_name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    set_year = models.CharField(max_length=10, blank=True, null=True)
    subset_name = models.CharField(max_length=255, blank=True, null=True)
    print_run = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    friendly_name = models.CharField(max_length=128, default="FIXME")
    checksum = models.CharField(max_length=64, default=friendly_name)     

    class Meta:
        db_table = 'dim_set'
        constraints = [
            models.UniqueConstraint(
                fields=["friendly_name"],
                name='unique_set'
            )
        ]
    
    def equals(self, other) -> bool:
        if not isinstance(other, DimSet):
            return False
        return (
            self.checksum == other.checksum
        )
    
    def save(self, *args, **kwargs):
        self.checksum = hash_object(self)
        self.friendly_name = f"{self.set_year}-{self.publisher}-{self.set_name}-{self.subset_name}"
        super().save(*args, **kwargs)

class DimParallel(SoftDeleteMixin, models.Model):
    parallel_id = models.AutoField(primary_key=True)
    parallel_name = models.CharField(max_length=64)
    print_run = models.PositiveBigIntegerField(blank=True, null=True)
    card_set = models.ForeignKey(DimSet, on_delete=models.DO_NOTHING, blank=True, null=True)
    

    class Meta:
        db_table = 'dim_parallel'
        constraints = [
            models.UniqueConstraint(
                fields=['parallel_name'],
                name='unique_parallel'
            )
        ]


class DimCard(SoftDeleteMixin, models.Model):
    card_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    team_name = models.CharField(max_length=64, blank=True, null=True)
    card_number = models.CharField(max_length=25, blank=True, null=True)
    cardset = models.ForeignKey(DimSet, on_delete=models.CASCADE, blank=True, null=True)
    identity_string = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    stock_image_path = models.CharField(max_length=255, blank=True, null=True)
    stock_image_name = models.CharField(max_length=255, blank=True, null=True)

    identity_fields = ['cardset.friendly_name', 'cardset.subset_name', 'card_number', 'parallel.parallel_name', 'name']

    class Meta:
        db_table = 'dim_card'
        constraints = [
            models.UniqueConstraint(
                fields=['identity_string'],
                name='unique_card_identity'
            )
        ]

    def json_eq(self, other) -> bool:
        if not isinstance(other, DimCard):
            return False
        return (
            self.cardset == other.cardset and
            self.card_number == other.card_number and
            self.name == other.name and
            self.team_name == other.team_name
        )
    
    def to_dict(self) -> dict:
        return {
            "card_id": self.card_id,
            "name": self.name,
            "team_name": self.team_name,
            "card_number": self.card_number,
            "parallel": self.parallel.to_dict() if self.parallel else None,
            "cardset": self.cardset.to_dict() if self.cardset else None,
            "identity_string": self.identity_string,
            "stock_image_path": self.stock_image_path,
            "stock_image_name": self.stock_image_name
        }
    
    def save(self, *args, **kwargs):
        self.identity_string = self.build_identity(self)
        super().save(*args, **kwargs)


class DimGrade(SoftDeleteMixin, models.Model):
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

class DimUsers(SoftDeleteMixin, models.Model):
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

class DimSessions(SoftDeleteMixin, models.Model):
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
class FactCardEvents(SoftDeleteMixin, models.Model):
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

class FactInventory(SoftDeleteMixin, models.Model):
    inventory_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(DimUsers, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        db_table = 'fact_inventory'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class FactPlayerMaster(SoftDeleteMixin, models.Model):
    hash_id = models.CharField(max_length=64, primary_key=True)
    full_name = models.CharField(max_length=128)
    card = models.ForeignKey(DimCard, on_delete=models.DO_NOTHING)
    parallel = models.ForeignKey(DimParallel, on_delete=models.DO_NOTHING)
    player_name = models.CharField(max_length=64)

    identity_fields = ['full_name', 'player_name']

    class Meta:
        db_table = 'fact_player_master'

    def save(self, *args, **kwargs):
        hash_id = self.build_identity()
        super().save(*args, **kwargs)

    
class FactTeamMaster(SoftDeleteMixin, models.Model):
    hash_id = models.CharField(max_length=64, primary_key=True)
    full_name = models.CharField(max_length=128)
    card = models.ForeignKey(DimCard, on_delete=models.DO_NOTHING)
    parallel = models.ForeignKey(DimParallel, on_delete=models.DO_NOTHING)
    team_name = models.CharField(max_length=64)

    identity_fields = ['full_name', 'team_name']

    class Meta:
        db_table = 'fact_team_master'

    def save(self, *args, **kwargs):
        hash_id = self.build_identity
        super().save(*args, **kwargs)


class BridgePlayerTeam(models.Model):
    """
    Relates FactPlayerMaster and FactTeamMaster rows by their hash_id.
    Provides a clean join path without circular FK dependencies.
    """

    id = models.AutoField(primary_key=True)
    player_master = models.ForeignKey(
        FactPlayerMaster,
        to_field="hash_id",
        on_delete=models.DO_NOTHING,
        db_index=True
    )
    team_master = models.ForeignKey(
        FactTeamMaster,
        to_field="hash_id",
        on_delete=models.DO_NOTHING,
        db_index=True
    )

    class Meta:
        db_table = "bridge_player_team"
        constraints = [
            models.UniqueConstraint(
                fields=["player_master", "team_master"],
                name="unique_player_team_bridge"
            )
        ]

class ChecklistUpload(models.Model):
    # fields here
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="checklists/")
    processed = models.BooleanField(default=False)

    class Meta:
        db_table = 'checklist_upload'

class FactInventoryDetail(SoftDeleteMixin, models.Model):
    detail_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(FactInventory, on_delete=models.DO_NOTHING, blank=True, null=True)
    player_master = models.ForeignKey(FactPlayerMaster, on_delete=models.DO_NOTHING, blank=True, null=True)
    team_master = models.ForeignKey(FactTeamMaster,on_delete=models.DO_NOTHING, blank=True, null=True)
    grade = models.ForeignKey(DimGrade, on_delete=models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True )
    acquired_at = models.DateTimeField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    identity_string = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    upc = models.CharField(max_length=255, blank=True, null=True)

    identity_fields = ['']

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
        if self.player_master:
            self.identity_string = self.card.identity_string
        super().save(*args, **kwargs)
