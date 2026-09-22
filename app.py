import streamlit as st

from calculations import load_sales_data, sales_trend, total_orders, total_sales
from charts import build_trend_chart

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", page_icon="📊")
st.title("ShopSmart Sales Dashboard")


@st.cache_data
def get_data():
    return load_sales_data(DATA_PATH)


df = get_data()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")

st.subheader("Sales Trend")
show_daily = st.toggle("Daily")
granularity = "daily" if show_daily else "monthly"
trend_df = sales_trend(df, granularity=granularity)
st.plotly_chart(build_trend_chart(trend_df, granularity), use_container_width=True)
