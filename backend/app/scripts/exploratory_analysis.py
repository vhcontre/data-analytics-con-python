"""
exploratory_analysis.py

Análisis exploratorio rápido y robusto del dataset de productos.
Mejoras:
- CLI (--path, --head-rows, --json-out)
- Ruta por defecto consistente
- Lectura rápida de head (nrows) y carga selectiva de columnas para el resto
- Conversión numérica segura
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def default_dataset_path() -> Path:
    # Este archivo está en backend/app/scripts/...  => subir dos niveles para llegar a backend/
    backend_root = Path(__file__).resolve().parents[2]
    return backend_root / "datasets" / "product_dataset.csv"


def load_head(csv_path: Path, n: int = 5) -> pd.DataFrame:
    return pd.read_csv(csv_path, nrows=max(1, n), low_memory=False)


def load_for_metrics(csv_path: Path) -> pd.DataFrame:
    usecols = ["Category", "BaseYield", "Cost", "EnvironmentalImpact"]
    df = pd.read_csv(csv_path, usecols=usecols, low_memory=False)
    for col in ["BaseYield", "Cost", "EnvironmentalImpact"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def compute_metrics(df: pd.DataFrame) -> dict:
    avg_metrics = {
        "BaseYield": (float(df["BaseYield"].mean()) if "BaseYield" in df else None),
        "Cost": (float(df["Cost"].mean()) if "Cost" in df else None),
        "EnvironmentalImpact": (
            float(df["EnvironmentalImpact"].mean()) if "EnvironmentalImpact" in df else None
        ),
    }

    by_category = {}
    if "Category" in df.columns:
        grouped = df.groupby("Category", dropna=False)
        by_category = (
            grouped.agg(
                count=("Category", "size"),
                AvgYield=("BaseYield", "mean"),
                AvgCost=("Cost", "mean"),
                AvgEnvImpact=("EnvironmentalImpact", "mean"),
            )
            .reset_index()
            .to_dict(orient="records")
        )

    return {"averages": avg_metrics, "by_category": by_category}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Exploratory analysis of the product dataset")
    parser.add_argument("--path", type=str, default=None, help="Ruta del CSV (default: backend/datasets/product_dataset.csv)")
    parser.add_argument("--head-rows", type=int, default=5, help="Filas a mostrar en el head (default: 5)")
    parser.add_argument("--json-out", type=str, default=None, help="Guardar resumen en JSON (opcional)")
    args = parser.parse_args(argv)

    csv_path = Path(args.path) if args.path else default_dataset_path()
    if not csv_path.exists():
        print(f"ERROR: CSV not found / no encontrado: {csv_path}")
        return 1

    # Head
    head_df = load_head(csv_path, n=args.head_rows)
    print(f"Dataset head ({len(head_df)} rows):\n{head_df}\n")

    # Métricas
    df = load_for_metrics(csv_path)
    print(f"Dataset loaded for metrics: {len(df)} rows / filas\n")

    summary = compute_metrics(df)
    print("Average metrics / Promedio de métricas:")
    print(pd.Series(summary["averages"]))

    if summary["by_category"]:
        print("\nMetrics by Category / Métricas por categoría:")
        for row in summary["by_category"]:
            print(
                f"- {row['Category']}: count={int(row['count'])}, "
                f"AvgYield={row['AvgYield']}, AvgCost={row['AvgCost']}, AvgEnvImpact={row['AvgEnvImpact']}"
            )

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"\nSummary saved to: {out_path}")

    print("\nExploratory analysis completed successfully / Análisis exploratorio completado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
