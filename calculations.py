import pandas as pd


def load_sales_data(path):
    return pd.read_csv(path, parse_dates=["date"])


def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return len(df)


def sales_trend(df, granularity="monthly"):
    if granularity == "monthly":
        period = df["date"].dt.to_period("M").dt.to_timestamp()
    elif granularity == "daily":
        period = df["date"].dt.normalize()
    else:
        raise ValueError(f"Unknown granularity: {granularity!r}")

    trend = df.groupby(period)["total_amount"].sum().reset_index()
    trend.columns = ["period", "total_amount"]
    return trend.sort_values("period").reset_index(drop=True)


def sales_by_category(df):
    grouped = df.groupby("category")["total_amount"].sum()
    return grouped.sort_values(ascending=False).reset_index()


def sales_by_region(df):
    grouped = df.groupby("region")["total_amount"].sum()
    return grouped.sort_values(ascending=False).reset_index()
