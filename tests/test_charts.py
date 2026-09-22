from pathlib import Path

from calculations import load_sales_data, sales_trend
from charts import build_trend_chart

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sales-data.csv"


def test_build_trend_chart_monthly_plots_all_points():
    df = load_sales_data(DATA_PATH)
    trend = sales_trend(df, granularity="monthly")
    fig = build_trend_chart(trend, granularity="monthly")
    assert len(fig.data) == 1
    assert len(fig.data[0].x) == len(trend)
