# Lab 17: FRED / ALFRED as-of app

From this folder, run:

```powershell
uv run --with streamlit --with pandas --with requests python -m streamlit run asof_app.py
```

Streamlit opens a browser with four rate charts and a comparison table. The running session launched during development is at http://127.0.0.1:8503.

Each series uses one FRED current CSV request and one ALFRED vintage CSV request per uncached selection. Successful downloads are cached for one hour, with a daily cache key. A period (`.`) is missing, not zero. The chart start date affects charts; table endpoints and counts use the complete downloads. Shared-date numeric differences count as revisions; new observations are counted separately. Unknown IDs report per-series errors without stopping the remaining series.

The as-known date defaults to the computer's current date. ALFRED provides a date-level vintage, not an intraday release timestamp; a same-day trading decision still requires checking publication time. Some FRED series lack ALFRED vintage coverage and will report an error.

Live default-data results and the unknown-ID check are saved in `asof_results.md`. Four chart elements were verified with Streamlit AppTest. The default browser was opened through Windows; browser visual inspection was unavailable in this session.

The table also shows today's value for the last observation known then, so a revision to the same measured month can be distinguished from a newer observation. Run the requested historical acceptance probes with:

```powershell
uv run --with streamlit --with pandas --with requests python probe_asof.py
```

This checks the four rates at 5 October 2026 and PAYEMS at 15 January 2025 against the expected values, using the actual Streamlit controls and live downloads. Results are saved to `vintage_probe_results.md` after all assertions pass.
