"""Tests for leakage-aware features."""

import pandas as pd

from src.feature_engineering import build_features


def test_features_use_previous_observations():
    frame = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "created_date": pd.date_range("2026-01-01", periods=4, freq="h"),
        "water_pH": [7.0, 7.1, 7.2, 7.3],
        "TDS": [300, 301, 302, 303],
        "water_temp": [24, 24, 25, 25],
    })
    result = build_features(frame, lags=(1,), rolling_window=2)
    assert pd.isna(result.loc[0, "pH_lag_1"])
    assert result.loc[1, "pH_lag_1"] == 7.0
    assert pd.isna(result.loc[1, "water_pH_rolling_mean_2"])
    assert result.loc[2, "water_pH_rolling_mean_2"] == 7.05
