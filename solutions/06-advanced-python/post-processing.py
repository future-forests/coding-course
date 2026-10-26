# Class 6 — post-processing script (Class 5a workflow).
# Same idea as station-processing.py: Class 5a as a .py file with # %% cells.
# Figures go to PNG with plt.savefig instead of plt.show().

# %%
import os

import matplotlib.pyplot as plt
import xarray as xr

# %%
DataPath = '../../processed_data/pred_temperature_C_2024_01_wgs84.nc'
MaskPath = '../../processed_data/freiburg_city_mask.nc'
ElevPath = '../../processed_data/elevation_m_wgs84.nc'
FigDir = 'figures'

HartheimLon = 7.60
HartheimLat = 47.93

os.makedirs(FigDir, exist_ok=True)

# %%
# 1. Open netCDF and extract pred_temperature_C
TempDs = xr.open_dataset(filename_or_obj=DataPath, chunks='auto')
Temp = TempDs['pred_temperature_C']
print(Temp.dims, Temp.shape)

# %%
# 2. Hartheim point series
HartheimSeries = Temp.sel(lon=HartheimLon, lat=HartheimLat, method='nearest')
print(f'Hartheim January mean: {float(HartheimSeries.mean()):.2f} °C')

# %%
# 3. Freiburg box → spatial mean → daily resample
FreiburgBox = Temp.sel(lon=slice(7.5, 8.1), lat=slice(48.15, 47.75))
BoxSeries = FreiburgBox.mean(dim=('lat', 'lon'))
Daily = BoxSeries.resample(time='1D').mean()
print(f'Freiburg box spatial mean (first day): {float(Daily[0]):.2f} °C')
print(f'Freiburg box spatial mean (last day):  {float(Daily[-1]):.2f} °C')

# %%
# 4. Exercise A — latitudinal mean
BoxLatitudinalMean = FreiburgBox.mean(dim=('lon', 'time'))
print(BoxLatitudinalMean.dims)

plt.plot(BoxLatitudinalMean, BoxLatitudinalMean.lat)
plt.ylabel('Latitude')
plt.xlabel('Temperature (°C)')
plt.title('Freiburg–Hartheim box, latitudinal mean')
plt.tight_layout()
plt.savefig(f'{FigDir}/latitudinal_mean.png')
plt.close()
print(f'Saved {FigDir}/latitudinal_mean.png')

# %%
# 5. Value mask (Temp > 5)
WarmCells = Temp.where(Temp > 5)
NWarm = int((Temp > 5).sum())
print(f'Cells warmer than 5 °C (all timesteps): {NWarm:,}')

WarmMap = WarmCells.sel(time='2024-01-18T12:00')
plt.pcolormesh(WarmMap.lon, WarmMap.lat, WarmMap, cmap='YlOrRd')
plt.colorbar(label='Temperature (°C)')
plt.title('Cells warmer than 5 °C (example timestep)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(f'{FigDir}/warm_cells.png')
plt.close()
print(f'Saved {FigDir}/warm_cells.png')

# %%
# 6. Exercise B — frozen cells on a logging day
CollectWoodDate = Temp.sel(
    lon=slice(7.5, 8.1), lat=slice(48.15, 47.75)
).sel(time='2024-01-20T14:00', method='nearest')
BelowZero = CollectWoodDate.where(CollectWoodDate < 0)

plt.pcolormesh(BelowZero.lon, BelowZero.lat, BelowZero, cmap='Blues_r')
plt.colorbar(label='Temperature (°C)')
plt.title('20 Jan 14:00, cells below 0 °C')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(f'{FigDir}/frozen_cells.png')
plt.close()
print(f'Saved {FigDir}/frozen_cells.png')

# %%
# 7. Exercise C — urban heat island (city vs countryside)
InFreiburg = xr.open_dataarray(MaskPath)

CitySeries = Temp.where(InFreiburg).mean(dim=('lat', 'lon'))
RuralSeries = Temp.where(InFreiburg == False).mean(dim=('lat', 'lon'))
CityDaily = CitySeries.resample(time='1D').mean()
RuralDaily = RuralSeries.resample(time='1D').mean()

plt.plot(CityDaily.time, CityDaily, label='Inside Freiburg')
plt.plot(RuralDaily.time, RuralDaily, label='Outside Freiburg')
plt.ylabel('Temperature (°C)')
plt.title('Daily mean temperature, January 2024')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(f'{FigDir}/city_vs_rural.png')
plt.close()
print(f'Saved {FigDir}/city_vs_rural.png')

# %%
DiffSeries = CitySeries - RuralSeries
SignDiff = DiffSeries > 1
NHours = int(SignDiff.sum())
PctHours = 100 * NHours / SignDiff.size
print(f'Urban heat island (city − countryside > 1 °C):')
print(f'  Hours: {NHours} / {SignDiff.size}')
print(f'  Share: {PctHours:.1f} %')

plt.plot(DiffSeries.time, DiffSeries)
plt.axhline(y=0, color='grey', linestyle='--')
plt.ylabel('City − countryside (°C)')
plt.title('Urban heat island intensity, hourly')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{FigDir}/uhi_intensity.png')
plt.close()
print(f'Saved {FigDir}/uhi_intensity.png')

# %%
# 8. Exercise D (Class 5a) — valley vs ridges with DEM
Elev = xr.open_dataarray(ElevPath)
ElevBox = Elev.sel(lon=slice(7.6, 8.1), lat=slice(48.15, 47.75))

plt.pcolormesh(ElevBox.lon, ElevBox.lat, ElevBox, cmap='Greys_r')
plt.colorbar(label='Elevation (m)')
plt.title('Elevation around Freiburg')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(f'{FigDir}/elevation.png')
plt.close()
print(f'Saved {FigDir}/elevation.png')

# %%
ValleyMask = ElevBox < 600
RidgesMask = ElevBox > 900

plt.pcolormesh(ElevBox.lon, ElevBox.lat, ElevBox.where(ValleyMask), cmap='Blues')
plt.pcolormesh(ElevBox.lon, ElevBox.lat, ElevBox.where(RidgesMask), cmap='Reds')
plt.title('Valleys (< 600 m, blue) and ridges (> 900 m, red)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(f'{FigDir}/valley_ridges_mask.png')
plt.close()
print(f'Saved {FigDir}/valley_ridges_mask.png')

# %%
TempBox = Temp.sel(lon=slice(7.6, 8.1), lat=slice(48.15, 47.75))
ValleyDaily = TempBox.where(ValleyMask).mean(dim=('lat', 'lon')).resample(time='1D').mean()
RidgesDaily = TempBox.where(RidgesMask).mean(dim=('lat', 'lon')).resample(time='1D').mean()

plt.plot(ValleyDaily.time, ValleyDaily, label='Valley (< 600 m)')
plt.plot(RidgesDaily.time, RidgesDaily, label='Ridges (> 900 m)')
plt.ylabel('Temperature (°C)')
plt.title('Daily mean temperature — valley vs ridges, January 2024')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(f'{FigDir}/valley_vs_ridges.png')
plt.close()
print(f'Saved {FigDir}/valley_vs_ridges.png')

# %%
TempDs.close()
InFreiburg.close()
Elev.close()
