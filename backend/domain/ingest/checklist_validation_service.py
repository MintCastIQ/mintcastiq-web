class ChecklistValidationService:
    """
    Validates a normalized staging row.
    Ensures required fields are present and logically consistent.
    Writes validation errors back to the staging row.
    """

    REQUIRED_FIELDS = [
        "normalized_set",
        "normalized_card_number",
        "normalized_player",
    ]

    def __init__(self, staging_row):
        self.row = staging_row
        self.errors = []

    def run(self):
        self._check_required_fields()
        self._check_card_number()
        self._check_parallel()

        if self.errors:
            self.row.validation_errors = self.errors
            self.row.status = "ERROR"
        else:
            self.row.status = "VALIDATED"

        self.row.save()

    # ----------------------------------------
    # Validation checks
    # ----------------------------------------

    def _check_required_fields(self):
        for field in self.REQUIRED_FIELDS:
            if not getattr(self.row, field):
                self.errors.append(f"Missing required field: {field}")

    def _check_card_number(self):
        num = self.row.normalized_card_number
        if not num:
            return  # already caught by required fields

        # Example rule: must contain at least one alphanumeric
        if not any(c.isalnum() for c in num):
            self.errors.append(f"Invalid card number: {num}")

    def _check_parallel(self):
        parallel = self.row.normalized_parallel

        # Parallel is optional for some sets
        if parallel is None:
            return

        # Example: check against known parallels
        from mintcastiq.models import DimParallel

        if not DimParallel.objects.filter(name=parallel).exists():
            self.errors.append(f"Unknown parallel: {parallel}")
