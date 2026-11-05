"""Unit economics.  ROAS = CVR * EPL / CPC;  break-even CPC = CVR * EPL.

Levers: c = CPC, v = click-to-lead conversion, e = EPL (value per lead), s = spend volume.
Every effect range is a hypothesis taken from `data/params.json`, not a measured elasticity.
"""
from __future__ import annotations
import re


def scenario(b: dict, e: dict | None = None) -> dict:
    e = e or {}
    c, v, ep, s = e.get("c", 0), e.get("v", 0), e.get("e", 0), e.get("s", 0)
    spend = b["S"] * (1 + s)
    clicks = spend / (b["cpc"] * (1 + c))
    leads = clicks * b["cvr"] * (1 + v)
    epl = b["roas"] * b["cpc"] / b["cvr"] * (1 + ep)
    rev = leads * epl
    return {"spend": spend, "clicks": clicks, "leads": leads, "epl": epl, "rev": rev, "profit": rev - spend,
            "roas": rev / spend if spend else 0.0, "cpl": spend / leads if leads else 0.0,
            "cpc": b["cpc"] * (1 + c), "cvr": b["cvr"] * (1 + v)}


def combine(actions: list[dict], level: str, damp: float) -> dict:
    k = 0.0 if level == "lo" else 1.0 if level == "hi" else 0.5
    t = {"c": 1.0, "v": 1.0, "e": 1.0, "s": 1.0}
    for a in actions:
        for key in "cves":
            x = a["eff"].get(key)
            if not x:
                continue
            # the CPC improves towards its most negative end
            val = x[1] + (x[0] - x[1]) * k if key == "c" else x[0] + (x[1] - x[0]) * k
            t[key] *= 1 + damp * val
    return {key: t[key] - 1 for key in t}


def action_impact(b: dict, a: dict) -> dict:
    base = scenario(b)["profit"]
    return {lv: scenario(b, combine([a], lv, 1.0))["profit"] - base for lv in ("lo", "mid", "hi")}


def projection(b: dict, actions: list[dict], months: int, ramp: float, damp: float) -> dict:
    base = scenario(b)["profit"]
    out = {"base": [], "lo": [], "mid": [], "hi": []}
    sc = {lv: scenario(b, combine(actions, lv, damp))["profit"] for lv in ("lo", "mid", "hi")}
    for m in range(1, months + 1):
        r = min(1.0, m / ramp)
        out["base"].append(base)
        for lv in sc:
            out[lv].append(base + (sc[lv] - base) * r)
    return out


def priority(a: dict, imp: dict, problems: set) -> float:
    hit = any(x in problems for x in a["p"])
    return imp["mid"] / a["effort"] * (1.5 if hit else 1.0)


def claims_of(lines: list[str], claims: dict) -> dict:
    n = len(lines)
    return {k: (sum(1 for l in lines if re.search(p, l, re.I)) / n if n else 0.0) for k, p in claims.items()}


def capacity(clicks: float, is_now: float, is_target: float, elast: float) -> dict:
    f = is_target / is_now
    return {"clicks": clicks * f, "extra": clicks * (f - 1), "cpcUp": elast * (f - 1)}
