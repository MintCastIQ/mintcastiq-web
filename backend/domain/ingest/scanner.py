"""
scanner.py
----------
Handles card scan ingestion for MintCastIQ.

Responsibilities:
- Detect a scan event (triggered externally).
- Calculate all 10 positional hashes for the card image.
- Assign a single `hash_run` value for the batch.
- Insert all hashes atomically into `DimCardHash`.
"""

from django.db import transaction, models
from mintcastiq.models import DimCard, DimCardHash, HashPosition
from  domain.utils import next_hash_run  # utility function you moved earlier


def hash_run(card, hash_values):
    """
    Process a scan for a given card and insert all positional hashes.

    Args:
        card (DimCard): The card object being scanned.
        hash_values (dict): Mapping of HashPosition -> hash string.
            Example: {"TOP_LEFT": "abc123", "TOP_RIGHT": "def456", ...}

    Returns:
        int: The `hash_run` value assigned to this batch.
    """
    # Calculate next run once
    run_id = next_hash_run(card)

    # Ensure atomic insert of all 10 hashes
    with transaction.atomic():
        for pos, value in hash_values.items():
            DimCardHash.objects.create(
                card=card,
                hash_position=pos,
                hash_value=value.strip(),
                hash_run=run_id
            )

    return run_id
