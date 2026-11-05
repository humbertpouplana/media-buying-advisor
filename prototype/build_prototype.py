"""Build prototype/index.html from template.html + data/*.csv + data/params.json.

    python prototype/build_prototype.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from media_buying_advisor import data  # noqa: E402


def main(out: Path | None = None) -> Path:
    params = data.load_params()
    payload = {"brands": data.load_accounts(), "source": "Fuentes anonimizadas de datos"}
    tpl = (ROOT / "prototype" / "template.html").read_text(encoding="utf-8")
    html = tpl.replace("__DATA__", json.dumps(payload, ensure_ascii=False, separators=(",", ":"))).replace("__PARAMS__", json.dumps(params, ensure_ascii=False, separators=(",", ":")))
    out = out or ROOT / "prototype" / "index.html"
    out.write_text(html, encoding="utf-8")
    print("built", out, len(html), "bytes")
    return out


if __name__ == "__main__":
    main()
