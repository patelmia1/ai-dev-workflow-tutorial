# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A course tutorial repo (see `README.md`) whose actual deliverable is a small Streamlit sales dashboard for a fictional retailer, ShopSmart. The dashboard itself is simple; the point of the repo is the workflow used to build it: PRD → `TASKS.md` milestones → design spec → implementation plan → test-driven implementation on a feature branch → commit/push → deploy. When asked to work on a `TASK-N`, follow that pipeline rather than improvising — see "Milestone-driven workflow" below.

## Commands

- Activate venv: `source venv/bin/activate` (plain `venv/`, no `uv`/`conda`)
- Install deps: `pip install -r requirements.txt`
- Run the app: `streamlit run app.py` (add `--server.headless true` when launching in the background/non-interactively — otherwise Streamlit's first-run prompt blocks on stdin)
- Run all tests: `pytest -v` (from the repo root)
- Run one test file: `pytest tests/test_calculations.py -v`
- Run a single test: `pytest tests/test_calculations.py::test_total_sales -v`

`pytest.ini` sets `pythonpath = .`. This is required, not optional boilerplate: `tests/` has no `__init__.py`, so without it bare `pytest` fails with `ModuleNotFoundError` on `calculations`/`charts` (pytest's default import mode won't add the repo root to `sys.path` on its own). `python -m pytest` doesn't need this since Python itself prepends the cwd — but the plan/spec docs and this project standardize on bare `pytest`.

## Architecture

Flat file layout at the repo root. Data flows one direction:

`calculations.load_sales_data` → aggregation functions in `calculations.py` → `charts.build_*_chart` → rendered via `st.plotly_chart` in `app.py`.

- `calculations.py` — pure aggregation functions over the sales DataFrame, no `st.*` calls, so testable without a Streamlit runtime.
- `charts.py` — pure Plotly figure builders, same no-`st.*` constraint, same reason.
- `app.py` — the only file that calls Streamlit; wires `calculations`/`charts` output into page layout and widgets. Data loading is wrapped in `@st.cache_data` so the CSV parses once per session.
- No custom CSV schema validation anywhere: malformed input surfaces as pandas' own exceptions (`FileNotFoundError`, `ParserError`) rather than a bespoke validation layer — a deliberate scope decision, not an oversight (see the design spec's "Error Handling" section).
- Dependencies are deliberately capped at `streamlit`, `pandas`, `plotly`, `pytest` (`requirements.txt`).

## Milestone-driven workflow

Work is tracked in `TASKS.md` as milestones `TASK-1`..`TASK-7`, organized into To Do / In Progress / Done sections. Each entry has acceptance-criteria checkboxes, a `Commit:` line, and a `Notes:` line. Definition of Done (from `TASKS.md`): acceptance criteria met, app runs locally with `streamlit run app.py`, changes committed with the milestone ID.

- Moving a task to "In Progress" and later to "Done" are each their own commit, kept separate from the implementation commit(s) — see `git log` for the established pattern, e.g. `TASK-3: mark in progress on the board` / `TASK-3: add KPI cards for total sales and orders` / `TASK-3: mark done on the board`.
- Every commit message includes its milestone ID.
- When a task is marked Done, `Commit:` points to the implementation commit (not the board-move commit), and `Notes:` records anything that deviated from the plan or was changed afterward — or `clean` if nothing did. Verify each acceptance criterion against actual output before checking it off; don't just trust the plan's example values.
- Some acceptance criteria are inherently visual/subjective (e.g. TASK-6's "professional appearance suitable for executive presentation," which is also literally in the PRD's own Acceptance Criteria list) and can't be confirmed from a terminal. Don't check those boxes yourself — leave the task in "In Progress," record in `Notes:` exactly which criteria need the user's own look and why, and only move it to Done after they confirm.
- The step-by-step instructions per milestone (including each step's expected command output) live in `docs/superpowers/plans/2026-09-21-sales-dashboard.md`. The architecture rationale lives in `docs/superpowers/specs/2026-09-21-sales-dashboard-design.md`. Both derive from `prd/ecommerce-analytics.md`.
- TASK-7 (deployment to Streamlit Community Cloud) is explicitly out of scope to execute from this repo's automated workflow — it's done manually by the user, from `main`, after the branch is reviewed and merged.

## Lessons

Rules distilled from `TASKS.md` `Notes:` lines — read before repeating the same mistake:

- Bare `pytest` needs `pythonpath = .` (via `pytest.ini`) to resolve top-level modules from `tests/`, since there's no `__init__.py` there. This isn't in the implementation plan's own commands — if a future plan step's `pytest` command mysteriously fails with `ModuleNotFoundError` for a module that clearly exists, check `pytest.ini` before assuming the code is broken. (From TASK-2.)
- The plan's UI widget choices (e.g. `st.radio` for the granularity control) are a starting point, not a fixed spec — the user changed it to `st.toggle` after TASK-4 was already marked Done. Don't assume `app.py` still matches what the plan or design spec describes; check the actual file. When re-verifying a "Done" task's acceptance criteria, confirm against current code, not the plan's original snippet. (From TASK-4.)
- The implementation plan's own expected-output numbers can be stale: its Task 6 step 1 says "13 total" tests, but summing what Tasks 2-5 actually specify gives 12 (`test_calculations.py` + `test_charts.py`). Trust the current test suite's real count over a plan doc's stated expectation. (From TASK-6.)

## Testing conventions

Every `calculations.py`/`charts.py` function was built test-first: a failing test asserting exact expected values from the PRD's sample dataset (e.g. Total Sales ≈ $116,500.21, Total Orders = 482, top category = Electronics, 4 regions: North/South/East/West), then the minimal implementation to pass it. Follow the same red-green pattern for new aggregation or chart functions.
