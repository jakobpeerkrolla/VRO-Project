"""Time-indexed summaries without unsupported seasonal claims."""

from __future__ import annotations

import pandas as pd


def measurement_intervals(frame: pd.DataFrame) -> pd.Series:
    """Return intervals between consecutive measurements."""
    dates = pd.to_datetime(frame["created_date"]).sort_values()
    return dates.diff().dropna()


def temporal_summary(frame: pd.DataFrame) -> dict[str, object]:
    """Summarize coverage and measurement cadence for interpretation."""
    dates = pd.to_datetime(frame["created_date"]).sort_values()
    intervals = measurement_intervals(frame)
    return {
        "start": dates.min(),
        "end": dates.max(),
        "duration_days": (dates.max() - dates.min()).total_seconds() / 86400 if len(dates) else 0,
        "measurements": len(frame),
        "median_interval": intervals.median() if not intervals.empty else pd.NaT,
        "min_interval": intervals.min() if not intervals.empty else pd.NaT,
        "max_interval": intervals.max() if not intervals.empty else pd.NaT,
    }
