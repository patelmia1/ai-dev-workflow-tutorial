# ShopSmart Sales Dashboard — Design Spec

Date: 2026-09-21
Source PRD: `prd/ecommerce-analytics.md` (Phase 1 only)
Tracked milestones: `TASKS.md` (TASK-1 through TASK-7)

## Overview

A single-page Streamlit dashboard reading `data/sales-data.csv` and showing:
Total Sales / Total Orders KPIs, a sales trend line chart (daily/monthly
toggle), and category and region bar charts. Scope is strictly PRD Phase 1 —
no auth, no DB, no filtering, no export, no automated refresh.

## Architecture

Flat file layout at the repo root, no package/`src` nesting — the project is
three small modules plus tests, and the PRD's Phase 2 items are explicitly
out of scope, so there's nothing to leave room for.

```
app.py              # Streamlit page: layout, widgets, wiring
calculations.py      # CSV loading + all aggregations (pure functions)
charts.py            # Plotly figure builders (pure functions)
requirements.txt
venv/                # local virtualenv (gitignored)
tests/
  test_calculations.py
  test_charts.py
```

Data flows one direction: `calculations.load_sales_data` →
aggregation functions → `charts.build_*_chart` → `st.plotly_chart` in
`app.py`. Nothing downstream mutates the DataFrame in place.

## Components

### `calculations.py`

- `load_sales_data(path) -> pd.DataFrame` — `pd.read_csv` with `date` parsed
  as a date column. No custom schema/type validation: the sample dataset is
  known-clean, and Phase 1 explicitly favors simplicity. Malformed input
  surfaces as pandas' own exceptions (e.g. `FileNotFoundError`,
  `ParserError`) rather than a custom validation layer.
- `total_sales(df) -> float` — sum of `total_amount`.
- `total_orders(df) -> int` — row count (one row per order per the data spec).
- `sales_by_category(df) -> pd.DataFrame` — grouped sum of `total_amount` by
  `category`, sorted descending.
- `sales_by_region(df) -> pd.DataFrame` — grouped sum of `total_amount` by
  `region`, sorted descending.
- `sales_trend(df, granularity: Literal["daily", "monthly"]) -> pd.DataFrame`
  — grouped sum of `total_amount` by day or by calendar month, ascending by
  date. `granularity` is the parameter the UI toggle drives.

### `charts.py`

- `build_trend_chart(trend_df, granularity) -> go.Figure` — Plotly line
  chart, x=period, y=total_amount, hover shows exact value; axis label
  reflects the chosen granularity.
- `build_category_chart(category_df) -> go.Figure` — Plotly bar chart,
  already-sorted input rendered top-to-bottom/left-to-right as given.
- `build_region_chart(region_df) -> go.Figure` — same pattern as category.

Each function takes plain data in and returns a `Figure` out — no
Streamlit calls inside `charts.py`, so every function is callable and
assertable from a test without a Streamlit runtime.

### `app.py`

- `st.set_page_config(...)` with a page title (default Streamlit theme
  otherwise — no custom CSS, no custom Plotly color sequence).
- `load_sales_data` wrapped with `@st.cache_data` so the CSV is parsed once
  per session, keeping load time well under the PRD's 5-second budget.
- KPI row: `st.columns(2)` + `st.metric` for Total Sales (currency-formatted)
  and Total Orders (comma-formatted).
- Granularity control: `st.radio("Trend granularity", ["Monthly", "Daily"])`
  feeding `sales_trend(df, granularity)` → `build_trend_chart`.
- Category and region bar charts side by side via `st.columns(2)`.

## Error Handling

Minimal by design (per the validation-scope decision): no bespoke schema
checks. If the CSV is missing or malformed, the app surfaces Python's/pandas'
native exception in the Streamlit UI rather than a custom error message.
Acceptable because the CSV is a known, versioned sample file, not
user-uploaded input.

## Testing

- `tests/test_calculations.py`: exercises every aggregation function against
  `data/sales-data.csv` (or a small fixture), asserting the PRD's expected
  values — Total Sales ≈ $116,500, Total Orders = 482, top category =
  Electronics, four regions present.
- `tests/test_charts.py`: light assertions per chart function — correct
  `Figure` type, expected trace count, and that the number of plotted points
  matches the input rows (catches wiring bugs like an off-by-one or wrong
  column, not visual styling).
- Run via `pytest` from the project root inside the venv.

## Dependencies

`requirements.txt`: `streamlit`, `pandas`, `plotly`, `pytest`. Installed into
a plain `venv/` (`python -m venv venv`), no `uv`/`conda`.

## Out of Scope for This Plan

Deployment to Streamlit Community Cloud (PRD M7 / TASKS.md TASK-7) is
scoped but not executed by this plan — see the implementation plan for the
handoff.
