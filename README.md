# Supply Chain Forecasting — CODTECH AI Internship

**Intern ID:** CITS9608  
**Full Name:** Apeksha Mahadev Mundey
**No. of Weeks:** 4  
**Project Name:** Supply Chain Forecasting

## Scope
Educational demand forecasting dashboard that generates fictional daily sales for three products, plots historical demand, forecasts the next 30 days with a 14-day moving-average baseline, evaluates the baseline on a chronological 80/20 split, and allows CSV export.

**Important:** Data is synthetic. Forecasts are illustrative and must not be used alone for real procurement or inventory decisions.

## Features
- Synthetic daily demand data for three fictional products.
- Historical demand and forecast charts.
- 30-day forecast table and CSV download.
- MAE and RMSE metrics from a time-ordered holdout split.
- Streamlit user interface.

## Stack
Python, Pandas, NumPy, scikit-learn, Matplotlib, Streamlit, pytest.

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
```powershell
python -m streamlit run app.py
```
The app generates the dataset and metrics on first run. Open the localhost URL printed in the terminal.

## Tests
```powershell
python -m pytest -q
```
Tests cover data generation, forecast horizon, and metric structure; they do not prove real-world forecast accuracy.

## Methodology
1. Generate 540 days of synthetic sales with trend, weekly patterns, and random noise.
2. Split each product's timeline chronologically (80% historical training window, 20% test window).
3. Forecast the test period using the mean of the latest 14 training days.
4. Report MAE and RMSE.
5. Forecast the next 30 days using the same baseline.

## Screenshots
Save genuine screenshots in `screenshots/`: `homepage.png`, `forecast.png`, and `evaluation.png`. Do not fabricate outputs.

## Limitations
Synthetic data does not represent a real supply chain. The moving-average baseline may miss trend changes, promotions, holidays, lead times, and stockouts. Real use requires appropriate data and time-aware validation.

## Internship Metadata
- Intern ID: CITS9598
- Full Name: Apeksha Mahadev Mundey
- Duration: 4 weeks
