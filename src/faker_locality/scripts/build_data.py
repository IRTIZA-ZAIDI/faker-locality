import pandas as pd
from pathlib import Path

# 1. Correct Path Resolution
# Script location: src/faker_locality/scripts/build_data.py
SCRIPT_DIR = Path(__file__).resolve().parent

# The Project Root (where the raw /data folder lives)
PROJECT_ROOT = SCRIPT_DIR.parents[2]

# The Package Data folder (where store.py looks via importlib.resources)
PACKAGE_DATA = SCRIPT_DIR.parent / "data" / "processed"

RAW = PROJECT_ROOT / "data" / "raw"
OUT = PACKAGE_DATA

# Ensure output directory exists inside the package
OUT.mkdir(parents=True, exist_ok=True)


def load_exonyms():
    """Load and process the exonyms from the XLSX file and merge them for the store."""
    exonyms_file = RAW / "Exonyms.xlsx"

    if not exonyms_file.exists():
        print(f"Error: Could not find {exonyms_file}")
        return

    # Load all sheets
    try:
        country_df = pd.read_excel(exonyms_file, sheet_name="Country")
        city_df = pd.read_excel(exonyms_file, sheet_name="City")
        state_df = pd.read_excel(exonyms_file, sheet_name="States")
    except Exception as e:
        print(f"Error reading Excel sheets: {e}")
        return

    # Helper to clean columns and standardize names
    def clean_df(df, cols, level_name):
        df = df[cols].copy()
        # FIX: Rename the primary name column to 'exonym' to satisfy the test suite
        df.columns = ["exonym"] + [col.strip().lower() for col in df.columns[1:]]
        df["level"] = level_name
        return df

    # Standardize column selections (Primary Name + translated names)
    translations = [
        "Portuguese",
        "Spanish",
        "German",
        "Dutch",
        "Norwegian",
        "Indonesian",
        "Vietnamese",
        "Italian",
        "French",
        "Greek",
    ]

    # Process each level
    # We take the first column (Type, English, or English (state)) and map it to 'exonym'
    country_cleaned = clean_df(country_df, ["Type"] + translations, "country")
    city_cleaned = clean_df(city_df, ["English"] + translations, "city")
    state_cleaned = clean_df(state_df, ["English (state)"] + translations, "state")

    # Combine all into one master file as expected by store.py
    exonyms_master = pd.concat(
        [country_cleaned, city_cleaned, state_cleaned], ignore_index=True
    )

    # Save to parquet
    exonyms_master.to_parquet(OUT / "exonyms.parquet", index=False)

    print(f"Saved merged exonyms.parquet with 'exonym' column to {OUT}")


def process_worldcities():
    """Clean and save the worldcities data."""
    worldcities_file = RAW / "worldcities.csv"

    if not worldcities_file.exists():
        print(f"Error: Could not find {worldcities_file}")
        return

    wc_df = pd.read_csv(worldcities_file)

    # Map 'admin_name' to 'province' as found in your CSV inspection
    if "province" not in wc_df.columns and "admin_name" in wc_df.columns:
        wc_df = wc_df.rename(columns={"admin_name": "province"})

    # Select required columns and drop rows with missing values
    try:
        wc_df = wc_df[["city", "province", "country"]].dropna()
    except KeyError as e:
        print(f"Error: Required columns missing. {e}")
        return

    wc_df.to_parquet(OUT / "worldcities.parquet", index=False)
    print(f"Processed worldcities: {len(wc_df)} entries saved to {OUT}")


def main():
    # Run the processing steps
    process_worldcities()
    load_exonyms()


if __name__ == "__main__":
    main()
