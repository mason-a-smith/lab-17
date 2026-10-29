# Lab 17 verification

Default as-known date: 2026-10-29. Live public CSV downloads.

Four charts and the four-row comparison table rendered with no errors or exceptions.

```text
                                         Series Last date known then  Value known then Last date today  Value today  Values after last date known then  Revised values on shared dates
         https://fred.stlouisfed.org/series/BAA           2026-09-01              6.47      2026-09-01         6.47                                  0                               0
    https://fred.stlouisfed.org/series/FEDFUNDS           2026-09-01              3.75      2026-09-01         3.75                                  0                               0
       https://fred.stlouisfed.org/series/DGS10           2026-10-28              5.05      2026-10-28         5.05                                  0                               0
https://fred.stlouisfed.org/series/MORTGAGE30US           2026-10-29              7.24      2026-10-29         7.24                                  0                               0
```

Unknown-ID check: 2 per-series download errors; all four valid charts remain. No app exceptions.

App running at http://127.0.0.1:8503. Default browser opened through Windows; visual browser inspection unavailable.
