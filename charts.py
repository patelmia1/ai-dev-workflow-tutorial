import plotly.express as px


def build_trend_chart(trend_df, granularity):
    axis_label = "Day" if granularity == "daily" else "Month"
    fig = px.line(
        trend_df,
        x="period",
        y="total_amount",
        markers=True,
        labels={"period": axis_label, "total_amount": "Total Sales ($)"},
    )
    fig.update_traces(hovertemplate="%{x}<br>$%{y:,.2f}<extra></extra>")
    return fig


def build_category_chart(category_df):
    fig = px.bar(
        category_df,
        x="category",
        y="total_amount",
        labels={"category": "Category", "total_amount": "Total Sales ($)"},
    )
    fig.update_traces(hovertemplate="%{x}<br>$%{y:,.2f}<extra></extra>")
    return fig


def build_region_chart(region_df):
    fig = px.bar(
        region_df,
        x="region",
        y="total_amount",
        labels={"region": "Region", "total_amount": "Total Sales ($)"},
    )
    fig.update_traces(hovertemplate="%{x}<br>$%{y:,.2f}<extra></extra>")
    return fig
