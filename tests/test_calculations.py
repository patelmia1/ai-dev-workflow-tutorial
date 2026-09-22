from pathlib import Path

from calculations import load_sales_data, total_orders, total_sales

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sales-data.csv"


def test_load_sales_data_returns_all_rows():
    df = load_sales_data(DATA_PATH)
    assert len(df) == 482


def test_load_sales_data_parses_date_column():
    df = load_sales_data(DATA_PATH)
    assert str(df["date"].dtype).startswith("datetime64")


def test_total_sales():
    df = load_sales_data(DATA_PATH)
    assert round(total_sales(df), 2) == 116500.21


def test_total_orders():
    df = load_sales_data(DATA_PATH)
    assert total_orders(df) == 482
