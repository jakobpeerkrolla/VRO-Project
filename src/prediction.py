"""Chronological regression workflows for any measured target."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit


def chronological_split(frame: pd.DataFrame, test_size: float = 0.2) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split without shuffling, preserving the future holdout."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    split_index = int(len(frame) * (1 - test_size))
    if split_index < 1 or split_index >= len(frame):
        raise ValueError("Not enough rows for the requested split")
    return frame.iloc[:split_index].copy(), frame.iloc[split_index:].copy()


def build_models(random_state: int = 42) -> dict[str, Any]:
    """Create reproducible baseline ML regressors."""
    return {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(n_estimators=200, random_state=random_state, n_jobs=-1),
        "gradient_boosting": GradientBoostingRegressor(random_state=random_state),
    }


def last_observation_baseline(train_target: pd.Series, test_target: pd.Series) -> pd.Series:
    """Predict every future point with the last observed training value."""
    if train_target.empty:
        raise ValueError("Training target cannot be empty")
    return pd.Series(train_target.iloc[-1], index=test_target.index, name=test_target.name)


def prepare_xy(frame: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series]:
    """Drop identifiers and rows lacking target/features for model fitting."""
    if target not in ["water_pH", "TDS", "water_temp"]:
        raise ValueError("target must be water_pH, TDS, or water_temp")
    numeric = frame.select_dtypes(include="number").drop(columns=["id"], errors="ignore")
    clean = numeric.dropna(subset=[target]).dropna()
    return clean.drop(columns=[target]), clean[target]


def save_model(model: Any, path: str | Path) -> None:
    """Persist a fitted model."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, destination)


def time_series_cv(frame: pd.DataFrame, target: str, splits: int = 5) -> TimeSeriesSplit:
    """Return a chronological cross-validation splitter for later model tuning."""
    prepare_xy(frame, target)
    return TimeSeriesSplit(n_splits=splits)
