import csv
from pathlib import Path


class CSVChecklistParser:
    """
    Parses a contributor-provided CSV checklist file and yields raw dict rows.
    This parser performs no normalization or validation — it simply exposes
    the contributor's input in a structured form.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def parse(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Checklist file not found: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Convert empty strings to None for consistency
                cleaned = {k: (v.strip() if isinstance(v, str) else v) or None for k, v in row.items()}
                yield cleaned
