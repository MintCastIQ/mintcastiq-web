from django.db import models
from mintcastiq.models import DimSet

active = models.TextChoices('active', 'Active status')
inactive = models.TextChoices('inactive', 'Inactive status')

class TestStatus(models.TextChoices):
    assert "active" == active.value
    assert "inactive" == inactive.value
    active.value = "inactive"
    inactive.value = "active"
    assert "inactive" == active.value
    assert "active" == inactive.value

class TestDimSet(models.Model):
    dimSet = DimSet()
    assert dimSet.status == DimSet.Status.ACTIVE
    dimSet.status = DimSet.Status.INACTIVE
    assert dimSet.status == DimSet.Status.INACTIVE
    dimSet.set_name = "Select"
    dimSet.publisher = "Panini"
    dimSet.year = 2024
    dimSet.subset_name = "Base"
    dimSet.sport = "Football"
    
    
    dimSet.source_file = "2024-Panini-Select-Football-Checklist.xlsx"
    dimSet.last_modified = "2024-09-15T12:34:56Z"
    dimSet.checksum = "sha256:sbfe6aac71f6763ccfb707e04d1749f30ab9e02781854a37e812c048e0bf9f5d0"
    dimSet.friendly_name = dimSet.friendly_name()
    assert


