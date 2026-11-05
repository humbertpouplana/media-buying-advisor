"""The HTML prototype keeps a JavaScript mirror of the model; it must agree with the Python reference."""
import json
import shutil
import subprocess
import pytest
from media_buying_advisor import data, model

ROOT = data.ROOT


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_prototype_matches_python():
    html = ROOT / "prototype" / "index.html"
    if not html.exists():
        pytest.skip("run `make prototype` first")
    out = json.loads(subprocess.run(["node", str(ROOT / "tests" / "js_parity.js"), str(html)], capture_output=True, text=True, check=True).stdout)
    P = data.load_params(); ex = P["worked_example"]
    b = {"S": ex["spend"], "roas": ex["roas"], "cpc": ex["cpc"], "cvr": ex["cvr"]}
    chosen = [a for a in P["actions"] if a["id"] in P["plan_ids"]]
    assert out["profit"] == pytest.approx(model.scenario(b)["profit"])
    assert out["planRoas"] == pytest.approx([model.scenario(b, model.combine(chosen, lv, P["damping"]))["roas"] for lv in ("lo", "mid", "hi")])
    assert out["impacts"] == pytest.approx([model.action_impact(b, a)["mid"] for a in P["actions"]])
    assert out["cap"] == pytest.approx(model.capacity(model.scenario(b)["clicks"], ex["impression_share"], 35, P["capacity_cpc_elasticity"])["extra"])
    py = model.claims_of(P["example_ads"]["own"].split("\n"), P["claims"])
    assert out["claims"] == pytest.approx(py)
