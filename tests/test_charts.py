from pathlib import Path

from calculations import load_sales_data, sales_by_category, sales_by_region, sales_trend
from charts import build_category_chart, build_region_chart, build_trend_chart

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sales-data.csv"


def test_build_trend_chart_monthly_plots_all_points():
    df = load_sales_data(DATA_PATH)
    trend = sales_trend(df, granularity="monthly")
    fig = build_trend_chart(trend, granularity="monthly")
    assert len(fig.data) == 1
    assert len(fig.data[0].x) == len(trend)


def test_build_category_chart_plots_all_categories():
    df = load_sales_data(DATA_PATH)
    category_df = sales_by_category(df)
    fig = build_category_chart(category_df)
    assert len(fig.data) == 1
    assert len(fig.data[0].x) == len(category_df)


def test_build_region_chart_plots_all_regions():
    df = load_sales_data(DATA_PATH)
    region_df = sales_by_region(df)
    fig = build_region_chart(region_df)
    assert len(fig.data) == 1
    assert len(fig.data[0].x) == len(region_df)
