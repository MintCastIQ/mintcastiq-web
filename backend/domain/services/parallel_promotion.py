# mintcastiq/services/parallel_promotion.py

from mintcastiq.models import DimParallel, StagedParallel

def promote_staged_parallel(staged: StagedParallel) -> DimParallel:
    """
    Promote a StagedParallel into a strict DimParallel.
    Ensures all required fields are present before creation.
    """

    # Required FK
    if not staged.card_set:
        raise ValueError("StagedParallel is missing card_set")

    # Required name
    if not staged.raw_parallel_name:
        raise ValueError("StagedParallel is missing parallel_name")

    parallel = DimParallel.objects.create(
        parallel_name=staged.raw_parallel_name,
        print_run=staged.raw_print_run,
        card_set=staged.card_set,
    )

    staged.delete()
    return parallel
