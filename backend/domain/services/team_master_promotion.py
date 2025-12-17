def promote_staged_team(staged: StagedTeamMaster) -> FactTeamMaster:
    if not staged.raw_full_name:
        raise ValueError("Missing full_name")
    if not staged.raw_team_name:
        raise ValueError("Missing team_name")
    if not staged.card:
        raise ValueError("Missing card FK")
    if not staged.parallel:
        raise ValueError("Missing parallel FK")

    team = FactTeamMaster.objects.create(
        full_name=staged.raw_full_name,
        team_name=staged.raw_team_name,
        card=staged.card,
        parallel=staged.parallel,
    )

    staged.delete()
    return team
