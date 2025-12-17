def promote_staged_inventory_detail(staged: StagedInventoryDetail) -> FactInventoryDetail:
    # Ensure all required FKs are resolved
    if not staged.inventory:
        raise ValueError("Missing inventory")
    if not staged.player_master:
        raise ValueError("Missing player_master")
    if not staged.team_master:
        raise ValueError("Missing team_master")
    if not staged.grade:
        raise ValueError("Missing grade")
    if staged.raw_quantity is None:
        raise ValueError("Missing quantity")
    if staged.raw_acquired_at is None:
        raise ValueError("Missing acquired_at")

    detail = FactInventoryDetail.objects.create(
        inventory=staged.inventory,
        player_master=staged.player_master,
        team_master=staged.team_master,
        grade=staged.grade,
        quantity=staged.raw_quantity,
        acquired_at=staged.raw_acquired_at,
        source=staged.raw_source,
        notes=staged.raw_notes,
        upc=staged.raw_upc,
    )

    staged.delete()
    return detail
