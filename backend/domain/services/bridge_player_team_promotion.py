def promote_staged_player_team(staged: StagedPlayerTeam) -> BridgePlayerTeam:
    if not staged.player:
        raise ValueError("Missing player FK")
    if not staged.team:
        raise ValueError("Missing team FK")

    bridge = BridgePlayerTeam.objects.create(
        player=staged.player,
        team=staged.team,
    )

    staged.delete()
    return bridge
