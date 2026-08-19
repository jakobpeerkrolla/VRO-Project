"""Leakage-aware time-series feature engineering."""

from __future__ import annotations

import pandas as pd


def create_time_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Add calendar features derived only from each observation timestamp."""
    result = frame.copy()
    dates = pd.to_datetime(result["created_date"])
    result["hour"] = dates.dt.hour
    result["day"] = dates.dt.day
    result["day_of_week"] = dates.dt.dayofweek
    result["month"] = dates.dt.month
    return result


def create_lag_features(frame: pd.DataFrame, lags: tuple[int, ...] = (1, 3, 6)) -> pd.DataFrame:
    """Add historical lags; lag units are observations, not assumed hours."""
    result = frame.sort_values("created_date", kind="stable").copy()
    columns = {"water_pH": "pH", "TDS": "TDS", "water_temp": "temperature"}
    for source, label in columns.items():
        for lag in lags:
            result[f"{label}_lag_{lag}"] = result[source].shift(lag)
    return result


def create_rolling_features(frame: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """Add past-only rolling statistics by shifting before rolling."""
    result = frame.sort_values("created_date", kind="stable").copy()
    for column in ["water_pH", "TDS", "water_temp"]:
        history = result[column].shift(1)
        result[f"{column}_rolling_mean_{window}"] = history.rolling(window).mean()
        result[f"{column}_rolling_std_{window}"] = history.rolling(window).std()
        result[f"{column}_rolling_min_{window}"] = history.rolling(window).min()
        result[f"{column}_rolling_max_{window}"] = history.rolling(window).max()
    return result


def build_features(frame: pd.DataFrame, lags: tuple[int, ...] = (1, 3, 6), rolling_window: int = 3) -> pd.DataFrame:
    """Build calendar, lag, and past-only rolling features."""
    result = create_time_features(frame)
    result = create_lag_features(result, lags)
    return create_rolling_features(result, rolling_window)
