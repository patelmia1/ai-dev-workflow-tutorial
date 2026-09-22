# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ShopSmart Streamlit sales dashboard (KPIs, trend chart, category/region breakdowns) reading `data/sales-data.csv`, per PRD Phase 1.

**Architecture:** Three flat modules — `calculations.py` (pure aggregation functions), `charts.py` (pure Plotly figure builders, no Streamlit calls), `app.py` (Streamlit layout that wires the two together). Data flows one direction: load → aggregate → build chart → render.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly, pytest, plain `venv/`.

**Spec:** `docs/superpowers/specs/2026-09-21-sales-dashboard-design.md`

**Milestone tracking:** `TASKS.md` (TASK-1 .. TASK-7). Each task below is labeled with the milestone it fulfills. Plan task numbers (Task 1, Task 2, …) are this plan's own numbering and are independent of the TASK-N milestone IDs — don't conflate the two when discussing progress.

**Branch:** Work directly on the current branch (`feature/sales-dashboard`) — no worktree.

## Global Constraints

- Dependencies limited to: `streamlit`, `pandas`, `plotly`, `pytest` — installed into a plain `venv/` via `requirements.txt` (no `uv`, no `conda`).
- Flat file layout at repo root: `app.py`, `calculations.py`, `charts.py`, `requirements.txt`, `venv/`, `tests/`.
- `calculations.py` and `charts.py` contain only pure functions (no `st.*` calls) so both are testable without a Streamlit runtime.
- No custom CSV schema validation — rely on pandas' native exceptions (per spec's "Error Handling" section).
- Default Streamlit theme, no custom CSS, default Plotly color sequence.
- Every commit message includes its milestone ID (e.g. `TASK-2: ...`) per `TASKS.md`'s Definition of Done.
- Deployment (TASK-7) is explicitly out of scope for execution — the plan ends with a handoff, not a deploy.

---

### Task 1: Environment and Project Skeleton — Milestone: TASK-1

**Files:**
- Create: `requirements.txt`
- Create: `app.py`

**Interfaces:**
- Produces: a runnable `app.py` entrypoint later tasks will extend.

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`
Expected: a `venv/` directory appears (already covered by `.gitignore`).

- [ ] **Step 2: Write requirements.txt**

```
streamlit>=1.38
pandas>=2.2
plotly>=5.24
pytest>=8.3
```

- [ ] **Step 3: Activate the venv and install dependencies**

Run: `source venv/bin/activate && pip install -r requirements.txt`
Expected: all four packages install with no errors.

- [ ] **Step 4: Write a placeholder app.py**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", page_icon="📊")
st.title("ShopSmart Sales Dashboard")
st.write("Dashboard under construction.")
```

- [ ] **Step 5: Run the app to confirm the environment works**

Run: `streamlit run app.py`
Expected: browser opens showing the title and placeholder text, no errors in the terminal. Stop the server after confirming (Ctrl+C).

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: set up venv, requirements, and app skeleton"
```

---

### Task 2: Data Loading — Milestone: TASK-2

**Files:**
- Create: `calculations.py`
- Create: `tests/test_calculations.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: none (first calculations function).
- Produces: `load_sales_data(path) -> pd.DataFrame` with a parsed `date` column — every later calculations function takes this DataFrame as input.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_calculations.py
from pathlib import Path

from calculations import load_sales_data

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sales-data.csv"


def test_load_sales_data_returns_all_rows():
    df = load_sales_data(DATA_PATH)
    assert len(df) == 482


def test_load_sales_data_parses_date_column():
    df = load_sales_data(DATA_PATH)
    assert str(df["date"].dtype).startswith("datetime64")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'calculations'` (file doesn't exist yet).

- [ ] **Step 3: Implement load_sales_data**

```python
# calculations.py
import pandas as pd


def load_sales_data(path):
    return pd.read_csv(path, parse_dates=["date"])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 2 passed.

- [ ] **Step 5: Wire loading into app.py**

```python
# app.py
import streamlit as st

from calculations import load_sales_data

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", page_icon="📊")
st.title("ShopSmart Sales Dashboard")


@st.cache_data
def get_data():
    return load_sales_data(DATA_PATH)


df = get_data()
st.write(f"Loaded {len(df)} transactions.")
```

- [ ] **Step 6: Run the app to confirm data loads**

Run: `streamlit run app.py`
Expected: page shows "Loaded 482 transactions." with no errors.

- [ ] **Step 7: Commit**

```bash
git add calculations.py tests/test_calculations.py app.py
git commit -m "TASK-2: load sales data from CSV"
```

---

### Task 3: KPI Cards — Milestone: TASK-3

**Files:**
- Modify: `calculations.py`
- Modify: `tests/test_calculations.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data(path) -> pd.DataFrame` (Task 2).
- Produces: `total_sales(df) -> float`, `total_orders(df) -> int`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_calculations.py (add)
from calculations import load_sales_data, total_orders, total_sales


def test_total_sales():
    df = load_sales_data(DATA_PATH)
    assert round(total_sales(df), 2) == 116500.21


def test_total_orders():
    df = load_sales_data(DATA_PATH)
    assert total_orders(df) == 482
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL — `ImportError: cannot import name 'total_sales'`.

- [ ] **Step 3: Implement the aggregation functions**

```python
# calculations.py (add)
def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return len(df)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 4 passed.

- [ ] **Step 5: Add KPI cards to app.py**

```python
# app.py (replace the "Loaded N transactions" line with:)
from calculations import load_sales_data, total_orders, total_sales

# ... (get_data unchanged) ...

df = get_data()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")
```

- [ ] **Step 6: Run the app to confirm KPIs display**

Run: `streamlit run app.py`
Expected: two metric cards showing "Total Sales: $116,500" and "Total Orders: 482".

- [ ] **Step 7: Commit**

```bash
git add calculations.py tests/test_calculations.py app.py
git commit -m "TASK-3: add KPI cards for total sales and orders"
```

---

### Task 4: Sales Trend Chart — Milestone: TASK-4

**Files:**
- Modify: `calculations.py`
- Create: `charts.py`
- Create: `tests/test_charts.py`
- Modify: `tests/test_calculations.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data(path) -> pd.DataFrame` (Task 2).
- Produces: `sales_trend(df, granularity) -> pd.DataFrame` (columns: `period`, `total_amount`) and `charts.build_trend_chart(trend_df, granularity) -> plotly.graph_objects.Figure` — both consumed by app.py and by Task 5's tests as the pattern to follow.

- [ ] **Step 1: Write the failing calculations tests**

```python
# tests/test_calculations.py (add)
import pytest

from calculations import load_sales_data, sales_trend


def test_sales_trend_monthly_has_twelve_months():
    df = load_sales_data(DATA_PATH)
    trend = sales_trend(df, granularity="monthly")
    assert len(trend) == 12


def test_sales_trend_daily_matches_unique_dates():
    df = load_sales_data(DATA_PATH)
    trend = sales_trend(df, granularity="daily")
    assert len(trend) == 241


def test_sales_trend_invalid_granularity_raises():
    df = load_sales_data(DATA_PATH)
    with pytest.raises(ValueError):
        sales_trend(df, granularity="yearly")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL — `ImportError: cannot import name 'sales_trend'`.

- [ ] **Step 3: Implement sales_trend**

```python
# calculations.py (add)
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 7 passed.

- [ ] **Step 5: Write the failing chart test**

```python
# tests/test_charts.py
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
```

- [ ] **Step 6: Run test to verify it fails**

Run: `pytest tests/test_charts.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'charts'`.

- [ ] **Step 7: Implement build_trend_chart**

```python
# charts.py
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
```

- [ ] **Step 8: Run test to verify it passes**

Run: `pytest tests/test_charts.py -v`
Expected: 1 passed.

- [ ] **Step 9: Add the granularity toggle and trend chart to app.py**

```python
# app.py (add, after the KPI columns)
from calculations import load_sales_data, sales_trend, total_orders, total_sales
from charts import build_trend_chart

# ... (get_data, df, KPI columns unchanged) ...

st.subheader("Sales Trend")
granularity_label = st.radio("Granularity", ["Monthly", "Daily"], horizontal=True)
granularity = "monthly" if granularity_label == "Monthly" else "daily"
trend_df = sales_trend(df, granularity=granularity)
st.plotly_chart(build_trend_chart(trend_df, granularity), use_container_width=True)
```

- [ ] **Step 10: Run the app to confirm the chart and toggle work**

Run: `streamlit run app.py`
Expected: a line chart appears below the KPIs; switching the radio button between Monthly/Daily changes the chart's granularity with no errors.

- [ ] **Step 11: Commit**

```bash
git add calculations.py charts.py tests/test_calculations.py tests/test_charts.py app.py
git commit -m "TASK-4: add sales trend chart with granularity toggle"
```

---

### Task 5: Category and Region Breakdowns — Milestone: TASK-5

**Files:**
- Modify: `calculations.py`
- Modify: `charts.py`
- Modify: `tests/test_calculations.py`
- Modify: `tests/test_charts.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data(path) -> pd.DataFrame` (Task 2).
- Produces: `sales_by_category(df) -> pd.DataFrame` (columns: `category`, `total_amount`, sorted descending), `sales_by_region(df) -> pd.DataFrame` (columns: `region`, `total_amount`, sorted descending), `charts.build_category_chart(category_df) -> Figure`, `charts.build_region_chart(region_df) -> Figure`.

- [ ] **Step 1: Write the failing calculations tests**

```python
# tests/test_calculations.py (add)
from calculations import load_sales_data, sales_by_category, sales_by_region


def test_sales_by_category_sorted_descending_with_top_electronics():
    df = load_sales_data(DATA_PATH)
    result = sales_by_category(df)
    assert result.iloc[0]["category"] == "Electronics"
    assert round(result.iloc[0]["total_amount"], 2) == 42683.67
    amounts = list(result["total_amount"])
    assert amounts == sorted(amounts, reverse=True)


def test_sales_by_region_has_four_regions_sorted_descending():
    df = load_sales_data(DATA_PATH)
    result = sales_by_region(df)
    assert set(result["region"]) == {"North", "South", "East", "West"}
    assert result.iloc[0]["region"] == "North"
    amounts = list(result["total_amount"])
    assert amounts == sorted(amounts, reverse=True)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL — `ImportError: cannot import name 'sales_by_category'`.

- [ ] **Step 3: Implement the aggregation functions**

```python
# calculations.py (add)
def sales_by_category(df):
    grouped = df.groupby("category")["total_amount"].sum()
    return grouped.sort_values(ascending=False).reset_index()


def sales_by_region(df):
    grouped = df.groupby("region")["total_amount"].sum()
    return grouped.sort_values(ascending=False).reset_index()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 9 passed.

- [ ] **Step 5: Write the failing chart tests**

```python
# tests/test_charts.py (add)
from calculations import sales_by_category, sales_by_region
from charts import build_category_chart, build_region_chart


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
```

- [ ] **Step 6: Run tests to verify they fail**

Run: `pytest tests/test_charts.py -v`
Expected: FAIL — `ImportError: cannot import name 'build_category_chart'`.

- [ ] **Step 7: Implement the chart builders**

```python
# charts.py (add)
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
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `pytest tests/test_charts.py -v`
Expected: 3 passed.

- [ ] **Step 9: Add the breakdown charts to app.py**

```python
# app.py (add, after the trend chart)
from calculations import (
    load_sales_data,
    sales_by_category,
    sales_by_region,
    sales_trend,
    total_orders,
    total_sales,
)
from charts import build_category_chart, build_region_chart, build_trend_chart

# ... (existing code unchanged) ...

st.subheader("Breakdowns")
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(build_category_chart(sales_by_category(df)), use_container_width=True)
with col4:
    st.plotly_chart(build_region_chart(sales_by_region(df)), use_container_width=True)
```

- [ ] **Step 10: Run the app to confirm both charts display**

Run: `streamlit run app.py`
Expected: two bar charts side by side, each showing all categories/regions sorted highest to lowest, with hover tooltips.

- [ ] **Step 11: Commit**

```bash
git add calculations.py charts.py tests/test_calculations.py tests/test_charts.py app.py
git commit -m "TASK-5: add category and region breakdown charts"
```

---

### Task 6: Testing and Refinement — Milestone: TASK-6

**Files:**
- Modify: `calculations.py` (comments only, if needed)
- Modify: `charts.py` (comments only, if needed)
- No new functions — this task verifies and polishes, it doesn't add features.

**Interfaces:**
- Consumes: the full app built in Tasks 1-5.
- Produces: nothing new; confirms the PRD's Acceptance Criteria are met.

- [ ] **Step 1: Run the full test suite**

Run: `pytest -v`
Expected: all tests pass (13 total across `test_calculations.py` and `test_charts.py`).

- [ ] **Step 2: Manually verify each PRD acceptance criterion**

Run: `streamlit run app.py` and check against `prd/ecommerce-analytics.md`'s Acceptance Criteria section:
- Total Sales and Total Orders are displayed prominently
- Trend chart shows sales over time and responds to the granularity toggle
- Category chart is sorted highest to lowest and shows all 5 categories
- Region chart is sorted highest to lowest and shows all 4 regions
- No errors or warnings appear in the terminal or browser
- The page loads in well under 5 seconds

- [ ] **Step 3: Add a one-line module comment to calculations.py and charts.py**

```python
# calculations.py (top of file, above the import)
"""Pure aggregation functions over the sales DataFrame — no Streamlit calls here."""
```

```python
# charts.py (top of file, above the import)
"""Pure Plotly figure builders — no Streamlit calls here."""
```

- [ ] **Step 4: Commit**

```bash
git add calculations.py charts.py
git commit -m "TASK-6: verify acceptance criteria and add module docstrings"
```

---

### Task 7: Deployment — Milestone: TASK-7 (hand off, do not execute)

This task is **not executed as part of this plan**. Per the project's ground rules, deployment to Streamlit Community Cloud is done by the user, manually, from `main`, after this branch is reviewed and merged.

Whoever executes this plan (subagent or inline session) should stop after Task 6 and report the branch as ready for review/merge — do not push, open a PR, or attempt deployment.

For reference, when you (the user) are ready:
1. Merge `feature/sales-dashboard` into `main`.
2. From Streamlit Community Cloud, connect the repo and point it at `app.py` on `main`.
3. Confirm the public URL loads and matches what you verified locally in Task 6.
4. Fill in the `Commit:` line for TASK-7 in `TASKS.md` and move it to Done.
