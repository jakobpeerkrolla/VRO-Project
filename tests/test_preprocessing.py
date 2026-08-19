"""Tests for import, schema validation, and conservative cleaning."""

import pandas as pd
import pytest

from src.data_preprocessing import clean_data, load_data, validate_data


def test_load_data_parses_and_sorts(tmp_path):
    path = tmp_path / "water_quality.csv"
    pd.DataFrame({
        "id": [2, 1], "created_date": ["2026-01-02", "2026-01-01"],
        "water_pH": [7.1, 7.0], "TDS": [300, 290], "water_temp": [24, 23],
    }).to_csv(path, index=False)
    result = load_data(path)
    assert result["created_date"].is_monotonic_increasing
    assert pd.api.types.is_datetime64_any_dtype(result["created_date"])


def test_load_data_rejects_missing_columns(tmp_path):
    path = tmp_path / "water_quality.csv"
    pd.DataFrame({"id": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Missing expected columns"):
        load_data(path)


def test_validation_marks_outliers_without_removing_them():
    frame = pd.DataFrame({
        "id": [1], "created_date": pd.to_datetime(["2026-01-01"]),
        "water_pH": [15], "TDS": [-1], "water_temp": [101],
    })
    report = validate_data(frame)
    assert report["outlier_candidates"]["water_pH_outlier_candidate"] == 1
    assert report["outlier_candidates"]["TDS_outlier_candidate"] == 1


def test_clean_data_removes_exact_duplicates_only():
    frame = pd.DataFrame({
        "id": [1, 1], "created_date": ["2026-01-01", "2026-01-01"],
        "water_pH": [7.0, 7.0], "TDS": [300, 300], "water_temp": [24, 24],
    })
    result, report = clean_data(frame)
    assert len(result) == 1
    assert report["rows_removed"] == 1
