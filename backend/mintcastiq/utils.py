# utils.py
from django.db import models
from app.models import DimCardHash

def next_hash_run(card):
    """
    Calculate the next hash_run for a given card.
    Ensures audit-grade consistency: each scan batch increments once,
    regardless of the 10 positional hashes inserted.
    """
    last_run = DimCardHash.objects.filter(card=card).aggregate(
        models.Max("hash_run")
    )["hash_run__max"] or 0
    return last_run + 1
