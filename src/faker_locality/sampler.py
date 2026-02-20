import random
from faker_locality.store import load_localities
from typing import Dict, Optional


def get_location(
    country: Optional[str] = None,
    province: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, str]:
    """Sample a location based on country and/or province."""
    df = load_localities()

    if country:
        df = df[df["country"] == country]
    if province:
        df = df[df["province"] == province]

    if df.empty:
        raise ValueError("No matching localities found.")

    rng = random.Random(seed)
    row = df.iloc[rng.randrange(len(df))]
    return {"country": row["country"], "province": row["province"], "city": row["city"]}


def get_city(
    country: Optional[str] = None,
    province: Optional[str] = None,
    seed: Optional[int] = None,
) -> str:
    """Sample a city based on country and/or province."""
    return get_location(country=country, province=province, seed=seed)["city"]
