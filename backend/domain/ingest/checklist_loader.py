from mintcastiq.models import (
    DimSet,
    DimCard,
    DimParallel,
    DimCardParallel,
    FactChecklistEntry,
)
from mintcastiq.models import StagingChecklistRow
from mintcastiq.models.staging.staging_checklist_row import StagingChecklistRow
from mintcastiq.models.fact_checklist_entry import FactChecklistEntry


class ChecklistLoader:
    """
    Loads validated staging rows into canonical dimension tables.
    """

    def load_validated_rows(self):
        rows = StagingChecklistRow.objects.filter(status="VALIDATED")

        for row in rows:
            try:
                self._load_row(row)
                row.status = "LOADED"
            except Exception as e:
                row.status = "ERROR"
                row.load_error = str(e)

            row.save()
            row.mark_processed()

    # ----------------------------------------
    # Load a single staging row
    # ----------------------------------------
    def _load_row(self, row):
        data = row.normalized_row  # assuming normalized_row is a dict

        dim_set = self._get_or_create_set(data)
        dim_card = self._get_or_create_card(data, dim_set)
        dim_parallel = self._get_or_create_parallel(data)

        if dim_parallel:
            dim_card_parallel = self._get_or_create_card_parallel(dim_card, dim_parallel)
        else:
            dim_card_parallel = None

        self._create_fact_entry(row, dim_card, dim_card_parallel)

    # ----------------------------------------
    # Dimension resolvers
    # ----------------------------------------
    def _get_or_create_set(self, data):
        return DimSet.objects.get_or_create(
            name=data["set"]
        )[0]

    def _get_or_create_card(self, data, dim_set):
        return DimCard.objects.get_or_create(
            set=dim_set,
            card_number=data["card_number"],
            defaults={
                "player_name": data["player"],
                "team_name": data["team"],
            }
        )[0]

    def _get_or_create_parallel(self, data):
        parallel = data.get("parallel")
        if not parallel:
            return None
        return DimParallel.objects.get_or_create(name=parallel)[0]

    def _get_or_create_card_parallel(self, dim_card, dim_parallel):
        return DimCardParallel.objects.get_or_create(
            card=dim_card,
            parallel=dim_parallel
        )[0]

    # ----------------------------------------
    # Fact table
    # ----------------------------------------
    def _create_fact_entry(self, row, dim_card, dim_card_parallel):
        FactChecklistEntry.objects.create(
            card=dim_card,
            card_parallel=dim_card_parallel,
            source_file=row.source_file,
            source_sheet=row.source_sheet,
            source_row=row.row_number,
            raw_data=row.raw_row,
        )