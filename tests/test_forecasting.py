from src.forecasting import generate_sales_data, moving_average_forecast, evaluate_baseline

def test_generated_data_structure():
    data=generate_sales_data(days=60,seed=1)
    assert len(data)==180
    assert {"date","product","units_sold"}.issubset(data.columns)
    assert data["product"].nunique() == 3
    assert (data.units_sold>=0).all()

def test_forecast_horizon():
    pred=moving_average_forecast([10,12,14,16],horizon=7,window=3)
    assert len(pred)==7
    assert all(x>=0 for x in pred)

def test_evaluation_metrics():
    metrics=evaluate_baseline(generate_sales_data(days=100,seed=2))
    assert len(metrics)==3
    assert {"product","mae","rmse","test_days"}.issubset(metrics.columns)
    assert (metrics.mae>=0).all() and (metrics.rmse>=0).all()
