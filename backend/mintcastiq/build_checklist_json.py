import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


import pandas as pd
import json
import glob
import os
import django

# Point to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mciq.settings")
django.setup()

from mintcastiq.models import DimSet, DimParallel, DimCard  # adjust import path

def normalize_print_run(value: str) -> int | None:
    if not value:
        return None
    value = str(value).strip()
    if value == "1/1":
        return 1
    if value.startswith("/"):
        value = value[1:]
    try:
        return int(value.split("/")[-1])
    except ValueError:
        return None

def build_checklist_json(file_path: str) -> dict:
    df = pd.read_excel(file_path, sheet_name="Master")

    sets: list[DimSet] = []
    parallels: list[DimParallel] = []
    cards: list[DimCard] = []
    logging.info(f"Sets={len(sets)}, Parallels={len(parallels)}, Cards={len(cards)}")                              #log
    current_base = None

    for _, row in df.iterrows():
        subset_name = str(row["subset_name"]).strip()

        # New base subset or reset
        if current_base is None or subset_name == current_base or not subset_name.startswith(current_base):
            current_base = subset_name

            new_set = DimSet(
                set_name=str(row["set_name"]).strip(),
                publisher=str(row["brand"]).strip(),
                set_year=int(row["set_year"]),
                subset_name=current_base
            )
            if not any(s.json_eq(new_set) for s in sets):
                sets.append(new_set)

            new_card = DimCard(
                cardset = new_set,
                card_number=str(row["card_number"]).strip(),
                name=str(row["player"]).strip(),
                team_name=str(row["team_name"]).strip()
            )
            if not any(c.json_eq(new_card) for c in cards):
                cards.append(new_card)

        else:
            # Parallel row
            suffix = subset_name[len(current_base):].strip()
            if suffix:
                new_parallel = DimParallel(
                    cardset = new_set,
                    parallel_name=suffix,
                    print_run=normalize_print_run(row.get("print_run"))
                )
                if not any(p.json_eq(new_parallel) for p in parallels):
                    parallels.append(new_parallel)
            # ⚠️ No card added here

    # Serialize to JSON
    logging.info(f"Sets={len(sets)}, Parallels={len(parallels)}, Cards={len(cards)}") 
    sets_d = []
    parallels_d = []
    cards_d = []
    for s in sets:
        sets_d.append(s.to_dict())
    for p in parallels:
        parallels_d.append(p.to_dict())
    for c in cards:
        cards_d.append(c.to_dict())
                                      # log
    return {
        "sets": sets_d,
        "parallels": parallels_d,
        "cards": cards_d,
    }

def process_staging_files():
    for file_path in glob.glob("mintcastiq/checklists/staging/*.xlsx"):
        logging.info(f"Processing file: {file_path}")                                                                 #  log
        checklist_json = build_checklist_json(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        json_path = f"mintcastiq/checklists/staging/{base_name}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(checklist_json, f, indent=2)
        print(f"✅ JSON written: {json_path}")

def main():
    logging.info("Executing inside main()")
    process_staging_files()

if __name__ == "__main__":
    main()

