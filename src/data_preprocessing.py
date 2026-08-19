"""Import, validate, and conservatively clean water-quality data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

EXPECTED_COLUMNS = ["id", "created_date", "water_pH", "TDS", "water_temp"]
NUMERIC_COLUMNS = ["id", "water_pH", "TDS", "water_temp"]


def load_data(path: str | Path) -> pd.DataFrame:
    """Read a CSV, validate its schema, parse dates, and sort chronologically."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    frame = pd.read_csv(csv_path)
    missing = sorted(set(EXPECTED_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")
    frame = frame[EXPECTED_COLUMNS].copy()
    frame["created_date"] = pd.to_datetime(frame["created_date"], errors="coerce")
    frame = frame.sort_values("created_date", kind="stable").reset_index(drop=True)
    print(frame.info())
    return frame


def validate_data(frame: pd.DataFrame) -> dict[str, Any]:
    """Return validation findings without deleting or altering observations."""
    missing = sorted(set(EXPECTED_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")
    numeric = frame[NUMERIC_COLUMNS].apply(pd.to_numeric, errors="coerce")
    outlier_flags = pd.DataFrame(index=frame.index)
    outlier_flags["water_pH_outlier_candidate"] = frame["water_pH"].notna() & ~frame["water_pH"].between(0, 14)
    outlier_flags["TDS_outlier_candidate"] = frame["TDS"].notna() & (frame["TDS"] < 0)
    outlier_flags["water_temp_outlier_candidate"] = frame["water_temp"].notna() & ~frame["water_temp"].between(-50, 100)
    return {
        "missing_values": frame[EXPECTED_COLUMNS].isna().sum().to_dict(),
        "duplicate_rows": int(frame.duplicated().sum()),
        "duplicate_ids": int(frame["id"].duplicated().sum()),
        "invalid_dates": int(pd.to_datetime(frame["created_date"], errors="coerce").isna().sum()),
        "invalid_numeric_values": int(numeric.isna().sum().sum()),
        "is_chronologically_sorted": bool(frame["created_date"].is_monotonic_increasing),
        "outlier_candidates": {column: int(values.sum()) for column, values in outlier_flags.items()},
        "outlier_flags": outlier_flags,
    }


def clean_data(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Conservatively clean structure while documenting every change.

    Invalid dates and exact duplicate rows cannot support a time-series record and
    are removed; numeric outlier candidates are retained and reported for review.
    """
    result = frame.copy()
    before = len(result)
    result["created_date"] = pd.to_datetime(result["created_date"], errors="coerce")
    result = result.drop_duplicates().dropna(subset=["created_date"])
    for column in ["id", "water_pH", "TDS", "water_temp"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result = result.sort_values("created_date", kind="stable").reset_index(drop=True)
    report = validate_data(result)
    report["rows_before"] = before
    report["rows_after"] = len(result)
    report["rows_removed"] = before - len(result)
    return result, report


def preprocess_file(input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Load, clean, save processed data, and return the validation report."""
    raw = load_data(input_path)
    cleaned, report = clean_data(raw)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(destination, index=False)
    return report
