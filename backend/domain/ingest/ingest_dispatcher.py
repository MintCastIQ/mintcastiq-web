from pathlib import Path

from domain.ingest.parsers.dispatcher import ChecklistParserDispatcher
from domain.ingest.staging_writer import StagingWriter
from domain.ingest.checklist_normalization_service import ChecklistNormalizationService
from domain.ingest.checklist_validation_service import ChecklistValidationService
from domain.ingest.checklist_loader import ChecklistLoader
from domain.ingest.scanner import ScanIngestService
import time


class IngestDispatcher:
    """
    Orchestrates all ingest operations for MintCastIQ.
    Determines whether a directory contains checklist files,
    scan images, or both, and dispatches to the correct pipeline.
    """

    CHECKLIST_EXTS = {".xlsx", ".csv", ".json"}
    SCAN_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

    def __init__(self, directory_path):
        self.directory = Path(directory_path)

    def run(self):
        checklist_files = []
        scan_files = []

        for file in self.directory.iterdir():
            if not file.is_file():
                continue

            ext = file.suffix.lower()

            if ext in self.CHECKLIST_EXTS:
                checklist_files.append(file)
            elif ext in self.SCAN_EXTS:
                scan_files.append(file)

        if checklist_files:
            self._run_checklist_ingest()

        if scan_files:
            self._run_scan_ingest()

    # ----------------------------------------
    # Checklist ingest pipeline
    # ----------------------------------------
    def _run_checklist_ingest(self):
        start = time.time()
        count = 0
        errors = []
        dispatcher = ChecklistParserDispatcher(self.directory)
        writer = StagingWriter()

        for raw_row in dispatcher.parse():
            try:
                writer.write(raw_row)
                # normalized = ChecklistNormalizationService(raw_row).run()
                # ChecklistValidationService(normalized).run()
                

                count += 1
                if count % 1000 == 0:
                    elapsed = time.time() - start
                    rate = count / elapsed
                    print(f"[ingest] {count:,} rows staged "
                          f"({elapsed:.1f}s elapsed, {rate:.1f} rows/sec)")

            except Exception as e:   
                errors.append((raw_row, str(e)))
                print(f"[ingest][error] Failed to stage row: {e}")
                continue

        ChecklistLoader().load_validated_rows()
        elapsed = time.time() - start

        print("\n=== INGEST SUMMARY ===")
        print(f"Rows written: {count:,}")
        print(f"Errors:       {len(errors):,}")
        print(f"Total time:   {elapsed:.1f}s")
        print(f"Rate:         {count/elapsed:.1f} rows/sec")

        if errors:
            print("\nFirst few errors:")
            for idx, err in enumerate(errors[:5]):
                print(f"{idx+1}. {err}")
            if len(errors) > 5:
                print("... (more errors not shown)")

    # ----------------------------------------
    # Scan ingest pipeline
    # ----------------------------------------
    def _run_scan_ingest(self):
        ScanIngestService(self.directory).run()

