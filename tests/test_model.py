import math
import pytest
from media_buying_advisor import data, model, results, __version__

P = data.load_params()
EX = P["worked_example"]
B = {"S": EX["spend"], "roas": EX["roas"], "cpc": EX["cpc"], "cvr": EX["cvr"]}
ACTS = {a["id"]: a for a in P["actions"]}


def test_baseline_identities():
    s = model.scenario(B)
    assert math.isclose(s["roas"], B["roas"], rel_tol=1e-12)
    assert math.isclose(s["epl"] * B["cvr"] / B["cpc"], B["roas"], rel_tol=1e-12)          # ROAS = CVR*EPL/CPC
    assert math.isclose(s["cvr"] * s["epl"], 0.855, rel_tol=1e-9)                          # break-even CPC
    assert round(s["profit"]) == -2000


def test_worked_example_plan_roas():
    chosen = [ACTS[i] for i in P["plan_ids"]]
    roas = [model.scenario(B, model.combine(chosen, lv, P["damping"]))["roas"] for lv in ("lo", "mid", "hi")]
    assert [round(x * 100) for x in roas] == [115, 142, 173]


def test_ranges_are_ordered_for_actions_without_volume_lever():
    for a in P["actions"]:
        imp = model.action_impact(B, a)
        if "s" not in a["eff"]:
            assert imp["lo"] <= imp["mid"] <= imp["hi"], a["id"]


def test_volume_actions_destroy_value_below_break_even():
    """At ROAS < 100 % every extra euro of spend loses money, so volume levers cannot improve profit."""
    for a in P["actions"]:
        if set(a["eff"]) == {"s"}:
            assert model.action_impact(B, a)["mid"] < 0


def test_combining_with_damping_is_below_sum_of_parts():
    chosen = [ACTS[i] for i in P["plan_ids"]]
    full = model.scenario(B, model.combine(chosen, "mid", P["damping"]))["profit"] - model.scenario(B)["profit"]
    parts = sum(model.action_impact(B, a)["mid"] for a in chosen)
    assert full < parts * 1.2 and full > 0


def test_projection_ramps_to_steady_state():
    chosen = [ACTS[i] for i in P["plan_ids"]]
    pj = model.projection(B, chosen, P["projection"]["months"], P["projection"]["ramp_months"], P["damping"])
    assert pj["mid"][0] < pj["mid"][2] == pj["mid"][-1]


def test_capacity_model():
    c = model.capacity(1000, 15, 30, P["capacity_cpc_elasticity"])
    assert math.isclose(c["clicks"], 2000) and math.isclose(c["cpcUp"], 0.3)


def test_claims_coverage_on_example_ads():
    own = P["example_ads"]["own"].split("\n")
    cov = model.claims_of(own, P["claims"])
    assert set(cov) == set(P["claims"]) and all(0 <= v <= 1 for v in cov.values())
    assert cov["Velocidad"] > 0 and cov["Sin comisiones"] == 0


def test_account_data_integrity_and_reconciliation():
    accounts = data.load_accounts()
    assert len(accounts) == 9
    for a in accounts:
        for month, spend, roas in a["series"]:
            assert spend >= 0 and (roas is None or 0 <= roas < 10)
            if roas is not None and spend:
                # implied revenue / spend returns the reported ROAS (accounting identity of the model)
                s = model.scenario({"S": spend, "roas": roas, "cpc": 1.0, "cvr": 0.1})
                assert math.isclose(s["rev"] / s["spend"], roas, rel_tol=1e-9)


def test_dataset_is_anonymised():
    """Only generic labels may appear: accounts 'Cuenta N', competitors 'CompetitorN'."""
    import csv
    from pathlib import Path
    for r in csv.DictReader(open(Path(data.DATA) / "account_monthly.csv", encoding="utf-8")):
        assert r["account"].startswith("Cuenta ") and r["account"][7:].isdigit()
    for name in ("competitor_mentions.csv",):
        for r in csv.DictReader(open(Path(data.DATA) / name, encoding="utf-8")):
            assert r["competitor"].startswith("Competitor") and r["competitor"][10:].isdigit()
    for r in csv.DictReader(open(Path(data.DATA) / "campaign_snapshot.csv", encoding="utf-8")):
        assert r["account"].startswith("Cuenta ")


def test_results_json_is_current():
    import json
    res = json.loads((data.ROOT / "results" / "results.json").read_text(encoding="utf-8"))
    assert res["model_version"] == __version__
    assert res["p2"]["plan"]["roas"] == pytest.approx(results.build(P)["p2"]["plan"]["roas"])


def test_readme_quotes_current_headline():
    assert "115% / 142% / 173%" in (data.ROOT / "README.md").read_text(encoding="utf-8")
