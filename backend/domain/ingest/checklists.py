import os, json, openpyxl, yaml
import logging
from datetime import datetime
import importlib
from domain.hashing import hash_string, hash_file

STAGING_DIR = "staging"
BASE_PATH = "/opt/mintcastiq_web/backend/mintcastiq/checklists"
CONFIG_PATH = "/opt/mintcastiq_web/backend/mintcastiq/"
CONFIG_FILE = os.path.join(CONFIG_PATH, "checklists.yaml")

config = {
    "defaults": {
        "columns": {
            "cards": {
                0: "card_number",
                1: "player_name",
                2: "team_name",
                3: "print_run"
            },
            "subset": {
                0: "subset_name"
            },
            "parallel": {
                0: "parallel_name"
            }
        }
    },
    "2024-Panini-Select-Football-Checklist": {
        "meta": {
            "sport": "Football",
            "year": 2024,
            "brand": "Panini",
            "set_name": "Select",
            "source_file": "2024-Panini-Select-Football-Checklist.xlsx",
            "last_modified": "2024-09-15T12:34:56Z",
            "columns": {
                "cards": {
                    0: "card_number",
                    1: "player_name",
                    2: "team_name",
                    3: "print_run"
                },
                "subset": {
                    0: "subset_name"
                },
                "parallel": {
                    0: "parallel_name"
                }
            },
            "checksum": "sha256:sbfe6aac71f6763ccfb707e04d1749f30ab9e02781854a37e812c048e0bf9f5d0"
        },
        "column_sets": {
            "with_subset_skip4": {
                0: "subset_name",
                1: "card_number",
                2: "player_name",
                3: "team_name",
                5: "print_run"
            },
            "with_subset": {
                0: "subset_name",
                1: "card_number",
                2: "player_name",
                3: "team_name",
                4: "print_run"
            }
        },
        "sheets": {
            0: {"name": "Base"},
            1: {"name": "Autographs"},
            2: {"name": "Memorabilia"},
            3: {"name": "Inserts"},
            4: {"name": "XRC Redemptions"},
            5: {
                "name": "Teams",
                "columns": "with_subset_skip4",
                "intentional_gaps": [4]  # gap at index 4
            },
            6: {
                "name": "Master Checklist",
                "columns": "with_subset"
            }
        }
    },
    "2024-Panini-Illusions-Football-Checklist": {
        "meta": {
            "sport": "Football",
            "year": 2024,
            "brand": "Panini",
            "set_name": "Illusions",
            "source_file": "2024-Panini-Illusions-Football-Checklist.xlsx",
            "last_modified": "2024-09-20T08:00:00Z",
            "columns": {
                0: "card_number",
                1: "player_name",
                2: "team_name",
                3: "print_run"
            },
            "checksum": "sha256:0dee7196dff5638f957ceab29d09c6f898b0aca1e4a3c865d22dd3ca8dc0c3a1"
        },
        "column_sets": {
            "with_subset": {
                0: "subset_name",
                1: "card_number",
                2: "player_name",
                3: "team_name",
                4: "print_run"
            },
            "with_subset_team_focus": {
                0: "team_name",
                1: "subset_name",
                2: "card_number",
                3: "player_name",
                4: "print_run"
            }
        },
        "sheets": {
            0: {"name": "Base"},
            1: {"name": "Autographs"},
            2: {"name": "Memorabilia"},
            3: {"name": "Inserts"},
            4: {
                "name": "Teams",
                "columns": "with_subset_team_focus"
               },
            5: {
                "name": "Master",
                "columns": "with_subset"
               }
        }
    }
}

def validate_config(config: dict) -> bool:
    """
    Validate ingest config:
    - Resolve column aliases
    - Handle intentional gaps
    - Log results using main()'s logging config
    Returns True if config passes, False if errors found.
    """
    # validate the provided config dict; do not reference external globals here

    errors_found = False

    for checklist_name, checklist in config.items():
        meta = checklist.get("meta", {})
        column_sets = checklist.get("column_sets", {})
        sheets = checklist.get("sheets", {})

        logging.info(f"Validating checklist: {checklist_name}")

        for sheet_idx, sheet in sheets.items():
            sheet_name = sheet.get("name", f"Sheet{sheet_idx}")
            columns = sheet.get("columns")

            # Resolve alias → dict
            if isinstance(columns, str):
                if columns in column_sets:
                    resolved = column_sets[columns].copy()
                else:
                    logging.error(
                        f"[{checklist_name}:{sheet_name}] Unknown column alias '{columns}'"
                    )
                    errors_found = True
                    continue
            elif isinstance(columns, dict):
                resolved = columns.copy()
            else:
                resolved = meta.get("columns", {}).copy()

            # Handle intentional gaps
            gaps = sheet.get("intentional_gaps", [])
            for gap in gaps:
                if gap in resolved:
                    logging.error(
                        f"[{checklist_name}:{sheet_name}] Gap declared but column present at index {gap}"
                    )
                    errors_found = True
                else:
                    logging.info(
                        f"[{checklist_name}:{sheet_name}] Index {gap} intentionally blank"
                    )

            # Syntax sanity check
            # Support two shapes for `resolved`:
            # 1) A dict of sections: {"cards": {0: "card_number", ...}, ...}
            # 2) A flat mapping used by column_sets: {0: "card_number", 1: "player_name", ...}
            if isinstance(resolved, dict) and resolved and all(isinstance(k, int) for k in resolved.keys()) and all(isinstance(v, str) for v in resolved.values()):
                # Flat mapping — validate as single unnamed section
                mapping_iter = [("default", resolved)]
            else:
                mapping_iter = resolved.items()

            for section, mapping in mapping_iter:
                if not isinstance(mapping, dict):
                    logging.error(
                        f"[{checklist_name}:{sheet_name}] Section '{section}' must be a dict"
                    )
                    errors_found = True
                    continue

                for idx, name in mapping.items():
                    if not isinstance(idx, int):
                        logging.error(
                            f"[{checklist_name}:{sheet_name}] Non-integer column index '{idx}' in section '{section}'"
                        )
                        errors_found = True
                    elif not isinstance(name, str):
                        logging.error(
                            f"[{checklist_name}:{sheet_name}] Non-string column name at index {idx} in section '{section}': {name}"
                        )
                        errors_found = True
                    else:
                        logging.debug(
                            f"[{checklist_name}:{sheet_name}] Section '{section}' Column {idx} = {name} OK"
                        )

    if errors_found:
        logging.error("Config validation FAILED")
    else:
        logging.info("Config validation PASSED")

    return not errors_found

def safe_get(row, idx):
    if idx >= 0 and idx < len(row):
        val = row[idx]
        if val is not None:
            return str(val).strip()
    return ""

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not validate_config(cfg):
        raise RuntimeError("Checklist config validation failed")
    return cfg

def get_col_values(row, cols) -> dict:
    vals = {}
    for idx, field_name in cols.items():
        val = safe_get(row, idx)
        vals[field_name] = val
    return vals

def resolve_columns(sheet_def, column_sets, meta, defaults, row_type="cards"):
        """
        Resolve column mapping for a given row type.
        Priority:
          1. Explicit sheet_def["columns"] (string key or dict)
          2. Meta["columns"][row_type]
          3. Defaults["columns"][row_type]
        """
        columns = sheet_def.get("columns")
        if isinstance(columns, str) and columns in column_sets:
            return column_sets[columns]
        elif isinstance(columns, dict):
            return columns
        elif "columns" in meta and row_type in meta["columns"]:
            return meta["columns"][row_type]
        else:
            return defaults["columns"].get(row_type, {})

def build(row, col_map, meta) -> dict:
    # Build value objects for richer representation
    vals = {field_name: safe_get(row, idx) for idx, field_name in col_map.items()}

    # Canonical key always starts with meta
    key_parts = [meta.get("year"), meta.get("brand"), meta.get("set_name")]
    for field in ("subset_name", "parallel_name", "card_number"):
        if vals.get(field):
            key_parts.append(vals[field])

    k = "-".join(map(str, key_parts))

    # Try to use Django model classes if available, otherwise fall back
    try:
        from mintcastiq.models import DimSet as ModelDimSet, DimCard as ModelDimCard, DimParallel as ModelDimParallel
    except Exception:
        ModelDimSet = ModelDimCard = ModelDimParallel = None

    # Decide which model object to build (do NOT save to DB here)
    # Map fields from meta/vals into model constructor kwargs
    if vals.get("card_number"):
        # build a DimCard-like object
        card_kwargs = {
            "name": vals.get("player_name") or vals.get("parallel_name") or "",
            "team_name": vals.get("team_name"),
            "card_number": vals.get("card_number"),
            "cardset": None,
        }
        if ModelDimCard:
            obj = ModelDimCard(**card_kwargs)
            setattr(obj, "parallel", None)
        else:
            # fallback lightweight object that mirrors earlier meta/vals merging
            class DimCard:
                def __init__(self, meta, vals):
                    self.meta = dict(meta)
                    self.vals = dict(vals)
                    self.cardset = None
                    self.parallel = None

                def to_dict(self):
                    out = {**self.meta, **self.vals}
                    out["parallel"] = None
                    if self.cardset is not None:
                        out["cardset"] = self.cardset.to_dict() if hasattr(self.cardset, "to_dict") else self.cardset
                    return out

            obj = DimCard(meta, vals)
    elif vals.get("parallel_name") and not vals.get("card_number"):
        parallel_kwargs = {
            "parallel_name": vals.get("parallel_name"),
            "print_run": vals.get("print_run") if vals.get("print_run") else None,
            "cardset": None,
        }
        if ModelDimParallel:
            obj = ModelDimParallel(**parallel_kwargs)
        else:
            class DimParallel:
                def __init__(self, meta, vals):
                    self.meta = dict(meta)
                    self.vals = dict(vals)
                    self.cardset = None

                def to_dict(self):
                    out = {**self.meta, **self.vals}
                    if self.cardset is not None:
                        out["cardset"] = self.cardset.to_dict() if hasattr(self.cardset, "to_dict") else self.cardset
                    return out

            obj = DimParallel(meta, vals)
    else:
        # subset / generic set
        set_kwargs = {
            "set_name": meta.get("set_name"),
            "publisher": meta.get("brand"),
            "set_year": str(meta.get("year")) if meta.get("year") else None,
            "subset_name": vals.get("subset_name"),
            "print_run": vals.get("print_run") if vals.get("print_run") else None,
            "friendly_name": f"{meta.get('year')}-{meta.get('brand')}-{meta.get('set_name')}",
        }
        if ModelDimSet:
            obj = ModelDimSet(**set_kwargs)
        else:
            class DimSet:
                def __init__(self, meta, vals):
                    self.meta = dict(meta)
                    self.vals = dict(vals)

                def to_dict(self):
                    return {**self.meta, **self.vals}

            obj = DimSet(meta, vals)

    return {k: obj}

def classify_row(row, is_parallel):
        # Parallel marker row should be detected before subset rows
        first_col = (safe_get(row, 0) or "").strip()
        if not first_col:
            return "unknown", {}
        elif "parallel" in first_col.lower():
            return "parallel_marker", {"parallel_name": safe_get(row, 0)}

        # Parallel rows: only col0 populated, in parallel mode
        elif safe_get(row, 0) and not safe_get(row, 1) and not safe_get(row, 2) and is_parallel:
            return "parallel", {"parallel_name": safe_get(row, 0)}

        # Subset rows: only col0 populated, not in parallel mode
        elif safe_get(row, 0) and not safe_get(row, 1) and not safe_get(row, 2) and not is_parallel:
            return "subset", {"subset_name": safe_get(row, 0)}

        # Master rows: card fields + extras
        elif safe_get(row, 1) and safe_get(row, 2) and safe_get(row, 3) and safe_get(row, 4):
            return "master", {
                "card_number": safe_get(row, 1),
                "player_name": safe_get(row, 2),
                "team_name": safe_get(row, 3),
                "print_run": safe_get(row, 4),
            }

        # Card rows: basic card fields
        elif safe_get(row, 1) and safe_get(row, 2):
            return "card", {
                "card_number": safe_get(row, 1),
                "player_name": safe_get(row, 2),
                "team_name": safe_get(row, 3),
            }

        else:
            return "unknown", {}

def ingest_checklist(ws, filename, sheetname, cfg):
    meta = cfg.get("meta", {})
    sheets = cfg.get("sheets", {})
    column_sets = cfg.get("column_sets", {})
    defaults = cfg.get("defaults", {})

    sheet_def = next((s for s in sheets.values() if s["name"].lower() == sheetname.lower()), None)
    if not sheet_def:
        logging.warning(f"No config for sheet {sheetname}, skipping")
        return {"cards": {}, "parallels": {}}

    rows = list(ws.iter_rows(values_only=True))
    is_parallel = False

    # --- Outer loop ---
    current_subset = None
    parallels = {}
    cards = {}

    for row in rows:
        mode, vals = classify_row(row, is_parallel)

        if mode == "parallel_marker":
            is_parallel = True
            continue
        elif mode == "card":
            is_parallel = False  # flip back out of parallel mode
        col_map = resolve_columns(sheet_def, column_sets, meta, defaults, mode)
        artifact = build(row, col_map, meta)

        if mode == "subset":
            # store the DimSet instance (first/only value)
            current_subset = next(iter(artifact.values()))
            # normalize to a serializable dict for later attachment
            current_subset = current_subset.to_dict() if hasattr(current_subset, "to_dict") else current_subset

        elif mode == "parallel":
            for k, v in artifact.items():
                # v is a DimParallel instance — attach cardset and serialize
                if current_subset is not None:
                    v.cardset = current_subset
                d = v.to_dict() if hasattr(v, "to_dict") else v
                if "cardset" not in d:
                    d["cardset"] = current_subset if current_subset is not None else None
                parallels.update({k: d})

        elif mode in ("card", "master"):
            for k, v in artifact.items():
                if current_subset is not None:
                    v.cardset = current_subset
                d = v.to_dict() if hasattr(v, "to_dict") else v
                if "cardset" not in d:
                    d["cardset"] = current_subset if current_subset is not None else None
                cards.update({k: d})

    return {"cards": cards, "parallels": parallels}

def ingest_workbook(wb, filename, all_cfg):
    """
    Process a workbook using the top-level checklists configuration `all_cfg`.
    `all_cfg` maps checklist keys (filename without .xlsx) to per-checklist configs.
    """
    checklist_key = filename.replace(".xlsx", "")
    cfg = all_cfg.get(checklist_key)
    if not cfg:
        logging.warning(f"No checklist config for {filename}")
        return {"cards": {}, "parallels": {}}

    all_results = {"cards": {}, "parallels": {}}
    for sheetname in wb.sheetnames:
        ws = wb[sheetname]
        logging.info(f"Processing {sheetname}...")
        result = ingest_checklist(ws, filename, sheetname, cfg)
        all_results["cards"].update(result["cards"])
        all_results["parallels"].update(result["parallels"])
    return all_results

def main():
    # Load external config if present, otherwise fall back to embedded `config`
    if os.path.exists(CONFIG_FILE):
        logging.info(f"Loading external checklist config from {CONFIG_FILE}")
        cfg = load_config(CONFIG_FILE)
    else:
        logging.info("Using embedded checklist config")
        cfg = config

    if not validate_config(cfg):
        raise SystemExit("Checklist config invalid — aborting")

    staging_dir = os.path.join(BASE_PATH, STAGING_DIR)
    if not os.path.isdir(staging_dir):
        logging.warning(f"Staging directory does not exist: {staging_dir}")
        return

    log_filename = f"/opt/mintcastiq_web/backend/mintcastiq/logs/ingest_{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    for fname in os.listdir(staging_dir):
        if fname.lower().endswith(".xlsx"):
            path = os.path.join(staging_dir, fname)
            logging.info(f"Processing workbook file {fname}")
            wb = openpyxl.load_workbook(path)
            result = ingest_workbook(wb, fname, cfg)
            out_name = os.path.splitext(path)[0] + ".json"
            with open(out_name, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Wrote {out_name} with {len(result['cards'])} cards and {len(result['parallels'])} parallels.")

if __name__ == '__main__':
    main()
