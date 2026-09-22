# Tasks

This file tracks all work for the E-Commerce Analytics dashboard (ShopSmart Sales Dashboard).

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes committed with the milestone ID in the commit message

## To Do

## In Progress

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard so stakeholders can access it via a public URL.

Deployed URL: https://patelmia1-ai-dev-workflow-tutorial-app-tagmf8.streamlit.app/

- [x] App is deployed to Streamlit Community Cloud
- [ ] Public URL loads the dashboard without errors
- [ ] Deployed version matches the locally verified app from TASK-6

Commit:
Notes: The URL currently redirects to Streamlit's login wall (`share.streamlit.io/-/auth/app`) instead of loading the dashboard — the app's sharing setting looks to be private rather than public. In the app's Streamlit Community Cloud settings, switch sharing to public/"anyone can view" so it's reachable without a Streamlit account, per the PRD's NFR-5. Separately, TASK-6 itself is still In Progress, so "matches the locally verified app from TASK-6" can't be confirmed yet either.

### TASK-6: Testing and refinement
Verify the dashboard meets all Phase 1 acceptance criteria and polish the presentation.
- [ ] All acceptance criteria in the PRD are verified against the running app
- [x] Dashboard loads within 5 seconds and charts render within 2 seconds
- [ ] Layout and labels are clean enough for an executive presentation

Commit: ad24157
Notes: Full suite passes (12/12 — the plan's step 1 says "13 total" but summing the tests actually specified in Tasks 2-5 gives 12; that's a stale count in the plan doc, not a gap here). Load time confirmed fast (page responds in ~2ms locally) and no errors/warnings in the server log. Left unchecked: "all PRD acceptance criteria verified" and "professional appearance" both depend on visually inspecting the rendered charts/layout in a browser, which I can't do from here — please take a look at http://localhost:8501 and confirm before this moves to Done.

## Done

### TASK-1: Environment setup and project initialization
Set up the Python project structure and dependencies needed to build the dashboard.
- [x] `requirements.txt` includes streamlit, pandas, and plotly
- [x] `app.py` exists and runs with `streamlit run app.py` showing a placeholder page
- [x] Project structure matches the architecture in the PRD (e.g. `data/` for `sales-data.csv`)

Commit: 7fe8cc9
Notes: clean

### TASK-2: Data loading and basic structure
Load and validate the transaction data from `data/sales-data.csv`.
- [x] CSV loads into a Pandas DataFrame with correct column types (date, numeric, categorical)
- [x] Loading is wrapped in a reusable function/module, not inlined ad hoc
- [x] App shows no errors when the data loads

Commit: 4ead56c
Notes: Claude added `pytest.ini` (`pythonpath = .`), not called for in the plan — without it, the plain `pytest` command from the plan docs fails with `ModuleNotFoundError` since `tests/` has no `__init__.py` and pytest's default import mode won't add the repo root to `sys.path` on its own.

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders prominently at the top of the dashboard.
- [x] Total Sales is calculated as the sum of `total_amount` and formatted as currency (e.g. $116,500)
- [x] Total Orders is calculated as the count of transactions and formatted with separators
- [x] KPI values match expected output in the PRD (~$116,500 / 482 orders)

Commit: 803e1cb
Notes: clean

### TASK-4: Sales trend chart
Add a line chart showing sales over time.
- [x] Line chart plots sales amount on the Y-axis against time on the X-axis
- [x] Chart includes interactive tooltips showing exact values
- [x] Chart renders without errors using the loaded CSV data

Commit: fe26670
Notes: You changed the granularity control from a radio (as specced in the plan) to a toggle switch after this task was marked done.

### TASK-5: Category and region breakdowns
Add bar charts showing sales by product category and by region.
- [x] Category bar chart shows all 5 categories, sorted by sales value (highest to lowest)
- [x] Region bar chart shows all 4 regions, sorted by sales value (highest to lowest)
- [x] Both charts have interactive tooltips with exact values

Commit: 91eb17f
Notes: clean
