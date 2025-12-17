def validate_configs(configs: list[dict], names: list[str]) -> bool:
    """
    Validate a list of ingest configs.
    Each config is validated independently.
    Returns True only if ALL configs pass.
    """
    assert len(configs) == len(names), "configs and names must align"

    overall_errors = False

    for config, name in zip(configs, names):
        logging.info(f"=== Validating config file: {name} ===")
        if not validate_single_config(config, name):
            overall_errors = True

    if overall_errors:
        logging.error("One or more config files FAILED validation")
    else:
        logging.info("All config files PASSED validation")

    return not overall_errors


def validate_single_config(config: dict, config_name: str) -> bool:
    """
    Validate a single ingest config dict.
    This is your original logic, refactored for clarity.
    """
    errors_found = False

    for checklist_name, checklist in config.items():
        meta = checklist.get("meta", {})
        column_sets = checklist.get("column_sets", {})
        sheets = checklist.get("sheets", {})

        logging.info(f"Validating checklist: {checklist_name} (from {config_name})")

        for sheet_idx, sheet in sheets.items():
            sheet_name = sheet.get("name", f"Sheet{sheet_idx}")
            columns = sheet.get("columns")

            # Resolve alias → dict
            if isinstance(columns, str):
                if columns in column_sets:
                    resolved = column_sets[columns].copy()
                else:
                    logging.error(
                        f"[{config_name}:{checklist_name}:{sheet_name}] "
                        f"Unknown column alias '{columns}'"
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
                        f"[{config_name}:{checklist_name}:{sheet_name}] "
                        f"Gap declared but column present at index {gap}"
                    )
                    errors_found = True
                else:
                    logging.info(
                        f"[{config_name}:{checklist_name}:{sheet_name}] "
                        f"Index {gap} intentionally blank"
                    )

            # Determine mapping shape
            if (
                isinstance(resolved, dict)
                and resolved
                and all(isinstance(k, int) for k in resolved.keys())
                and all(isinstance(v, str) for v in resolved.values())
            ):
                mapping_iter = [("default", resolved)]
            else:
                mapping_iter = resolved.items()

            # Validate mapping
            for section, mapping in mapping_iter:
                if not isinstance(mapping, dict):
                    logging.error(
                        f"[{config_name}:{checklist_name}:{sheet_name}] "
                        f"Section '{section}' must be a dict"
                    )
                    errors_found = True
                    continue

                for idx, name in mapping.items():
                    if not isinstance(idx, int):
                        logging.error(
                            f"[{config_name}:{checklist_name}:{sheet_name}] "
                            f"Non-integer column index '{idx}' in section '{section}'"
                        )
                        errors_found = True
                    elif not isinstance(name, str):
                        logging.error(
                            f"[{config_name}:{checklist_name}:{sheet_name}] "
                            f"Non-string column name at index {idx} in section '{section}': {name}"
                        )
                        errors_found = True
                    else:
                        logging.debug(
                            f"[{config_name}:{checklist_name}:{sheet_name}] "
                            f"Section '{section}' Column {idx} = {name} OK"
                        )

    if errors_found:
        logging.error(f"Config '{config_name}' FAILED validation")
    else:
        logging.info(f"Config '{config_name}' PASSED validation")

    return not errors_found