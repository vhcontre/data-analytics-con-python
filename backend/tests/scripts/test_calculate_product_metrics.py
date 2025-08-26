import json
from pathlib import Path

import pandas as pd

from app.scripts.calculate_product_metrics import load_dataset, compute_metrics, main


def _make_sample_csv(path: Path) -> None:
    df = pd.DataFrame(
        {
            "Category": ["A", "A", "B", "B", "B"],
            "BaseYield": [100, 200, 300, None, 400],
            "Cost": [10.5, 20.0, 5.0, 2.5, 12.0],
            "EnvironmentalImpact": [1.0, 2.0, None, 4.0, 5.0],
        }
    )
    df.to_csv(path, index=False)


def test_compute_metrics_from_temp_csv(tmp_path: Path):
    csv = tmp_path / "sample.csv"
    _make_sample_csv(csv)

    df = load_dataset(csv)
    metrics = compute_metrics(df)

    # Global checks
    assert metrics["rows"] == 5
    # BaseYield mean over [100,200,300,None,400] => (100+200+300+400)/4 = 250.0
    assert metrics["average_base_yield"] == 250.0
    # total cost: 10.5+20+5+2.5+12 = 50.0
    assert metrics["total_cost"] == 50.0
    # env impact average over [1,2,None,4,5] => (1+2+4+5)/4 = 3.0
    assert metrics["average_environmental_impact"] == 3.0

    # By category
    by_cat = metrics["by_category"]
    assert set(by_cat.keys()) == {"A", "B"}
    assert by_cat["A"]["count"] == 2
    assert by_cat["B"]["count"] == 3
    # Category A AvgYield: mean([100,200]) = 150
    assert by_cat["A"]["AvgYield"] == 150.0
    # Category B TotalCost: 5.0 + 2.5 + 12.0 = 19.5
    assert by_cat["B"]["TotalCost"] == 19.5


def test_main_writes_json(tmp_path: Path, monkeypatch):
    csv = tmp_path / "sample.csv"
    out_json = tmp_path / "metrics.json"
    _make_sample_csv(csv)

    # Call main with arguments (bypass CLI parsing from sys.argv)
    exit_code = main(["--path", str(csv), "--json-out", str(out_json)])
    assert exit_code == 0
    assert out_json.exists()

    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert set(["rows", "average_base_yield", "total_cost", "average_environmental_impact", "by_category"]).issubset(
        data.keys()
    )