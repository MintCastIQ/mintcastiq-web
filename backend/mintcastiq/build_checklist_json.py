import pandas as pd
import json
import glob
import os

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

    # Top-level set info (all rows share same set_name/brand/year)
    set_name = str(df.iloc[0]["set_name"]).strip()
    brand = str(df.iloc[0]["brand"]).strip()
    set_year = int(df.iloc[0]["set_year"])

    subsets = {}
    subset_counter = 1

    for _, row in df.iterrows():
        subset_name = str(row["subset_name"]).strip()
        card_number = str(row["card_number"]).strip()
        player = str(row["player"]).strip()
        team_name = str(row["team_name"]).strip()
        print_run = normalize_print_run(row.get("print_run"))

        # Initialize subset entry if first time seen
        if subset_name not in subsets:
            subsets[subset_name] = {
                "id": f"subset_{subset_counter}",
                "subset_name": subset_name,
                "parallels": [],
                "cards": []
            }
            subset_counter += 1

        # Detect parallel suffix relative to first occurrence of this subset
        base_name = subsets[subset_name]["subset_name"]
        parallel_name = None
        if subset_name != base_name and subset_name.startswith(base_name):
            suffix = subset_name[len(base_name):].strip()
            parallel_name = suffix if suffix else None

        if parallel_name:
            subsets[subset_name]["parallels"].append({
                "parallel_name": parallel_name,
                "print_run": print_run
            })

        # Add card
        subsets[subset_name]["cards"].append({
            "card_number": card_number,
            "name": player,
            "team_name": team_name
        })

    # Build final JSON
    return {
        "set_name": set_name,
        "publisher": brand,
        "set_year": set_year,
        "subsets": list(subsets.values())
    }

def process_staging_files():
    for file_path in glob.glob("checklists/staging/*.xlsx"):
        checklist_json = build_checklist_json(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        json_path = f"checklists/staging/{base_name}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(checklist_json, f, indent=2)
        print(f"✅ JSON written: {json_path}")

def main():
    process_staging_files()

if __name__ == "__main__":
    main()
