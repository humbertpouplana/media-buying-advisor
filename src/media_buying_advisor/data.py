from __future__ import annotations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def load_params(path=DATA / "params.json") -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _rows(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _f(x):
    return None if x == "" else float(x)


def load_accounts() -> list[dict]:
    """Rebuild the account structure used by the prototype and the paper figures."""
    brands: dict[str, dict] = {}
    for r in _rows("account_monthly.csv"):
        b = brands.setdefault(r["account"], {"name": r["account"], "mkt": r["market"], "mt": r["roas_metric"], "series": [], "comps": {}, "ins": [], "camps": [], "campSk": None})
        b["series"].append([int(r["month"]), int(r["spend_eur"]), _f(r["roas"])])
    for r in _rows("auction_insights.csv"):
        brands[r["account"]]["ins"].append([int(r["month"]), *(None if r[k] == "" else float(r[k]) if k != "competitors_listed" else int(r[k]) for k in ("competitors_listed", "impression_share_pct", "avg_position", "first_place_pct"))])
    for r in _rows("competitor_mentions.csv"):
        brands[r["account"]]["comps"][r["competitor"]] = int(r["mentions"])
    for r in _rows("campaign_snapshot.csv"):
        b = brands[r["account"]]; b["campSk"] = int(r["snapshot_month"])
        b["camps"].append({"n": r["campaign"], "rl": _f(r["roas_last_week"]), "rp": _f(r["roas_prev_week"])})
    return list(brands.values())
