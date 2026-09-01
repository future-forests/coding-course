"""Reproject FuFo predicted temperature from EPSG:25832 to WGS84 lon/lat.

Reads the full-domain hourly netCDF (ETRS89 / UTM zone 32N) and writes a
lon/lat (EPSG:4326) version for class use with xarray.

Usage (from repo root):
    pixi run python scripts/reproject_pred_temperature_to_wgs84.py

Expected runtime: several minutes for the full 744 x ~2400 x ~1250 grid,
depending on hardware. Output is typically a few GB on disk. Students should
use the processed file, not the raw UTM netCDF.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import rasterio
import xarray as xr
from rasterio.enums import Resampling
from rasterio.transform import Affine
from rasterio.warp import calculate_default_transform, reproject

INPUT_PATH = Path("raw_data/pred_temperature_C_2024_01.nc")
OUTPUT_PATH = Path("processed_data/pred_temperature_C_2024_01_wgs84.nc")
SOURCE_CRS = "EPSG:25832"
TARGET_CRS = "EPSG:4326"
VAR_NAME = "pred_temperature_C"
# Process this many timesteps per warp batch (memory vs speed trade-off).
BATCH_SIZE = 24


def source_transform_and_shape(x: np.ndarray, y: np.ndarray) -> tuple[Affine, int, int]:
    """Build a north-up Affine transform from 1D projected coordinates."""
    dx = float(x[1] - x[0])
    dy = float(y[1] - y[0])
    # Pixel centres → outer edges for rasterio.
    west = float(x[0]) - dx / 2.0
    # y may increase or decrease with index.
    if dy < 0:
        north = float(y[0]) - dy / 2.0
    else:
        # Flip to north-up for a stable destination grid.
        north = float(y[-1]) + dy / 2.0
        dy = -abs(dy)
    transform = Affine(dx, 0.0, west, 0.0, dy, north)
    return transform, len(y), len(x)


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH.resolve()}\n"
            "Place the raw netCDF under raw_data/ before running this script."
        )

    print(f"Opening {INPUT_PATH} ...", flush=True)
    with xr.open_dataset(INPUT_PATH) as ds_in:
        if VAR_NAME not in ds_in:
            raise KeyError(f"Expected variable {VAR_NAME!r} in {INPUT_PATH}")

        Temp = ds_in[VAR_NAME].load()
        x = Temp["x"].values.astype("float64")
        y = Temp["y"].values.astype("float64")
        # Ensure north-up source array (row 0 = north).
        if float(y[1] - y[0]) > 0:
            Temp = Temp.reindex(y=Temp.y[::-1])
            y = Temp["y"].values.astype("float64")

        src_transform, height, width = source_transform_and_shape(x, y)
        src_bounds = rasterio.transform.array_bounds(height, width, src_transform)
        dst_transform, dst_width, dst_height = calculate_default_transform(
            SOURCE_CRS,
            TARGET_CRS,
            width,
            height,
            *src_bounds,
        )

        # Destination lon/lat centres.
        # Affine: x = a*col + c, y = e*row + f  (b=d=0).
        cols = np.arange(dst_width)
        rows = np.arange(dst_height)
        lon_values = dst_transform.c + (cols + 0.5) * dst_transform.a
        lat_values = dst_transform.f + (rows + 0.5) * dst_transform.e

        n_times = Temp.sizes["time"]
        print(
            f"Input shape (time, y, x): {Temp.shape}\n"
            f"Output grid (lat, lon): ({dst_height}, {dst_width})\n"
            f"time range: {str(Temp.time.values[0])[:19]} → "
            f"{str(Temp.time.values[-1])[:19]}",
            flush=True,
        )

        out_data = np.full((n_times, dst_height, dst_width), np.nan, dtype="float32")
        src_nodata = np.nan

        for start in range(0, n_times, BATCH_SIZE):
            end = min(start + BATCH_SIZE, n_times)
            print(f"  reprojecting timesteps {start + 1}–{end}/{n_times} ...", flush=True)
            batch = np.asarray(Temp.isel(time=slice(start, end)).values, dtype="float32")
            # rasterio expects (bands, rows, cols)
            dst_batch = np.full(
                (end - start, dst_height, dst_width), np.nan, dtype="float32"
            )
            reproject(
                source=batch,
                destination=dst_batch,
                src_transform=src_transform,
                src_crs=SOURCE_CRS,
                dst_transform=dst_transform,
                dst_crs=TARGET_CRS,
                resampling=Resampling.bilinear,
                src_nodata=src_nodata,
                dst_nodata=np.nan,
            )
            out_data[start:end] = dst_batch

        TempWgs84 = xr.DataArray(
            out_data,
            dims=("time", "lat", "lon"),
            coords={
                "time": Temp["time"].values,
                "lat": ("lat", lat_values),
                "lon": ("lon", lon_values),
            },
            name=VAR_NAME,
            attrs={
                "standard_name": Temp.attrs.get("standard_name", "air_temperature"),
                "long_name": Temp.attrs.get(
                    "long_name", "predicted 2 metre air temperature"
                ),
                "units": Temp.attrs.get("units", "degree_Celsius"),
                "grid_mapping": "crs",
            },
        )

        DsOut = TempWgs84.to_dataset()
        DsOut["crs"] = xr.DataArray(
            0,
            attrs={
                "grid_mapping_name": "latitude_longitude",
                "epsg_code": TARGET_CRS,
                "semi_major_axis": 6378137.0,
                "inverse_flattening": 298.257223563,
            },
        )
        DsOut = DsOut.assign_attrs(
            {
                **{
                    k: v
                    for k, v in ds_in.attrs.items()
                    if k.lower() != "history" and isinstance(v, (str, int, float))
                },
                "title": ds_in.attrs.get(
                    "title", "Predicted temperature on 100 m grid"
                )
                + " (reprojected to WGS84 lon/lat)",
                "Conventions": "CF-1.8",
                "history": (
                    f"{ds_in.attrs.get('history', '')}; "
                    f"Reprojected from {SOURCE_CRS} to {TARGET_CRS} "
                    "with rasterio for FuFo coding course."
                ).strip("; "),
            }
        )

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        if OUTPUT_PATH.exists():
            OUTPUT_PATH.unlink()

        encoding = {
            VAR_NAME: {
                "zlib": True,
                "complevel": 4,
                "dtype": "float32",
                "_FillValue": np.float32(np.nan),
                "chunksizes": (24, min(256, dst_height), min(256, dst_width)),
            }
        }
        print(f"Writing {OUTPUT_PATH} ...", flush=True)
        DsOut.to_netcdf(OUTPUT_PATH, encoding=encoding)

        print(
            f"Output shape (time, lat, lon): {TempWgs84.shape}\n"
            f"  lon: {float(lon_values.min()):.4f} → {float(lon_values.max()):.4f}\n"
            f"  lat: {float(lat_values.min()):.4f} → {float(lat_values.max()):.4f}",
            flush=True,
        )

    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Saved: {OUTPUT_PATH} ({size_mb:.1f} MB)", flush=True)


if __name__ == "__main__":
    main()
