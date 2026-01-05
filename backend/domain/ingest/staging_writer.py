import datetime
import json
import time
import os.path
from decimal import Decimal
from mintcastiq.models.staging.staging_checklist_row import StagingChecklistRow



class StagingWriter:
    """
    Writes normalized checklist rows into the staging table.
    """
    def __init__(self):
        self.count = 0
        self.start_time = time.time()

    @staticmethod
    def json_safe(value):
        if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return float(value)
        return value

    def write(self, raw_row: dict) -> StagingChecklistRow:
        safe_row = {k: self.json_safe(v) for k, v in raw_row.items()}
        staging = StagingChecklistRow.objects.create(raw_row=safe_row)
        self.count += 1

        if self.count % 1000 == 0:
            elapsed = time.time() - self.start_time
            rate = self.count / elapsed
            print(f"[staging] {self.count:,} rows written "
                  f"({elapsed:.1f}s elapsed, {rate:.1f} rows/sec)")

        return staging


class DryRunWriter:
    def __init__(self):
        self.output_path = "/opt/mintcastiq_web/backend/configs/checklists/dry_run_output"
        self.output_file = f"dry_run_{int(time.time())}.jsonl"
        full_path = os.path.join(self.output_path, self.output_file)
        self.file = open(full_path, "w", encoding="utf-8")

        self.count = 0
        self.blank_subset_count = 0
        self.start = time.time()

    def write(self, raw_row: dict):
        json.dump(raw_row, self.file, ensure_ascii=False)
        self.file.write("\n")

        self.count += 1
        if not raw_row.get("subset_name"):
            self.blank_subset_count += 1

        if self.count % 1000 == 0:
            elapsed = time.time() - self.start
            rate = self.count / elapsed
            print(
                f"[dry-run] {self.count:,} rows "
                f"({elapsed:.1f}s elapsed, {rate:.1f} rows/sec)"
            )

    def close(self):
        self.file.close()

    def summary(self, workbook_name: str, sheet_name: str):
        elapsed = time.time() - self.start
        print(f"\n[dry-run][summary]")
        print(f"  Workbook: {workbook_name}")
        print(f"  Sheet: {sheet_name}")
        print(f"  Rows written: {self.count:,}")
        print(f"  Blank subset_name: {self.blank_subset_count:,}")
        print(f"  Elapsed: {elapsed:.1f}s")
