"""Class 6 — solution: process multiple station CSV files with functions.

Refactors station-processing.py into reusable functions and loops over
several input files (real Hartheim + synthetic second station).
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "processed_data"
STATION_PATH = DATA_DIR / "26030350_hourly.csv"
SYNTHETIC_DIR = Path(__file__).resolve().parent / "_exercise_stations"

COLUMNS = [
    "temperature_2m",
    "humidity_2m",
    "temperature_ground",
    "precipitation",
]


def load_station(csv_path):
    df = pd.read_csv(csv_path, parse_dates=["utc_time"])
    return df.set_index("utc_time")


def select_columns(df, columns):
    return df[columns].copy()


def add_gradient_column(df):
    df = df.copy()
    df["temp_gradient_2m_minus_ground"] = (
        df["temperature_2m"] - df["temperature_ground"]
    )
    return df


def daily_summary(df):
    daily_mean = df[["temperature_2m", "humidity_2m", "temperature_ground"]].resample(
        "D"
    ).mean()
    daily_precip = df[["precipitation"]].resample("D").sum()
    return daily_mean.join(daily_precip)


def process_station_csv(csv_path, columns):
    """Process one station CSV and return a summary dictionary."""
    raw = load_station(csv_path)
    data = add_gradient_column(select_columns(raw, columns))
    daily = daily_summary(data)

    return {
        "path": str(csv_path),
        "n_rows": len(data),
        "mean_temperature_2m_c": float(data["temperature_2m"].mean()),
        "n_hot_hours": int((data["temperature_2m"] > 38).sum()),
        "daily": daily,
    }


def make_synthetic_station(source_path, output_dir):
    """Create a second CSV (subset of dates, slightly shifted temps) for the exercise."""
    output_dir.mkdir(exist_ok=True)
    raw = load_station(source_path)
    subset = raw.loc["2026-07-01":"2026-08-31"].copy()
    subset["temperature_2m"] = subset["temperature_2m"] + 1.5
    subset["temperature_ground"] = subset["temperature_ground"] + 1.0
    out_path = output_dir / "synthetic_station_hourly.csv"
    subset.reset_index().to_csv(out_path, index=False)
    return out_path


def main():
    synthetic_path = make_synthetic_station(STATION_PATH, SYNTHETIC_DIR)
    station_paths = [STATION_PATH, synthetic_path]

    results = []
    for path in station_paths:
        print(f"Processing {path.name}...")
        summary = process_station_csv(path, COLUMNS)
        results.append(summary)
        print(f"  Rows: {summary['n_rows']}")
        print(f"  Mean 2 m temp: {summary['mean_temperature_2m_c']:.2f} °C")
        print(f"  Hot hours (>38 °C): {summary['n_hot_hours']}")
        print(f"  Daily records: {summary['daily'].shape[0]}")
        print()

    print(f"Processed {len(results)} station file(s).")


if __name__ == "__main__":
    main()
