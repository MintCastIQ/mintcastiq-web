class ChecklistNormalizationService:
    """
    Normalizes contributor-provided checklist rows into canonical,
    audit-safe values. This service never mutates raw input and
    writes all normalized fields back to the staging row.
    """

    def __init__(self, raw_row: dict):
        self.raw = raw_row  # or staging_row.raw if that's the field name 
        self.normalized = {}

        
    def run(self):
        try:
            self.normalized["set"] = self.normalize_set(self.raw.get("set_name"))
            self.normalized["card_number"] = self.normalize_card_number(self.raw.get("card_number"))
            self.normalized["player"] = self.normalize_player(self.raw.get("player_name"))
            self.normalized["parallel"] = self.normalize_parallel(self.raw.get("parallel"))

            return self.normalized

        except Exception as e:
            raise e
        
    # -----------------------------
    # Normalization helpers
    # -----------------------------

    def normalize_set(self, value):
        if not value:
            raise ValueError("Missing set name")

        cleaned = value.strip().title()

        # Example: "2025 topps baseball" → "2025 Topps Baseball"
        return cleaned

    def normalize_card_number(self, value):
        if not value:
            raise ValueError("Missing card number")

        cleaned = str(value).strip().upper()

        # Example: "  23a " → "23A"
        return cleaned

    def normalize_player(self, value):
        if not value:
            raise ValueError("Missing player name")

        cleaned = " ".join(value.split()).title()

        # Example: "mike trout" → "Mike Trout"
        return cleaned

    def normalize_parallel(self, value):
        if not value:
            return None  # parallels are optional

        cleaned = value.strip().title()

        # Example: "rainbow foil" → "Rainbow Foil"
        return cleaned
