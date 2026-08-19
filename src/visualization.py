"""Reusable scientific plots saved to disk."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
    figure, axis = plt.subplots(figsize=(12, 5))
    ordered = frame.sort_values("created_date")
    axis.scatter(
        ordered["created_date"],
        ordered[column],
        s=10,
        alpha=0.25,
        color="#2f6690",
        edgecolors="none",
        label="Individual measurements",
    )
    axis.set(xlabel="Measurement date", ylabel=PARAMETERS[column], title=f"{PARAMETERS[column]} over time")
    axis.xaxis.set_major_locator(mdates.AutoDateLocator())
    axis.xaxis.set_major_formatter(mdates.ConciseDateFormatter(axis.xaxis.get_major_locator()))
    axis.grid(True, alpha=0.2)
    axis.legend(frameon=False)
    _save(figure, path)


def plot_time_series_summary(
    frame: pd.DataFrame,
    column: str,
    path: str | Path,
    frequency: str = "D",
) -> None:
    """Plot raw observations with a period summary and interquartile band.

    The summary improves readability for dense or repeated timestamps. It does
    not replace the raw observations and should be interpreted as aggregation.
    """
    ordered = frame[["created_date", column]].copy()
    ordered["created_date"] = pd.to_datetime(ordered["created_date"])
    ordered = ordered.dropna().set_index("created_date").sort_index()
    grouped = ordered[column].resample(frequency).agg(
        median="median",
        first_quartile=lambda values: values.quantile(0.25),
        third_quartile=lambda values: values.quantile(0.75),
    ).dropna(subset=["median"])

    figure, axis = plt.subplots(figsize=(12, 5.5))
    axis.scatter(
        ordered.index,
        ordered[column],
        s=8,
        alpha=0.12,
        color="#6c757d",
        edgecolors="none",
        label="Individual measurements",
    )
    axis.fill_between(
        grouped.index,
        grouped["first_quartile"],
        grouped["third_quartile"],
        color="#4c956c",
        alpha=0.22,
        label="Interquartile range",
    )
    axis.plot(
        grouped.index,
        grouped["median"],
        color="#1b4332",
        linewidth=2.2,
        marker="o",
        markersize=3.5,
        label="Period median",
    )
    frequency_labels = {"D": "daily", "W": "weekly", "h": "hourly"}
    summary_label = frequency_labels.get(frequency, f"{frequency}-period")
    axis.set(
        xlabel="Measurement date",
        ylabel=PARAMETERS[column],
        title=f"{PARAMETERS[column]} over time with {summary_label} summary",
    )
    axis.xaxis.set_major_locator(mdates.AutoDateLocator())
    axis.xaxis.set_major_formatter(mdates.ConciseDateFormatter(axis.xaxis.get_major_locator()))
    axis.grid(True, alpha=0.2)
    axis.legend(frameon=False, ncol=3, loc="upper left")
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
