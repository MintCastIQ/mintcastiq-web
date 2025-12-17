def promote_staged_inventory(staged: StagedInventory) -> FactInventory:
    if not staged.user:
        raise ValueError("Missing user")

    inv = FactInventory.objects.create(
        user=staged.user
    )

    staged.delete()
    return inv
