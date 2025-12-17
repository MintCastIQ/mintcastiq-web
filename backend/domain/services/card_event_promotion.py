def promote_staged_card_event(staged: StagedCardEvent) -> FactCardEvents:
    if not staged.card:
        raise ValueError("Missing card")
    if not staged.user:
        raise ValueError("Missing user")
    if not staged.set:
        raise ValueError("Missing set")
    if not staged.grade:
        raise ValueError("Missing grade")
    if not staged.raw_action_type:
        raise ValueError("Missing action_type")

    event = FactCardEvents.objects.create(
        card=staged.card,
        user=staged.user,
        set=staged.set,
        grade=staged.grade,
        action_type=staged.raw_action_type,
        timestamp=staged.raw_timestamp or timezone.now(),
        confidence_score=staged.raw_confidence_score,
        processing_time_ms=staged.raw_processing_time_ms,
    )

    staged.delete()
    return event
