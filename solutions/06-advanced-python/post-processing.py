"""Class 6 — post-processing script (Class 5 workflow).

Linear script version of the Class 5 geospatial analysis:
open netCDF → Hartheim point series → Freiburg box → spatial mean →
daily resample → urban heat island stats (Exercise D).
"""

from pathlib import Path

import xarray as xr

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "processed_data"
TEMP_PATH = DATA_DIR / "pred_temperature_C_2024_01_wgs84.nc"
MASK_PATH = DATA_DIR / "freiburg_city_mask.nc"

HARTHEIM_LON, HARTHEIM_LAT = 7.60, 47.93


def load_temperature(data_path):
    """Open a netCDF file and return the temperature DataArray."""
    temp_ds = xr.open_dataset(data_path, chunks="auto")
    return temp_ds["pred_temperature_C"]


def freiburg_box(temp):
    """Select the Freiburg–Hartheim region."""
    return temp.sel(
        lon=slice(7.5, 8.1),
        lat=slice(48.15, 47.75),
    )


def spatial_mean_series(temp_box):
    """Collapse lat and lon → one value per time step."""
    return temp_box.mean(dim=("lat", "lon"))


def daily_mean(series):
    """Resample an hourly series to daily means."""
    return series.resample(time="1D").mean()


def urban_heat_island_stats(temp, city_mask):
    """Compare city vs countryside spatial means (Exercise D)."""
    city_only = temp.where(city_mask)
    city_series = city_only.mean(dim=("lat", "lon"))

    rural_only = temp.where(city_mask == False)
    rural_series = rural_only.mean(dim=("lat", "lon"))

    diff_series = city_series - rural_series
    sign_diff = diff_series > 1
    n_hours = int(sign_diff.sum())
    total_hours = sign_diff.size
    pct_hours = 100 * n_hours / total_hours

    return {
        "city_series": city_series,
        "rural_series": rural_series,
        "diff_series": diff_series,
        "n_hours_warmer_than_1c": n_hours,
        "pct_hours_warmer_than_1c": pct_hours,
    }


def main():
    print("=== Class 5 post-processing ===\n")

    temp = load_temperature(TEMP_PATH)
    print(f"Opened: {TEMP_PATH.name}")
    print(f"  dims: {temp.dims}, shape: {temp.shape}")

    # Hartheim point series
    hartheim_series = temp.sel(
        lon=HARTHEIM_LON, lat=HARTHEIM_LAT, method="nearest"
    )
    print(f"\nHartheim January mean: {float(hartheim_series.mean()):.2f} °C")

    # Freiburg box → spatial mean → daily
    box = freiburg_box(temp)
    box_series = spatial_mean_series(box)
    daily = daily_mean(box_series)
    print(f"Freiburg box spatial mean (first day): {float(daily[0]):.2f} °C")
    print(f"Freiburg box spatial mean (last day):  {float(daily[-1]):.2f} °C")

    # Value mask example
    n_warm = int((temp > 5).sum())
    print(f"\nCells warmer than 5 °C (all timesteps): {n_warm:,}")

    # Geographic mask + urban heat island
    in_freiburg = xr.open_dataarray(MASK_PATH)
    uhi = urban_heat_island_stats(temp, in_freiburg)
    print(f"\nUrban heat island (city − countryside > 1 °C):")
    print(f"  Hours: {uhi['n_hours_warmer_than_1c']} / {uhi['diff_series'].size}")
    print(f"  Share: {uhi['pct_hours_warmer_than_1c']:.1f} %")

    temp.close()
    in_freiburg.close()


if __name__ == "__main__":
    main()
