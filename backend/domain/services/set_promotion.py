from mintcastiq.models.dim_set import DimSet
from mintcastiq.models.staging.staged_set import StagedSet
from domain.services.promotion_result import PromotionResult


class DimSetPromotionService:
    """
    Promote a staged set into the canonical DimSet dimension.

    Responsibilities:
    - Validate staged data
    - Normalize fields via canonicalize()
    - Compute identity + checksum via BaseIdentity
    - Prevent accidental overwrites
    - Support dry-run mode
    - Return structured PromotionResult
    """

    @staticmethod
    def promote(staged: StagedSet, dry_run=False) -> PromotionResult:
        warnings = []

        # ----------------------------------------
        # 1. Extract staged fields
        # ----------------------------------------
        data = {
            "set_name": staged.set_name,
            "publisher": staged.publisher,
            "set_year": staged.set_year,
            "subset_name": staged.subset_name,
            "brand": staged.brand,
            "sport": staged.sport,
            "set_code": staged.set_code,
        }

        # ----------------------------------------
        # 2. Canonicalize staged data (preview)
        # ----------------------------------------
        preview = DimSet(**data).canonicalize()

        # ----------------------------------------
        # 3. Compute identity_string for lookup
        # ----------------------------------------
        preview._compute_identity()

        # ----------------------------------------
        # 4. Check if canonical object already exists
        # ----------------------------------------
        try:
            existing = DimSet.objects.get(identity_string=preview.identity_string)
            if dry_run:
                return PromotionResult(
                    created=False,
                    updated=False,
                    canonical_object=existing,
                    warnings=["Dry run: existing object would be reused"]
                )

            # No updates allowed — identity is immutable
            return PromotionResult(
                created=False,
                updated=False,
                canonical_object=existing,
            )

        except DimSet.DoesNotExist:
            pass

        # ----------------------------------------
        # 5. Create new canonical object
        # ----------------------------------------
        if dry_run:
            return PromotionResult(
                created=True,
                updated=False,
                canonical_object=preview,
                warnings=["Dry run: object would be created"]
            )

        canonical = DimSet.create(**data)

        return PromotionResult(
            created=True,
            updated=False,
            canonical_object=canonical,
        )
