"""
Script: check_dataset_integrity.py

Valida la integridad del dataset de productos.
Mejoras:
- Ruta por defecto robusta (backend/datasets/product_dataset.csv)
- CLI (--path, --strict) y manejo de errores amigable
- Validaciones vectorizadas y seguras ante columnas ausentes
"""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import timedelta
import sys

import pandas as pd


def default_dataset_path() -> Path:
    # Este archivo está en backend/app/scripts/...  => subir dos niveles para llegar a backend/
    backend_root = Path(__file__).resolve().parents[2]
    return backend_root / "datasets" / "product_dataset.csv"


def check_integrity(df: pd.DataFrame) -> dict:
    """Ejecuta verificaciones de integridad y devuelve un resumen de issues."""
    issues: dict[str, int] = {
        "missing_columns": 0,
        "nulls": 0,
        "negatives": 0,
        "invalid_shelf_life": 0,
    }

    print("=== Checking required columns / Verificando columnas obligatorias ===")
    required_columns = [
        "Id",
        "Name",
        "Code",
        "Category",
        "IsActive",
        "BaseYield",
        "NutritionalValue",
        "Cost",
        "EnvironmentalImpact",
        "ShelfLife",
    ]
    missing = [c for c in required_columns if c not in df.columns]
    for col in missing:
        print(f"Missing column: {col} / Falta columna: {col}")
    issues["missing_columns"] = len(missing)

    print("\n=== Checking non-null values / Verificando valores nulos ===")
    non_nullable = [c for c in ["Id", "Name", "Code", "Category", "IsActive"] if c in df.columns]
    if non_nullable:
        null_counts = df[non_nullable].isnull().sum()
        for col, cnt in null_counts.items():
            print(f"{col}: {cnt} null values / valores nulos")
        issues["nulls"] = int(null_counts.sum())
    else:
        print("No non-nullable columns found present / No se hallaron columnas no nulas presentes")

    print("\n=== Checking numeric ranges / Verificando rangos numéricos ===")
    numeric_columns = [c for c in ["BaseYield", "NutritionalValue", "Cost", "EnvironmentalImpact"] if c in df.columns]
    for col in numeric_columns:
        series = pd.to_numeric(df[col], errors="coerce")
        neg_count = int((series < 0).sum())
        col_min, col_max = series.min(skipna=True), series.max(skipna=True)
        if neg_count > 0:
            print(f"Warning: {col} has {neg_count} negative values / valores negativos")
        print(f"{col} - min: {col_min}, max: {col_max}")
        issues["negatives"] += neg_count

    print("\n=== Checking ShelfLife positive / Verificando ShelfLife positiva ===")
    if "ShelfLife" in df.columns:
        shelf = pd.to_timedelta(df["ShelfLife"], errors="coerce")
        invalid = shelf.isna().sum()
        non_positive = (shelf <= timedelta(0)).sum()
        print(f"ShelfLife invalid (NaT): {int(invalid)}")
        print(f"ShelfLife <= 0 days: {int(non_positive)} products / productos")
        issues["invalid_shelf_life"] = int(invalid + non_positive)
    else:
        print("Column 'ShelfLife' not present / Columna 'ShelfLife' no presente")
        issues["missing_columns"] += 1

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check integrity of the product dataset (CSV)")
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Ruta del CSV a validar (por defecto backend/datasets/product_dataset.csv)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Salir con código 1 si hay issues detectados",
    )
    args = parser.parse_args(argv)

    csv_path = Path(args.path) if args.path else default_dataset_path()
    if not csv_path.exists():
        print(f"ERROR: CSV not found / no encontrado: {csv_path}")
        return 1

    try:
        df = pd.read_csv(csv_path, low_memory=False)
    except Exception as e:
        print(f"ERROR loading CSV: {e}")
        return 1

    print(f"Dataset loaded: {len(df)} rows / filas\n")
    issues = check_integrity(df)

    total_issues = sum(issues.values())
    print("\n=== Summary / Resumen ===")
    for k, v in issues.items():
        print(f"{k}: {v}")
    print(f"Total issues: {total_issues}")
    print("\n=== Done / Listo! ===")

    if args.strict and total_issues > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
