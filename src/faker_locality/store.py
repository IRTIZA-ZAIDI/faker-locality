import pandas as pd
from importlib import resources
from functools import lru_cache


@lru_cache(maxsize=1)
def load_localities() -> pd.DataFrame:
    """Load and return the processed localities data (city, province, country)."""
    # resources.files points to src/faker_locality
    pkg_root = resources.files("faker_locality")
    # Path must match tree: data/processed/worldcities.parquet
    file_path = pkg_root.joinpath("data", "processed", "worldcities.parquet")

    if not file_path.exists():
        raise FileNotFoundError(
            f"Parquet file not found at {file_path}. Did you run build_data.py?"
        )

    return pd.read_parquet(file_path)


@lru_cache(maxsize=1)
def load_exonyms() -> pd.DataFrame:
    """Load and return the processed exonyms data."""
    pkg_root = resources.files("faker_locality")
    file_path = pkg_root.joinpath("data", "processed", "exonyms.parquet")

    if not file_path.exists():
        raise FileNotFoundError(f"Parquet file not found at {file_path}.")

    return pd.read_parquet(file_path)
