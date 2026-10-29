# Project 2: admit, quarantine, or reject

Assessment date: **29 October 2026**. The Lab 15 universe is **SGOV, VGIT, VCIT, and ACWI**. These are four candidate funds, not four positive portfolio weights: Lab 15's full-window result was 65% SGOV / 35% ACWI, and its recent-window result was 85% SGOV / 15% ACWI. VGIT and VCIT received zero weight in those searches.

## Decision on the Lab 17 series

**DGS10 — Admit as an optional interest-rate context series, using the ALFRED vintage available on each decision date.** The September 30, 2026 vintage ends September 29 at 5.26%; today's October 29 vintage ends October 28 at 5.05%. Twenty observations available today were not yet published in the September 30 snapshot, and zero shared observations changed. This daily market rate shows almost no lag (about one business day here) and no revisions in this comparison. It is a percent-per-year Treasury yield, not the return of any of our four funds. **Reject its use as a replacement for SGOV, VGIT, VCIT, or ACWI total returns, or as a cash return obtained by dividing its annual yield by 12.**

What would change the admission: quarantine observations with missing provenance, unexplained corrections, or an unknown release time when the proposed trade occurs on the publication date. Use a documented vintage and a trade after availability; if intraday availability is unknown, use information confirmed available before that trade. Admission is a methodological recommendation, not confirmation of instructor permission or a reason to add a new predictor to the optimizer.

Sources: [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [September 30 ALFRED CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-09-30), [Federal Reserve H.15 release](https://www.federalreserve.gov/releases/h15/). See [DGS10 data card](DGS10_data_card.md) for the three independently checked values and download timestamp.

## Apply the same test to the four funds

**Overall verdict: quarantine the saved adjusted-price series for claims about what a trader knew at every historical decision date. Admit them for clearly labeled historical estimation at a decision after their recorded download, subject to source and return-method checks.** A present-day historical return estimate is a different use from a simulated allocation decided years earlier. Freeze the downloaded inputs for each actual decision. Never infer historical availability merely from the measured date or add a fixed lag to today's adjusted history and call it point-in-time data.

| Series | What it measures / units | Historical-decision verdict | Reason and what would change it |
|---|---|---|---|
| SGOV | Adjusted share price, USD; ratios estimate returns of the iShares 0–3 Month Treasury Bond ETF | Quarantine | Daily close is known after the session, but today's adjusted history can reflect later distributions and corrections. Admit a historical signal only with a documented available vintage or a verified return reconstruction using contemporaneous prices and corporate actions. SGOV-only reserve eligibility remains a provisional Lab 15 rule. |
| VGIT | Adjusted share price, USD; ratios estimate returns of Vanguard Intermediate-Term Treasury ETF | Quarantine | Same availability and adjustment issue. Its Treasury holdings do not make its share return equal to DGS10 or cash. Admit after the same vintage/return checks and a documented execution rule. Reserve eligibility is unconfirmed. |
| VCIT | Adjusted share price, USD; ratios estimate returns of Vanguard Intermediate-Term Corporate Bond ETF | Quarantine | Same adjustment issue; price movements and distributions must both enter returns. Admit documented contemporaneous inputs or verified return reconstruction. A corporate bond yield such as BAA is not a substitute for VCIT returns. |
| ACWI | Adjusted share price, USD; ratios estimate returns of iShares MSCI ACWI ETF | Quarantine | Same adjustment issue, including distributions and any corporate-action corrections. Admit documented available inputs and a verified return method. Global equity exposure does not make an issuer NAV interchangeable with the ETF's exchange closing price. |

Official descriptions: [SGOV](https://www.ishares.com/us/products/314116/ishares-0-3-month-treasury-bond-etf), [VGIT](https://investor.vanguard.com/investment-products/etfs/profile/vgit), [VCIT](https://investor.vanguard.com/investment-products/etfs/profile/vcit), [ACWI](https://www.ishares.com/us/products/239600/ishares-msci-acwi-etf). Actual Lab 15 price provider: Yahoo Finance via yfinance, not FRED. Yahoo historical pages: [SGOV](https://finance.yahoo.com/quote/SGOV/history/), [VGIT](https://finance.yahoo.com/quote/VGIT/history/), [VCIT](https://finance.yahoo.com/quote/VCIT/history/), [ACWI](https://finance.yahoo.com/quote/ACWI/history/).

## Publication and vintage test actually run

The archived Lab 15 download was **22 October 2026 at 21:27:42 UTC**. It contains 61 completed month-end observations, September 2021 through September 2026, yielding 60 monthly returns. No incomplete October month is used. We made a fresh download of the same measured window on **29 October 2026**, completing the audit at **21:18:11 UTC**. The archive was preserved.

| Fund | Shared month-end prices | Adjusted levels differing by more than $0.000001 | Largest level difference ($) | Monthly returns differing by more than 0.0001 percentage point |
|---|---:|---:|---:|---:|
| SGOV | 61 | 49 | 0.000053 | 0 |
| VGIT | 61 | 51 | 0.000027 | 0 |
| VCIT | 61 | 44 | 0.000046 | 0 |
| ACWI | 61 | 22 | 0.000015 | 0 |

These are tiny download-to-download adjusted-level differences; the audit cannot identify their cause as economic revisions rather than provider calculation or floating-point differences. At the stated tolerance, none changed a monthly return materially. Do not describe these counts as confirmed substantive revisions. A common rescaling of both return endpoints cancels; rounding can still produce tiny differences.

**Publication lag:** daily closing prices require the session to finish; month-end sampled prices require the month's final trading session to finish and the provider to publish them. Exact Yahoo publication times are not in our files, so a fixed same-day availability promise is unsupported. The saved series can be demonstrated available by the October 22 download timestamp, not retrospectively on September 30. A hypothetical October 23 decision can use that archived completed history; a September 30 decision cannot claim that later download was its recorded information set.

**Revision policy:** adjusted prices can change with subsequent distributions, splits, or corrections; this audit measures only October 22 versus October 29. It does not establish all historical versions. Unlike ALFRED, the Yahoo interface used here does not let this app request a September 30 or January 15 vintage. Entering an ETF ticker into the FRED app is not a valid way to obtain ETF price vintages. Missing historical vintages must remain unknown, not be assigned zero revisions.

What would change quarantine: archived data for each decision date, or a transparent reconstruction of total returns from unadjusted prices and dated cash distributions/splits with validated event timing, plus a decision/execution rule that never uses a close before it is published. Validate distributions without double counting them when using adjusted-price ratios. Preserve source files, retrieval timestamps, measured dates, and the exact calculation version. Independently reconcile selected observations to a compatible price field; an issuer NAV or unadjusted close does not validate a Yahoo adjusted close by simple equality.

Full machine output: [fund vintage audit](fund_vintage_audit.md) and [comparison CSV](fund_vintage_comparison.csv). Repeat with `uv run --with pandas --with yfinance python audit_project2_funds.py` from Lab 17. Fresh raw downloads are saved separately in Lab 17. The earlier [Lab 15 reflection](../lab%2015/trade_date_reflection.md) documents the same historical-availability limitation.

Built with AI help; a learning demonstration, not investment advice.
