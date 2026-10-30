
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.forecasting import (
    ensure_artifacts,
    load_data_and_metrics,
    make_forecast,
)

# Page configuration
st.set_page_config(
    page_title="Supply Chain Forecasting",
    page_icon="📦",
    layout="wide",
)

# Header
st.title("📦 Supply Chain Demand Forecasting")
st.caption(
    "CODTECH AI Internship | CITS9598 | Datla Gnana Venkata Reddy"
)
st.warning(
    "Educational demonstration using synthetic data. "
    "Do not use these forecasts alone for real inventory decisions."
)

# Load data and evaluation metrics
with st.spinner("Preparing synthetic sales data and evaluation metrics..."):
    ensure_artifacts()

data, metrics = load_data_and_metrics()

# Product selection
product = st.selectbox(
    "Choose a product",
    sorted(data["product"].unique()),
)

# IMPORTANT: Define history before using it
history = (
    data[data["product"] == product]
    .sort_values("date")
    .copy()
    .reset_index(drop=True)
)

# Historical demand chart
st.subheader(f"Historical demand: {product}")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(
    history["date"],
    history["units_sold"],
    label="Historical sales",
)
ax.set_xlabel("Date")
ax.set_ylabel("Units sold")
ax.grid(True, alpha=0.25)
ax.legend()
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Generate the 30-day forecast
st.subheader("Forecast for the next 30 days")

values = make_forecast(history, horizon=30)

dates = pd.date_range(
    start=history["date"].max() + pd.Timedelta(days=1),
    periods=30,
    freq="D",
)

forecast = pd.DataFrame(
    {
        "date": dates,
        "forecast_units": values,
    }
)
forecast["forecast_units"] = forecast["forecast_units"].round(1)

# Forecast table
st.dataframe(
    forecast,
    use_container_width=True,
    hide_index=True,
)

# Historical sales versus forecast
fig, ax = plt.subplots(figsize=(10, 4))

recent = history.tail(60)

ax.plot(
    recent["date"],
    recent["units_sold"],
    label="Actual sales (last 60 days)",
)
ax.plot(
    forecast["date"],
    forecast["forecast_units"],
    label="Forecast (next 30 days)",
)

ax.set_xlabel("Date")
ax.set_ylabel("Units sold")
ax.grid(True, alpha=0.25)
ax.legend()
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Model evaluation
st.subheader("Baseline model evaluation")
st.caption(
    "Chronological holdout evaluation; metrics describe synthetic data only."
)

row = metrics[metrics["product"] == product].iloc[0]

a, b, c = st.columns(3)
a.metric("MAE", f"{row['mae']:.2f} units")
b.metric("RMSE", f"{row['rmse']:.2f} units")
c.metric("Test days", int(row["test_days"]))

st.dataframe(
    metrics,
    use_container_width=True,
    hide_index=True,
)

# Download forecast
st.download_button(
    label="Download 30-day forecast (CSV)",
    data=forecast.to_csv(index=False).encode("utf-8"),
    file_name=f"{product.lower().replace(' ', '_')}_forecast.csv",
    mime="text/csv",
)
