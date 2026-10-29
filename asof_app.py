"""Run: uv run --with streamlit --with pandas --with requests python -m streamlit run asof_app.py"""
from datetime import date, datetime, timezone
from io import StringIO
import re

import pandas as pd
import requests
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


def parse_csv(response):
    response.raise_for_status()
    frame = pd.read_csv(StringIO(response.text), na_values=["."])
    if frame.shape[1] != 2:
        raise ValueError("FRED did not return a single-series CSV.")
    frame.columns = ["Date", "Value"]
    frame["Date"] = pd.to_datetime(frame["Date"], errors="raise")
    frame["Value"] = pd.to_numeric(frame["Value"], errors="raise")
    frame = frame.dropna(subset=["Value"]).set_index("Date").sort_index()
    if frame.empty:
        raise ValueError("No nonmissing observations are available.")
    if frame.index.has_duplicates:
        raise ValueError("The download contains duplicate observation dates.")
    return frame, datetime.now(timezone.utc).isoformat(timespec="seconds")


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id, download_day):
    """One public CSV request; daily key prevents yesterday's cache being reused."""
    return parse_csv(requests.get(
        "https://fred.stlouisfed.org/graph/fredgraph.csv",
        params={"id": series_id}, timeout=45))


@st.cache_data(ttl=3600, show_spinner=False)
def download_vintage(series_id, vintage_date, download_day):
    """One public ALFRED CSV request for the requested vintage."""
    return parse_csv(requests.get(
        "https://alfred.stlouisfed.org/graph/alfredgraph.csv",
        params={"id": series_id, "vintage_date": vintage_date}, timeout=45))


def comparison(series_id, current, vintage):
    last_then = vintage.index[-1]
    common = current.index.intersection(vintage.index)
    revised = int((current.loc[common, "Value"] != vintage.loc[common, "Value"]).sum())
    return {
        "Series": f"https://fred.stlouisfed.org/series/{series_id}",
        "Last date known then": last_then.date().isoformat(),
        "Value known then": float(vintage.iloc[-1]["Value"]),
        "Today's value for last date known then": (
            float(current.loc[last_then, "Value"]) if last_then in current.index else None
        ),
        "Last date today": current.index[-1].date().isoformat(),
        "Value today": float(current.iloc[-1]["Value"]),
        "Values after last date known then": int((current.index > last_then).sum()),
        "Revised values on shared dates": revised,
    }


def main():
    st.set_page_config(page_title="Interest rates: as known then", layout="wide")
    today = date.today()
    day_key = today.isoformat()
    st.title("Interest rates: as known then")
    st.caption(f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today ({day_key}); built with AI help, a learning demonstration, not investment advice.")
    selected = st.sidebar.multiselect(
        "Series", list(SERIES), default=list(SERIES),
        format_func=lambda sid: f"{sid} — {SERIES[sid]}")
    extra = st.sidebar.text_input("Add another FRED series ID", placeholder="For example: DGS2").strip().upper()
    start = st.sidebar.date_input("Start date", value=date(2020, 1, 1), min_value=date(1776, 1, 1), max_value=today)
    asof = st.sidebar.date_input("As known on", value=today, min_value=date(1776, 1, 1), max_value=today)
    if extra:
        if re.fullmatch(r"[A-Z0-9_]+", extra):
            if extra not in selected:
                selected.append(extra)
        else:
            st.sidebar.error("Enter a series ID using letters, numbers, or underscores.")
    st.caption("Charts show today's published values from the start date. Table counts use all nonmissing observations in the downloads; revisions compare only dates present in both downloads. Values use each series' native units and frequency.")
    rows = []
    downloads = []
    for sid in selected:
        st.subheader(f"{sid} — {SERIES.get(sid, 'Additional FRED series')}")
        current = None
        vintage = None
        with st.spinner(f"Downloading {sid}…"):
            try:
                current, timestamp = download_today(sid, day_key)
                downloads.append({"Series": sid, "Download": "FRED current", "Downloaded UTC": timestamp})
            except Exception as exc:
                st.error(f"{sid}: today's download failed: {exc}")
            try:
                vintage, timestamp = download_vintage(sid, asof.isoformat(), day_key)
                downloads.append({"Series": sid, "Download": f"ALFRED {asof}", "Downloaded UTC": timestamp})
            except Exception as exc:
                st.error(f"{sid}: as-known download failed: {exc}")
        if current is not None:
            visible = current.loc[pd.Timestamp(start):]
            if visible.empty:
                st.info("No current observations in the selected date range.")
            else:
                st.line_chart(visible, y="Value", x_label="Date measured", y_label="Published value")
        if vintage is not None:
            st.caption(f"Last date measured in data known on {asof}: {vintage.index[-1].date()}.")
        else:
            st.caption(f"Last date known on {asof}: unavailable.")
        if current is not None and vintage is not None:
            record = comparison(sid, current, vintage)
            rows.append(record)
        else:
            rows.append({"Series": f"https://fred.stlouisfed.org/series/{sid}", "Status": "Download unavailable; see series error above"})
    st.subheader("Current data versus the selected vintage")
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", column_config={
            "Series": st.column_config.LinkColumn("Series", display_text=r"https://fred\.stlouisfed\.org/series/(.*)")})
    else:
        st.info("Select a series to begin.")
    if downloads:
        with st.expander("Download timestamps"):
            st.dataframe(pd.DataFrame(downloads), hide_index=True)


if __name__ == "__main__":
    main()
