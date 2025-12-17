# utils.py
from django.db import models
from collections import defaultdict


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


def build_summary_index(cards_dict):
    """
    Build a multi-level summary index from the cards dict.

    Args:
        cards_dict (dict): Composite-keyed cards dictionary.

    Returns:
        dict: Nested summary structure grouped by subset, then parallel, then team.

    Example:
        summary = build_summary_index(myDict)

        for subset, keys in summary.items():
            print(f"{subset}: {len(keys)} myDict")
            for k in keys:
                print("  -", k)
    """
    summary = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for key, card in cards_dict.items():
        subset = card["set"]["subset_name"]
        parallel = card.get("parallel", "Base")
        team = card.get("team", "Unknown")

        summary[subset][parallel][team].append(key)

    return summary