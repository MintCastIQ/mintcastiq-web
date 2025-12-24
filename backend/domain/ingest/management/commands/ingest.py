from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from domain.ingest.ingest_dispatcher import IngestDispatcher
from mintcastiq.models.staging.staging_checklist_row import StagingChecklistRow
from domain.ingest.staging_writer import DryRunWriter, StagingWriter


class Command(BaseCommand):
    help = "Run the MintCastIQ ingest pipeline on a directory of files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run ingest without writing to the database; output rows to a file."
        )

    def run_staging_phase(self) -> int:
        # In this simplified example, we assume staging is done in the dispatcher
        return StagingChecklistRow.objects.count()  # Total rows in staging
    
    def run_loader_phase(self) -> int:
        return StagingChecklistRow.objects.filter(status="LOADED").count()
    


    def handle(self, *args, **options):
        CHECKLIST_DIR = "/opt/mintcastiq_web/backend/configs/checklists/staging"
        directory = Path(CHECKLIST_DIR)
        if options["dry_run"]:
            writer = DryRunWriter()
        else:
            writer = StagingWriter()
            
        

        if not directory.exists() or not directory.is_dir():
            raise CommandError(f"Directory does not exist: {directory}")

        self.stdout.write(self.style.NOTICE(f"Starting ingest for: {directory}"))

        total_written = self.run_staging_phase()
        self.stdout.write(self.style.SUCCESS(f"Staging complete: {total_written:,} rows"))

        total_loaded = self.run_loader_phase()
        self.stdout.write(self.style.SUCCESS(f"Canonical load complete: {total_loaded:,} rows"))

        deleted = self.cleanup_processed_rows()
        self.stdout.write(self.style.WARNING(f"Cleaned up {deleted:,} processed staging rows"))

        dispatcher = IngestDispatcher(directory)
        dispatcher.run()

        self.stdout.write(self.style.SUCCESS("Ingest completed successfully."))

    def cleanup_processed_rows(self):
        qs = StagingChecklistRow.objects.filter(processed_at__isnull=False)
        count = qs.count()
        qs.delete()
        return count
