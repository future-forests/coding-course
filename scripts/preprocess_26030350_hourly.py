"""Clean and resample logger data to hourly frequency.

Usage:
    python scripts/preprocess_26030350_hourly.py
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

INPUT_PATH = Path("raw_data/26030350.csv")
OUTPUT_PATH = Path("processed_data/26030350_hourly.csv")
NO_DATA_SENTINEL = -0.0065535


def normalize_column_name(name: str) -> str:
    """Convert raw column names to snake_case and standardize depth notation."""
    normalized = name.strip().lower()
    normalized = normalized.replace(",", ".")
    normalized = normalized.replace("-", "_")
    normalized = re.sub(r"\s+", "_", normalized)
    normalized = re.sub(r"[^a-z0-9_.]+", "", normalized)
    normalized = normalized.replace(".", "_")
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized


def nan_safe_sum(series: pd.Series) -> float:
    """Sum values but keep NaN when no valid values are present."""
    return series.sum(min_count=1)


def build_agg_map(columns: list[str]) -> dict[str, str | callable]:
    """Choose simple, explicit hourly aggregations per variable."""
    agg_map: dict[str, str | callable] = {}

    for col in columns:
        if col == "logger_id":
            agg_map[col] = "last"
        elif col == "packet_count":
            agg_map[col] = "max"
        elif col == "gust_speed":
            agg_map[col] = "max"
        elif col == "precipitation":
            agg_map[col] = nan_safe_sum
        elif col in {"battery_v", "signal_quality", "info_byte", "wind_direction"}:
            agg_map[col] = "mean"
        else:
            agg_map[col] = "mean"

    return agg_map


def main() -> None:
    df = pd.read_csv(INPUT_PATH, parse_dates=["UTC_Time"])
    df = df.rename(columns={col: normalize_column_name(col) for col in df.columns})

    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    data_columns = [col for col in numeric_columns if col != "logger_id"]

    # Replace sensor no-data sentinel with NaN while preserving true zeros.
    for col in data_columns:
        series = df[col]
        df[col] = series.mask(np.isclose(series, NO_DATA_SENTINEL, atol=1e-9))

    df = df.set_index("utc_time").sort_index()
    agg_map = build_agg_map(df.columns.tolist())
    hourly = df.resample("h").agg(agg_map)
    hourly.index.name = "utc_time"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    hourly.to_csv(OUTPUT_PATH)

    print(f"Saved hourly dataset to: {OUTPUT_PATH}")
    print(f"Rows: {len(hourly)} | Columns: {len(hourly.columns)}")


if __name__ == "__main__":
    main()
