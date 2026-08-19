# Analysis and Prediction of Water Quality in Aquaponic Fish Ponds using Python

## Wissenschaftliche Fragestellung

Dieses Projekt stellt eine reproduzierbare Pipeline zur Beschreibung und vorsichtigen Vorhersage der gemessenen Wasserqualitaetsparameter in einem aquaponischen Fischteich bereit. Die konkrete Forschungsfrage und alle Interpretationen muessen an den tatsaechlichen Messzeitraum, die Messfrequenz und die Datenqualitaet angepasst werden.

## Verfuegbare Variablen

Die Pipeline verwendet ausschliesslich:

- `id`: Identifikationsnummer
- `created_date`: Datum und Uhrzeit der Messung
- `water_pH`: pH-Wert
- `TDS`: Total Dissolved Solids in ppm
- `water_temp`: Wassertemperatur in Grad Celsius

Es werden keine Werte fuer Ammonia, Nitrite, Nitrate, Dissolved Oxygen, EC, Turbidity oder andere nicht gemessene Parameter erzeugt oder interpretiert. Externe Grenz- oder Optimalbereiche duerfen erst nach Literaturrecherche als externe Referenzen ergaenzt werden.

## Struktur

- `data/raw/`: Original-CSV; wird nie ueberschrieben
- `data/processed/`: bereinigte, dokumentierte Daten
- `notebooks/`: schrittweise Analyse-Arbeitsflaechen
- `src/`: wiederverwendbare Python-Module
- `models/`: gespeicherte Modelle
- `results/figures/`, `results/tables/`, `results/predictions/`: erzeugte Ergebnisse
- `tests/`: Unit-Tests fuer Kernfunktionen
- `config/config.yaml`: zentrale Pfade, Target-Variable und Modellparameter

## Installation

Voraussetzung ist Python 3.10 oder neuer.

```bash
cd aquaponic-water-quality
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## CSV einlegen

Lege die echte Datei unter `data/raw/water_quality.csv` ab. Die Kopfzeile muss mindestens genau diese Spalten enthalten:

```text
id,created_date,water_pH,TDS,water_temp
```

Die Rohdaten werden nicht veraendert. Ungueltige Datumswerte und exakte doppelte Zeilen werden in der Bereinigung dokumentiert und entfernt; potenzielle Messausreisser werden nur markiert und bleiben zunaechst erhalten.

## Ausfuehrung

Vom Projektstamm aus:

```bash
python main.py
pytest
jupyter notebook notebooks/01_data_overview.ipynb
```

`main.py` importiert und bereinigt die CSV nach `data/processed/water_quality_clean.csv`. Danach sollten die Notebooks der Reihe nach ausgefuehrt werden:

1. Datenueberblick und Validierung
2. EDA und deskriptive Statistik
3. Zeitreihen und Messintervalle
4. Leakage-freies Feature Engineering
5. Chronologischer Modellvergleich

Das Target wird in `config/config.yaml` mit `target.variable` auf `water_pH`, `TDS` oder `water_temp` gesetzt. Die Modellierung muss mit einem chronologischen Split erfolgen; ein zufaelliges Mischen kann Zukunftsinformationen in das Training bringen und die Testleistung unzulaessig optimistisch machen. `TimeSeriesSplit` steht fuer spaetere Cross-Validation bereit.

## Interpretation

MAE, MSE, RMSE und R2 werden als Messgroessen der Vorhersageleistung bereitgestellt. Korrelation beschreibt einen statistischen Zusammenhang, Feature Importance beschreibt den Beitrag innerhalb eines konkreten Modells; beides beweist keine Kausalitaet. Ergebnisse duerfen nicht auf nicht gemessene Wasserparameter uebertragen werden. Bei kurzer zeitlicher Abdeckung werden keine saisonalen Aussagen gemacht.

## Grenzen

Die Aussagekraft ist durch die drei vorhandenen Parameter, die Messqualitaet, eventuelle Luecken, die zeitliche Aufloesung und die Laenge des Beobachtungszeitraums begrenzt. Ein Machine-Learning-Modell kann Zusammenhaenge in diesen Messdaten beschreiben, ersetzt aber weder ein kontrolliertes Studiendesign noch externe biologische oder wasserchemische Literatur.
