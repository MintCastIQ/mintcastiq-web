# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DimCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    name = models.TextField()
    edition = models.TextField(blank=True, null=True)
    format = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    parallel = models.ForeignKey('DimParallel', models.DO_NOTHING, blank=True, null=True)
    set = models.ForeignKey('DimSet', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_card'


class DimCardHash(models.Model):
    hash_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(DimCard, models.DO_NOTHING)
    hash_value = models.TextField()
    hash_type = models.TextField()
    hash_position = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_card_hash'


class DimContributor(models.Model):
    contributor_id = models.AutoField(primary_key=True)
    username = models.TextField(unique=True)
    role = models.TextField(blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_contributor'


class DimGrade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    grading_standard = models.TextField()
    numeric_value = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    grade_label = models.TextField()
    overlay_ref = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_grade'


class DimParallel(models.Model):
    parallel_id = models.AutoField(primary_key=True)
    parallel_name = models.TextField()
    parallel_type = models.TextField(blank=True, null=True)
    print_run = models.IntegerField(blank=True, null=True)
    set = models.ForeignKey('DimSet', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_parallel'


class DimSessions(models.Model):
    user = models.ForeignKey('DimUsers', models.DO_NOTHING)
    session_token = models.CharField(unique=True, max_length=255)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_sessions'


class DimSet(models.Model):
    set_id = models.AutoField(primary_key=True)
    set_name = models.TextField()
    publisher = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    set_year = models.CharField(max_length=10, blank=True, null=True)
    ssubset_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_set'


class DimUsers(models.Model):
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    otp_delivery = models.CharField(max_length=10, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)
    is_contributor = models.BooleanField(blank=True, null=True)
    invited = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_users'


class FactCardEvents(models.Model):
    event_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(DimCard, models.DO_NOTHING)
    contributor = models.ForeignKey(DimContributor, models.DO_NOTHING)
    set = models.ForeignKey(DimSet, models.DO_NOTHING)
    grade = models.ForeignKey(DimGrade, models.DO_NOTHING, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    action_type = models.TextField()
    confidence_score = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    processing_time_ms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_card_events'


class FactInventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    contributor = models.ForeignKey(DimContributor, models.DO_NOTHING)
    card = models.ForeignKey(DimCard, models.DO_NOTHING)
    set = models.ForeignKey(DimSet, models.DO_NOTHING)
    grade = models.ForeignKey(DimGrade, models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    acquired_at = models.DateTimeField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_inventory'


class FactMetrics(models.Model):
    metric_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(FactCardEvents, models.DO_NOTHING)
    metric_name = models.TextField()
    metric_value = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    unit = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_metrics'
