# Task 2: Collect up to 25 stories per category (125 total).

import json
import pandas as pd


def process_data():
    """Load raw data and produce a cleaned dataset."""
    with open("raw_data.json", "r", encoding="utf-8") as fh:
        raw_data = json.load(fh)

    df = pd.DataFrame(raw_data)

    if "collected_at" in df.columns:
        df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")
    else:
        raise KeyError("raw_data.json must contain 'collected_at' field")

    df = df.sort_values("collected_at")
    df.to_csv("processed_data.csv", index=False)
    print(f"Saved processed_data.csv with {len(df)} records")


if __name__ == "__main__":
    process_data()