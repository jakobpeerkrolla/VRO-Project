"""Reusable scientific plots saved to disk."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PARAMETERS = {"water_pH": "pH", "TDS": "TDS (ppm)", "water_temp": "Water temperature (C)"}


def _save(figure: plt.Figure, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(destination, dpi=300, bbox_inches="tight")
    plt.close(figure)


def plot_time_series(frame: pd.DataFrame, column: str, path: str | Path) -> None:
    """Plot one measured parameter over time."""
    figure, axis = plt.subplots(figsize=(10, 5))
    axis.plot(frame["created_date"], frame[column], marker=".", linewidth=1)
    axis.set(xlabel="Measurement date", ylabel=PARAMETERS[column], title=f"{PARAMETERS[column]} over time")
    _save(figure, path)


def plot_distributions(frame: pd.DataFrame, directory: str | Path) -> None:
    """Save one histogram per measured parameter."""
    for column, label in PARAMETERS.items():
        figure, axis = plt.subplots(figsize=(7, 4))
        sns.histplot(frame[column].dropna(), kde=True, ax=axis)
        axis.set(xlabel=label, ylabel="Count", title=f"Distribution of {label}")
        _save(figure, Path(directory) / f"distribution_{column}.png")


def plot_correlation_heatmap(frame: pd.DataFrame, path: str | Path) -> None:
    """Save a correlation heatmap; correlations do not establish causality."""
    figure, axis = plt.subplots(figsize=(7, 5))
    sns.heatmap(frame[list(PARAMETERS)].corr(), annot=True, cmap="vlag", center=0, ax=axis)
    axis.set_title("Correlation matrix of measured parameters")
    _save(figure, path)


def plot_actual_vs_predicted(actual: pd.Series, predicted: pd.Series, model_name: str, path: str | Path) -> None:
    """Save an actual-versus-predicted diagnostic plot."""
    figure, axis = plt.subplots(figsize=(6, 6))
    axis.scatter(actual, predicted, alpha=0.7)
    axis.set(xlabel="Actual", ylabel="Predicted", title=f"Actual vs predicted: {model_name}")
    _save(figure, path)
