import pandas as pd

from app.scripts.create_product_dataset import generate_dataset


def test_generate_dataset_row_count():
    df = generate_dataset(num_samples=10, seed=123)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    # columnas mínimas esperadas
    expected = {
        "Id",
        "Name",
        "Code",
        "Description",
        "Category",
        "IsActive",
        "DiscontinuedAt",
        "BaseYield",
        "NutritionalValue",
        "Cost",
        "EnvironmentalImpact",
        "Notes",
        "Supplier",
        "ShelfLife",
    }
    assert expected.issubset(df.columns)


def test_write_csv_to_tmp(tmp_path):
    df = generate_dataset(num_samples=7, seed=42)
    out_file = tmp_path / "product_dataset.csv"
    df.to_csv(out_file, index=False)
    assert out_file.exists()
    df_read = pd.read_csv(out_file)
    assert len(df_read) == 7