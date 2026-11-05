# Data dictionary

All files are anonymised: accounts are `Cuenta 1`..`Cuenta 9`, competitors are `CompetitorN`, campaign names are generic. Origin: anonymised data sources (monthly account reporting and weekly auction reports).

## account_monthly.csv  (account x month)
| column | meaning |
|---|---|
| `account` | anonymised account label |
| `market` | country market of the account |
| `roas_metric` | how the account's return is measured (`Conv. Value/Cost`, `ROAS (Sale+Bin)` or `N/A`) |
| `month` | `YYYYMM` |
| `spend_eur` | media spend in the month (integer euros) |
| `roas` | revenue / spend as a ratio (0.90 = 90 %); empty when not available |

## auction_insights.csv  (account x month)
`competitors_listed`, `impression_share_pct` (% of eligible impressions won), `avg_position` (average rank, lower is better), `first_place_pct`. Empty = not reported.

## competitor_mentions.csv
Number of weekly auction reports in which each anonymised competitor is named, per account.

## campaign_snapshot.csv
ROAS of each campaign in the last week and the previous week of the account's latest snapshot month.

## params.json
Single source of truth for the model: damping of combined effects, ramp, capacity elasticity, worked example, the 15-action catalogue with its **hypothetical** effect ranges, ad-copy claim patterns, market defaults.

Integrity rules are checked in `tests/test_model.py` (nine accounts, ROAS identity, no real names).
