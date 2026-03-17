# Rider Fraud Alert Prioritization Dashboard

MVP product-ops dashboard for rider fraud triage using Python, SQL, HTML, and CSS.

**Live demo:** [https://moeedfarrukh.github.io/rider-fraud-alert-dashboard/](https://moeedfarrukh.github.io/rider-fraud-alert-dashboard/)

**Product strategy & roadmap:** [PRODUCT_STRATEGY_AND_ROADMAP.md](PRODUCT_STRATEGY_AND_ROADMAP.md)

## What this app does

- Generates synthetic rider, trip, payment, login, and refund data
- Computes rider-level fraud risk and estimated financial loss
- Prioritizes fraud alerts using `priority_score = risk_score * estimated_loss`
- Provides analyst workflow to review and action alerts (`allow`, `monitor`, `temporary_block`, `escalate`)
- Tracks analyst decisions in an action log page

## Tech stack

- Python + Flask backend
- SQLite database (SQL schema in `data/schema.sql`)
- Server-rendered HTML templates + CSS

## Run locally

1. Open terminal in project folder:
   - `cd rider-fraud-alert-dashboard`
2. Create and activate virtual environment (optional but recommended):
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Run app:
   - `python app.py`
5. Open:
   - [http://127.0.0.1:5000](http://127.0.0.1:5000)

On first run, database is auto-created and seeded.

## Main routes

- `/` Alert queue with filters and action forms
- `/rider/<rider_id>` Rider details with evidence and history
- `/actions` Analyst action history

## Static Live Server demo

If you want to demo without Python, use the static version in `static-demo`:

1. Open `static-demo/index.html` in VS Code / Cursor
2. Right click -> Open with Live Server
3. Use these pages:
   - `index.html` (alert queue)
   - `rider.html?rider_id=12` (rider details example)
   - `actions.html` (saved analyst actions)

Notes:
- This demo uses hardcoded sample data.
- Queue actions are saved in browser `localStorage`.
- Use the `Reset Demo` button on `index.html` to restore defaults.

## Deploy to GitHub Pages

The `docs/` folder contains the static demo configured for GitHub Pages:

1. Push your repo to GitHub.
2. Go to **Settings** → **Pages**.
3. Under **Build and deployment** → **Source**, select **Deploy from a branch**.
4. Choose your default branch (e.g. `main`) and set **Folder** to `/docs`.
5. Click **Save**. The dashboard will be live at `https://<username>.github.io/rider-fraud-alert-dashboard/`.

GitHub Pages serves only static files (no Python/Flask). The `docs/` version uses the same UI with client-side JavaScript and `localStorage`.

## PM metrics you can derive from this dataset

- Alert precision proxy at top-risk percentile
- False positive rate by fraud type or threshold
- Mean time to decision (MTTD)
- Estimated fraud loss prevented
- Analyst throughput (actions/day)
