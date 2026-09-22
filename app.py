import streamlit as st

from calculations import (
    load_sales_data,
    sales_by_category,
    sales_by_region,
    sales_trend,
    total_orders,
    total_sales,
)
from charts import build_category_chart, build_region_chart, build_trend_chart

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", page_icon="📊")
st.title("ShopSmart Sales Dashboard")

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] {
        border-color: transparent !important;
        border-radius: 0.5rem;
        transition: border-color 0.2s ease;
    }
    div[data-testid="stVerticalBlock"]:hover {
        border-color: #d3d3d3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    return load_sales_data(DATA_PATH)


df = get_data()

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.metric("Total Sales", f"${total_sales(df):,.0f}")
with col2:
    with st.container(border=True):
        st.metric("Total Orders", f"{total_orders(df):,}")

st.subheader("Sales Trend")
with st.container(border=True):
    show_daily = st.toggle("Daily")
    granularity = "daily" if show_daily else "monthly"
    trend_df = sales_trend(df, granularity=granularity)
    st.plotly_chart(build_trend_chart(trend_df, granularity), use_container_width=True)

st.subheader("Breakdowns")
col3, col4 = st.columns(2)
with col3:
    with st.container(border=True):
        st.plotly_chart(build_category_chart(sales_by_category(df)), use_container_width=True)
with col4:
    with st.container(border=True):
        st.plotly_chart(build_region_chart(sales_by_region(df)), use_container_width=True)
