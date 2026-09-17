"""Class 6 — solution: process multiple netCDF files with functions.

Refactors post-processing.py into reusable functions and loops over
several input files (e.g. two halves of January).
"""

from pathlib import Path

import xarray as xr

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "processed_data"
TEMP_PATH = DATA_DIR / "pred_temperature_C_2024_01_wgs84.nc"
MASK_PATH = DATA_DIR / "freiburg_city_mask.nc"
CHUNK_DIR = Path(__file__).resolve().parent / "_exercise_chunks"

HARTHEIM_LON, HARTHEIM_LAT = 7.60, 47.93


def load_temperature(data_path):
    temp_ds = xr.open_dataset(data_path, chunks="auto")
    return temp_ds["pred_temperature_C"]


def freiburg_box(temp):
    return temp.sel(
        lon=slice(7.5, 8.1),
        lat=slice(48.15, 47.75),
    )


def spatial_mean_series(temp_box):
    return temp_box.mean(dim=("lat", "lon"))


def daily_mean(series):
    return series.resample(time="1D").mean()


def urban_heat_island_stats(temp, city_mask):
    city_series = temp.where(city_mask).mean(dim=("lat", "lon"))
    rural_series = temp.where(city_mask == False).mean(dim=("lat", "lon"))
    diff_series = city_series - rural_series
    sign_diff = diff_series > 1
    return {
        "city_series": city_series,
        "rural_series": rural_series,
        "diff_series": diff_series,
        "n_hours_warmer_than_1c": int(sign_diff.sum()),
        "pct_hours_warmer_than_1c": 100 * float(sign_diff.sum()) / sign_diff.size,
    }


def process_netcdf(data_path, city_mask_path):
    """Process one netCDF file and return a summary dictionary."""
    temp = load_temperature(data_path)
    city_mask = xr.open_dataarray(city_mask_path)

    hartheim_series = temp.sel(
        lon=HARTHEIM_LON, lat=HARTHEIM_LAT, method="nearest"
    )
    box = freiburg_box(temp)
    daily = daily_mean(spatial_mean_series(box))
    uhi = urban_heat_island_stats(temp, city_mask)

    summary = {
        "path": str(data_path),
        "hartheim_mean_c": float(hartheim_series.mean()),
        "daily_spatial_mean": daily,
        "uhi_stats": uhi,
    }

    temp.close()
    city_mask.close()
    return summary


def make_exercise_chunks(source_path, output_dir):
    """Split January into two netCDF chunks for the multi-file exercise."""
    output_dir.mkdir(exist_ok=True)
    temp = xr.open_dataset(source_path)
    chunk1_path = output_dir / "jan_2024_part1.nc"
    chunk2_path = output_dir / "jan_2024_part2.nc"
    temp.sel(time=slice("2024-01-01", "2024-01-15")).to_netcdf(chunk1_path)
    temp.sel(time=slice("2024-01-16", "2024-01-31")).to_netcdf(chunk2_path)
    temp.close()
    return [chunk1_path, chunk2_path]


def main():
    chunk_paths = make_exercise_chunks(TEMP_PATH, CHUNK_DIR)

    results = []
    for path in chunk_paths:
        print(f"Processing {path.name}...")
        summary = process_netcdf(path, MASK_PATH)
        results.append(summary)
        print(f"  Hartheim mean: {summary['hartheim_mean_c']:.2f} °C")
        print(f"  UHI hours > 1 °C: {summary['uhi_stats']['n_hours_warmer_than_1c']}")
        print(f"  UHI share: {summary['uhi_stats']['pct_hours_warmer_than_1c']:.1f} %")
        print()

    print(f"Processed {len(results)} file(s).")


if __name__ == "__main__":
    main()
