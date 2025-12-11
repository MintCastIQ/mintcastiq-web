import json
from mintcastiq.models import DimSet, DimCard, DimParallel

def ingest_checklist(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for row in data.get("checklist", []):
        set_obj, _ = DimSet.objects.get_or_create(
            set_name=row["set"],
            subset_name=row["subset"]
        )
        DimCard.objects.get_or_create(
            set=set_obj,
            card_number=row["cardNumber"],
            name=row["player"],
            team_name=row["team"],
        )

    for row in data.get("parallels", []):
        set_obj, _ = DimSet.objects.get_or_create(
            set_name=row["set"],
            subset_name=row["subset"]
        )
        DimParallel.objects.get_or_create(
            set=set_obj,
            parallel_name=row["parallel"],
            print_run=normalize_print_run(row.get("printRun")),
        )

def normalize_print_run(value: str) -> int | None:
    """
    Normalize print_run strings like '1/1', '25/50', '199/199' into integers.
    - For '1/1', return 1
    - For '25/50', return 50 (denominator)
    - For '199/199', return 199
    """
    if not value:
        return None

    # Ensure it's a string
    val = str(value).strip()

    # Skip datetime-like strings
    if "-" in val and ":" in val:
        return None

    if "/" in val:
        parts = val.split("/")
        # Special case: 1/1 → return 1
        if val == "1/1":
            return 1
        # Otherwise take denominator (the total print run)
        return int(parts[-1])
    else:
        return int(val)

