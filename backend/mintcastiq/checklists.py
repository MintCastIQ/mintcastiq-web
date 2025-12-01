def normalize_all_sheets(sheets):
    sets, parallels, cards = [], [], []

    for sheet in sheets:
        if sheet["name"] in ["Base", "Autographs", "Memorabilia", "Inserts", "XRC Redemptions"]:
            # Mode 1: subset + parallel declarations
            for subset in sheet["subsets"]:
                for card in subset["cards"]:
                    for parallel in subset["parallels"]:
                        if card["card_number"] not in parallel.get("exclusions", []):
                            sets.append({
                                "subset_name": subset["subset_name"],
                                "sheet": sheet["name"]
                            })
                            parallels.append({
                                "parallel_name": parallel["name"],
                                "print_run": parallel["print_run"],
                                "subset": subset["subset_name"]
                            })
                            cards.append({
                                "card_number": card["card_number"],
                                "player_name": card["player_name"],
                                "team": card["team"],
                                "parallel": parallel["name"],
                                "subset": subset["subset_name"],
                                "sheet": sheet["name"]
                            })
        else:
            # Mode 2: fully expanded tables (Teams, Master Checklist)
            for card in sheet["cards"]:
                sets.append({
                    "subset_name": sheet["name"],
                    "sheet": sheet["name"]
                })
                parallels.append({
                    "parallel_name": card["parallel"],
                    "print_run": card.get("print_run"),
                    "subset": sheet["name"]
                })
                cards.append(card)

    return {"sets": sets, "parallels": parallels, "cards": cards}

def validate_against_master(expanded_cards, master_cards):
    """
    Compare expanded subset cards against the master checklist.

    Args:
        expanded_cards: list of dicts from normalize_all_sheets (fan‑out mode)
        master_cards: list of dicts from Master Checklist sheet (already expanded)

    Returns:
        dict with missing, extra, and matched counts
    """
    # Build lookup sets for fast comparison
    expanded_set = {
        (c["card_number"], c["player_name"], c["team"], c["parallel"], c["subset"])
        for c in expanded_cards
    }
    master_set = {
        (c["card_number"], c["player_name"], c["team"], c["parallel"], c["subset"])
        for c in master_cards
    }

    missing = master_set - expanded_set   # cards in master but not in expanded
    extra   = expanded_set - master_set   # cards in expanded but not in master
    matched = expanded_set & master_set   # intersection

    return {
        "missing_count": len(missing),
        "extra_count": len(extra),
        "matched_count": len(matched),
        "missing_examples": list(missing)[:10],
        "extra_examples": list(extra)[:10]
    }
