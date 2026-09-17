"""Class 6 — station-processing script (Class 4 workflow).

Linear script version of the Class 4 tabular analysis:
load CSV → select columns → derived column → filter → daily resample.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "processed_data"
STATION_PATH = DATA_DIR / "26030350_hourly.csv"

COLUMNS = [
    "temperature_2m",
    "humidity_2m",
    "temperature_ground",
    "precipitation",
]


def load_station(csv_path):
    """Load a Hartheim-style hourly CSV and set the datetime index."""
    df = pd.read_csv(csv_path, parse_dates=["utc_time"])
    return df.set_index("utc_time")


def select_columns(df, columns):
    """Keep only the columns needed for analysis."""
    return df[columns].copy()


def add_gradient_column(df):
    """Air temperature minus ground temperature."""
    df["temp_gradient_2m_minus_ground"] = (
        df["temperature_2m"] - df["temperature_ground"]
    )
    return df


def count_hot_hours(df, threshold=38):
    """Count hours where 2 m temperature exceeds a threshold."""
    return int((df["temperature_2m"] > threshold).sum())


def daily_summary(df):
    """Resample to daily means (temps/humidity) and daily sum (precip)."""
    daily_mean = df[["temperature_2m", "humidity_2m", "temperature_ground"]].resample(
        "D"
    ).mean()
    daily_precip = df[["precipitation"]].resample("D").sum()
    return daily_mean.join(daily_precip)


def main():
    print("=== Class 4 station-processing ===\n")

    raw = load_station(STATION_PATH)
    print(f"Loaded: {STATION_PATH.name}")
    print(f"  shape: {raw.shape}")
    print(f"  columns: {list(raw.columns)}")

    data = select_columns(raw, COLUMNS)
    data = add_gradient_column(data)

    n_hot = count_hot_hours(data)
    print(f"\nHours warmer than 38 °C: {n_hot}")

    print(f"\nMean 2 m temperature: {data['temperature_2m'].mean():.2f} °C")
    print(f"Mean gradient (2m − ground): {data['temp_gradient_2m_minus_ground'].mean():.2f} °C")

    daily = daily_summary(data)
    print(f"\nDaily resample: {daily.shape[0]} days")
    print(f"  First day mean 2 m temp: {daily['temperature_2m'].iloc[0]:.2f} °C")
    print(f"  First day precipitation: {daily['precipitation'].iloc[0]:.2f} mm")


if __name__ == "__main__":
    main()
