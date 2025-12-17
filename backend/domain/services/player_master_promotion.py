def promote_staged_player(staged: StagedPlayerMaster) -> FactPlayerMaster:
    if not staged.raw_full_name:
        raise ValueError("Missing full_name")
    if not staged.raw_player_name:
        raise ValueError("Missing player_name")
    if not staged.card:
        raise ValueError("Missing card FK")
    if not staged.parallel:
        raise ValueError("Missing parallel FK")

    player = FactPlayerMaster.objects.create(
        full_name=staged.raw_full_name,
        player_name=staged.raw_player_name,
        card=staged.card,
        parallel=staged.parallel,
    )

    staged.delete()
    return player
