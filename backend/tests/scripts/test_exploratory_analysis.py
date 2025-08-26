import json
from pathlib import Path

import pandas as pd

from app.scripts.exploratory_analysis import load_head, load_for_metrics, compute_metrics, main


def _make_sample_csv(path: Path) -> None:
    df = pd.DataFrame(
        {
            "Category": ["A", "A", "B", "B", "B"],
            "BaseYield": [100, 200, 300, None, 400],
            "Cost": [10.5, 20.0, 5.0, 2.5, 12.0],
            "EnvironmentalImpact": [1.0, 2.0, None, 4.0, 5.0],
            "Extra": [1, 2, 3, 4, 5],
        }
    )
    df.to_csv(path, index=False)


def test_head_and_metrics(tmp_path: Path):
    csv = tmp_path / "sample.csv"
    _make_sample_csv(csv)

    head_df = load_head(csv, n=3)
    assert len(head_df) == 3

    df = load_for_metrics(csv)
    assert set(["Category", "BaseYield", "Cost", "EnvironmentalImpact"]).issubset(df.columns)

    summary = compute_metrics(df)
    assert set(["averages", "by_category"]).issubset(summary.keys())

    # Averages
    av = summary["averages"]
    assert av["BaseYield"] == 250.0  # (100+200+300+400)/4
    assert av["Cost"] == 10.0  # (10.5+20+5+2.5+12)/5
    assert av["EnvironmentalImpact"] == 3.0  # (1+2+4+5)/4

    # By category
    by_cat = {row["Category"]: row for row in summary["by_category"]}
    assert by_cat["A"]["count"] == 2
    assert by_cat["B"]["count"] == 3
    assert by_cat["A"]["AvgYield"] == 150.0
    assert by_cat["B"]["AvgCost"] == (5.0 + 2.5 + 12.0) / 3


def test_main_json_out(tmp_path: Path):
    csv = tmp_path / "sample.csv"
    out_json = tmp_path / "summary.json"
    _make_sample_csv(csv)

    exit_code = main(["--path", str(csv), "--json-out", str(out_json), "--head-rows", "2"])
    assert exit_code == 0
    assert out_json.exists()
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert "averages" in data and "by_category" in data