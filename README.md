# Analysis and Prediction of Water Quality in Aquaponic Fish Ponds using Python

## Scientific Question

This project provides a reproducible pipeline for describing and cautiously predicting measured water quality parameters in an aquaponic fish pond. The specific research question and all interpretations must be adapted to the actual measurement period, measurement frequency, and data quality.

## Available variables

The pipeline excluisly uses:

- `id`: Identification number
- `created_date`: Date and time of measurement
- `water_pH`: pH-Value
- `TDS`: Total Dissolved Solids in ppm
- `water_temp`: Watertemperature in Grad Celsius

No values for ammonia, nitrite, nitrate, dissolved oxygen, EC, turbidity, or other unmeasured parameters are generated or interpreted. External reference or optimal ranges may only be added after conducting a literature review.

## Structure

- `data/raw/`: Original-CSV; never overwriten 
- `data/processed/`: cleaned data
- `notebooks/`: Step-by-step analysis workspaces
- `src/`: reusable Python-Modules
- `models/`: saved Modelles
- `results/figures/`, `results/tables/`, `results/predictions/`: generated results
- `tests/`: Unit-Tests for core results
- `config/config.yaml`: Central paths, target variable, and model parameters

## Installation

Python 3.10 or newer is required

```bash
cd aquaponic-water-quality
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Interpretation

MAE, MSE, RMSE, and R2 are provided as measures of prediction performance. Correlation describes a statistical association, while feature importance describes the contribution within a specific model; neither proves causality. Results must not be generalized to unmeasured water parameters. No seasonal conclusions should be drawn when the temporal coverage is short.

## Limitations

The validity of the results is limited by the three available parameters, measurement quality, potential gaps, temporal resolution, and the length of the observation period. A machine learning model can describe relationships within these measurement data, but it does not replace a controlled study design or external biological and water chemistry literature.
