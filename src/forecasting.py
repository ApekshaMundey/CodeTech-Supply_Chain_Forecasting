from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_daily_sales.csv"
METRICS_PATH = ROOT / "artifacts" / "evaluation_metrics.csv"

def generate_sales_data(days=540, seed=42):
    """Generate fictional daily demand with trend, weekly patterns, and noise."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=days, freq="D")
    rows = []
    specs = {"Product A": (45, .025, 12), "Product B": (30, .010, 7), "Product C": (70, -.008, 16)}
    for product, (base, trend, amplitude) in specs.items():
        for i, date in enumerate(dates):
            weekly = amplitude * np.sin(2*np.pi*date.dayofweek/7)
            slow_cycle = 5*np.sin(2*np.pi*i/90)
            noise = rng.normal(0,5)
            units = max(0, int(round(base + trend*i + weekly + slow_cycle + noise)))
            rows.append({"date":date, "product":product, "units_sold":units})
    return pd.DataFrame(rows)

def moving_average_forecast(values, horizon=30, window=14):
    """Return a flat baseline using the mean of the latest observed window."""
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        raise ValueError("Cannot forecast from empty data.")
    return np.maximum(0, np.repeat(values[-min(window,len(values)):].mean(), horizon))

def make_forecast(history, horizon=30):
    return moving_average_forecast(history["units_sold"].to_numpy(), horizon=horizon)

def evaluate_baseline(data):
    rows=[]
    for product, group in data.groupby("product"):
        group=group.sort_values("date")
        split=int(len(group)*.8); train=group.iloc[:split]; test=group.iloc[split:]
        pred=moving_average_forecast(train.units_sold.to_numpy(), horizon=len(test), window=14)
        rows.append({"product":product, "mae":float(mean_absolute_error(test.units_sold,pred)),
                     "rmse":float(np.sqrt(mean_squared_error(test.units_sold,pred))), "test_days":len(test)})
    return pd.DataFrame(rows)

def ensure_artifacts():
    DATA_PATH.parent.mkdir(exist_ok=True); METRICS_PATH.parent.mkdir(exist_ok=True)
    if not DATA_PATH.exists(): generate_sales_data().to_csv(DATA_PATH,index=False)
    if not METRICS_PATH.exists():
        evaluate_baseline(pd.read_csv(DATA_PATH,parse_dates=["date"])).to_csv(METRICS_PATH,index=False)

def load_data_and_metrics():
    ensure_artifacts()
    return pd.read_csv(DATA_PATH,parse_dates=["date"]), pd.read_csv(METRICS_PATH)
