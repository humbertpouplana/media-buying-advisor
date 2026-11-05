"""Compute every number used by the paper, README and tests; write results/results.json.

Run:  python -m media_buying_advisor.results
"""
from __future__ import annotations
import json
from pathlib import Path
from . import data as D, model as M, __version__


def build(params: dict) -> dict:
    ex = params["worked_example"]
    b = {"S": ex["spend"], "roas": ex["roas"], "cpc": ex["cpc"], "cvr": ex["cvr"]}
    damp = params["damping"]
    base = M.scenario(b)
    acts = params["actions"]
    chosen = [a for a in acts if a["id"] in params["plan_ids"]]
    sh = params["tornado_shock"]
    tor = [[l, M.scenario(b, e)["profit"] - base["profit"]] for l, e in
           [("CPC -20%", {"c": -sh}), ("CPC +20%", {"c": sh}), ("CVR +20%", {"v": sh}), ("CVR -20%", {"v": -sh}),
            ("EPL +20%", {"e": sh}), ("EPL -20%", {"e": -sh}), ("Volume +20%", {"s": sh}), ("Volume -20%", {"s": -sh})]]
    p2 = {"base": base,
          "acts": [{"id": a["id"], "t": a["t"], "effort": a["effort"], "imp": M.action_impact(b, a), "eff": a["eff"]} for a in acts],
          "plan": {"ids": [a["id"] for a in chosen],
                   "proj": M.projection(b, chosen, params["projection"]["months"], params["projection"]["ramp_months"], damp),
                   "roas": [M.scenario(b, M.combine(chosen, lv, damp))["roas"] for lv in ("lo", "mid", "hi")]},
          "tor": tor,
          "cap": [[x, M.capacity(base["clicks"], ex["impression_share"], x, params["capacity_cpc_elasticity"])] for x in params["capacity_targets"]],
          "be": base["cvr"] * base["epl"]}
    return {"model_version": __version__, "params": {k: v for k, v in params.items() if k not in ("actions", "claims", "example_ads", "markets", "problems")}, "p2": p2}


def main(out=None) -> dict:
    res = build(D.load_params())
    path = Path(out) if out else D.ROOT / "results" / "results.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(f"results written to {path}: base profit {res['p2']['base']['profit']:,.0f} EUR, plan ROAS {[round(x, 3) for x in res['p2']['plan']['roas']]}")
    return res


if __name__ == "__main__":
    main()
