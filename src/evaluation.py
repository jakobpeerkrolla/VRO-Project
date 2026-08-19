"""Regression metrics and model comparison helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def regression_metrics(actual: pd.Series, predicted: pd.Series) -> dict[str, float]:
    """Calculate MAE, MSE, RMSE, and R2."""
    return {
        "MAE": float(mean_absolute_error(actual, predicted)),
        "MSE": float(mean_squared_error(actual, predicted)),
        "RMSE": float(np.sqrt(mean_squared_error(actual, predicted))),
        "R2": float(r2_score(actual, predicted)),
    }


def compare_predictions(actual: pd.Series, predictions: dict[str, pd.Series]) -> pd.DataFrame:
    """Return one metric row per model."""
    return pd.DataFrame({name: regression_metrics(actual, values) for name, values in predictions.items()}).T


def strongest_correlations(frame: pd.DataFrame, target: str) -> pd.Series:
    """Rank measured-variable correlations with target; correlation is not causation."""
    return frame.select_dtypes(include="number").corr()[target].drop(target).abs().sort_values(ascending=False)
