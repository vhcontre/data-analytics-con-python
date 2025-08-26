"""
calculate_product_metrics.py

Calcula métricas clave del dataset de productos de forma eficiente.
Mejoras:
- CLI (--path, --json-out) y ruta por defecto robusta
- Lectura selectiva de columnas para menor uso de memoria
- Conversión numérica segura y agregaciones en una sola pasada
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


def load_dataset(csv_path: Path) -> pd.DataFrame:
    # Leer solo columnas necesarias
    usecols = ["Category", "BaseYield", "Cost", "EnvironmentalImpact"]
    df = pd.read_csv(csv_path, usecols=usecols, low_memory=False)

    # Convertir a numérico de forma segura
    for col in ["BaseYield", "Cost", "EnvironmentalImpact"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def compute_metrics(df: pd.DataFrame) -> dict:
    # Métricas globales
    average_yield = float(df["BaseYield"].mean()) if "BaseYield" in df else None
    total_cost = float(df["Cost"].sum()) if "Cost" in df else None
    average_env = float(df["EnvironmentalImpact"].mean()) if "EnvironmentalImpact" in df else None

    # Conteos por categoría y agregados por categoría en una sola pasada
    by_cat = {}
    if "Category" in df.columns:
        grouped = df.groupby("Category", dropna=False)
        size = grouped.size()
        agg = grouped.agg(
            AvgYield=("BaseYield", "mean"),
            TotalCost=("Cost", "sum"),
            AvgEnvImpact=("EnvironmentalImpact", "mean"),
        )
        # Pasar a dicts serializables
        by_cat = {
            str(cat): {
                "count": int(size.get(cat, 0)),
                "AvgYield": (float(agg.loc[cat, "AvgYield"]) if pd.notna(agg.loc[cat, "AvgYield"]) else None),
                "TotalCost": (float(agg.loc[cat, "TotalCost"]) if pd.notna(agg.loc[cat, "TotalCost"]) else None),
                "AvgEnvImpact": (float(agg.loc[cat, "AvgEnvImpact"]) if pd.notna(agg.loc[cat, "AvgEnvImpact"]) else None),
            }
            for cat in agg.index
        }

    return {
        "rows": int(len(df)),
        "average_base_yield": average_yield,
        "total_cost": total_cost,
        "average_environmental_impact": average_env,
        "by_category": by_cat,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate product metrics from CSV")
    parser.add_argument("--path", type=str, default=None, help="Ruta del CSV (default: backend/datasets/product_dataset.csv)")
    parser.add_argument("--json-out", type=str, default=None, help="Archivo JSON para guardar las métricas (opcional)")
    args = parser.parse_args(argv)

    csv_path = Path(args.path) if args.path else default_dataset_path()
    if not csv_path.exists():
        print(f"ERROR: CSV not found / no encontrado: {csv_path}")
        return 1

    df = load_dataset(csv_path)
    print(f"Dataset loaded: {len(df)} rows / filas")

    metrics = compute_metrics(df)

    # Salida por consola
    print(f"Average BaseYield / Rendimiento promedio: {metrics['average_base_yield']:.2f}" if metrics["average_base_yield"] is not None else "Average BaseYield: N/A")
    print(f"Total Cost / Costo acumulado: {metrics['total_cost']:.2f}" if metrics["total_cost"] is not None else "Total Cost: N/A")
    print(
        f"Average Environmental Impact / Impacto ambiental promedio: {metrics['average_environmental_impact']:.2f}"
        if metrics["average_environmental_impact"] is not None
        else "Average Environmental Impact: N/A"
    )

    if metrics["by_category"]:
        print("\nMetrics by Category / Métricas por categoría:")
        for cat, vals in metrics["by_category"].items():
            print(
                f"- {cat}: count={vals['count']}, AvgYield={vals['AvgYield']}, TotalCost={vals['TotalCost']}, AvgEnvImpact={vals['AvgEnvImpact']}"
            )

    # Opcional: guardar a JSON
    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print(f"\nMetrics saved to: {out_path}")

    print("\nAll metrics calculated successfully / Todas las métricas calculadas correctamente")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
