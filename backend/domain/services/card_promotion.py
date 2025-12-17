def promote_staged_card(staged: StagedCard) -> DimCard:
    # Ensure all required FKs are resolved
    if not staged.cardset:
        raise ValueError("StagedCard missing cardset")
    if not staged.parallel:
        raise ValueError("StagedCard missing parallel")
    if not staged.raw_name:
        raise ValueError("StagedCard missing name")

    card = DimCard.objects.create(
        name=staged.raw_name,
        team_name=staged.raw_team_name,
        card_number=staged.raw_card_number,
        cardset=staged.cardset,
        parallel=staged.parallel,
    )

    staged.delete()
    return card
