"""Tests for chronological splitting and regression metrics."""

import pandas as pd

from src.evaluation import regression_metrics
from src.prediction import chronological_split


def test_chronological_split_does_not_shuffle():
    frame = pd.DataFrame({"value": range(10)})
    train, test = chronological_split(frame, test_size=0.2)
    assert train["value"].tolist() == list(range(8))
    assert test["value"].tolist() == [8, 9]


def test_regression_metrics():
    metrics = regression_metrics(pd.Series([1, 2, 3]), pd.Series([1, 3, 2]))
    assert metrics["MAE"] == 2 / 3
    assert metrics["RMSE"] > 0
    assert "R2" in metrics
