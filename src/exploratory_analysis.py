"""Descriptive summaries for the measured variables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PARAMETERS = ["water_pH", "TDS", "water_temp"]


def descriptive_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics and missing-value counts."""
    summary = frame[PARAMETERS].describe().T
    summary["missing"] = frame[PARAMETERS].isna().sum()
    return summary


def save_descriptive_statistics(frame: pd.DataFrame, output_path: str | Path) -> None:
    """Save descriptive statistics as CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptive_statistics(frame).to_csv(path)
