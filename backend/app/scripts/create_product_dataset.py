"""
scripts/create_product_dataset.py

Genera un dataset de productos aleatorio y lo guarda en CSV.
Mejoras:
- CLI con parámetros (--num-samples, --seed, --out)
- Ruta de salida robusta relativa al repo (backend/datasets)
- Crea el directorio de salida si no existe
- Reproducibilidad opcional vía semilla
"""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime, timedelta
import uuid

import numpy as np
import pandas as pd


def generate_dataset(num_samples: int, seed: int | None = None) -> pd.DataFrame:
    """Genera un DataFrame con datos de productos.

    Args:
        num_samples: cantidad de filas a generar.
        seed: semilla opcional para reproducibilidad.

    Returns:
        DataFrame con el dataset de productos.
    """
    if seed is not None:
        np.random.seed(seed)

    categories = ["Food", "Supplement", "Beverage", "Material", "Other"]  # ProductCategory

    data = {
        "Id": [str(uuid.uuid4()) for _ in range(num_samples)],
        "Name": [f"Product_{i+1}" for i in range(num_samples)],
        "Code": [f"P{i+1000}" for i in range(num_samples)],
        "Description": [f"Description of product {i+1}" for i in range(num_samples)],
        "Category": np.random.choice(categories, num_samples),
        "IsActive": np.random.choice([True, False], num_samples, p=[0.9, 0.1]),
        "DiscontinuedAt": [
            datetime.now() - timedelta(days=np.random.randint(0, 365))
            if np.random.rand() < 0.1
            else None
            for _ in range(num_samples)
        ],
        "BaseYield": np.random.uniform(50, 100, num_samples),
        "NutritionalValue": np.random.uniform(1, 10, num_samples),
        "Cost": np.random.uniform(10, 100, num_samples),
        "EnvironmentalImpact": np.random.uniform(0.1, 5.0, num_samples),
        "Notes": [f"Note {i+1}" for i in range(num_samples)],
        "Supplier": [f"Supplier {i % 5 + 1}" for i in range(num_samples)],
        "ShelfLife": [timedelta(days=np.random.randint(30, 365)) for _ in range(num_samples)],
    }

    return pd.DataFrame(data)


def default_output_path() -> Path:
    """Calcula la ruta por defecto para guardar el CSV dentro del repo.

    Coloca el archivo en: backend/datasets/product_dataset.csv
    """
    # Este archivo está en backend/app/scripts/...  => subir dos niveles para llegar a backend/
    backend_root = Path(__file__).resolve().parents[2]
    return backend_root / "datasets" / "product_dataset.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a synthetic product dataset and save as CSV")
    parser.add_argument("--num-samples", type=int, default=50, help="Number of products to generate (default: 50)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility (optional)")
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output CSV path (default: backend/datasets/product_dataset.csv)",
    )
    args = parser.parse_args()

    df = generate_dataset(num_samples=args.num_samples, seed=args.seed)

    out_path = Path(args.out) if args.out else default_output_path()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(
        f"Product dataset generated successfully at: {out_path} \n"
        "Dataset de productos generado exitosamente!"
    )


if __name__ == "__main__":
    main()
