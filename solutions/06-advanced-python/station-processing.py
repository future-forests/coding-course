# Class 6 — station-processing script (Class 4 workflow).
# Same analysis as Class 4, as a .py file with # %% cells.
# Figures go to PNG with plt.savefig instead of plt.show().

# %%
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# Paths as plain strings
DataPath = '../../processed_data/26030350_hourly.csv'
FigDir = 'figures'  # PNGs land here when you run the script

# %%
# 1. Load CSV and set a datetime index
HartheimRaw = pd.read_csv(DataPath, parse_dates=['utc_time'])
HartheimRaw = HartheimRaw.set_index('utc_time')
# print(HartheimRaw.shape)
# print(HartheimRaw.columns)

# %%
# 2. Keep the columns used in Class 4
HartheimData = HartheimRaw[
    ['temperature_2m', 'humidity_2m', 'temperature_ground', 'precipitation']
].copy()
print(HartheimData.head(2))

# %%
# 3. Derived columns
HartheimData['temp_gradient_2m_minus_ground'] = (
    HartheimData['temperature_2m'] - HartheimData['temperature_ground']
)
HartheimData['deficit_humidity_2m'] = 100 - HartheimData['humidity_2m']
print(HartheimData.loc['2026-07-25 12:00:00', [
    'temperature_2m', 'temperature_ground', 'temp_gradient_2m_minus_ground'
]])

# %%
# 4. Exercise A — mean temperature in °C and °F (inline, as in Class 4)
MeanC = HartheimData['temperature_2m'].mean()
HartheimData['temperature_2m_f'] = HartheimData['temperature_2m'] * 9 / 5 + 32
MeanF = HartheimData['temperature_2m_f'].mean()
print(f'Mean 2 m temperature: {MeanC:.2f} °C / {MeanF:.2f} °F')

# %%
# 5. Filtering rows
NHot = len(HartheimData[HartheimData['temperature_2m'] > 38])
NCold = len(HartheimData[HartheimData['temperature_2m'] < 10])
WarmHumid = HartheimData[
    (HartheimData['temperature_2m'] > 25) & (HartheimData['humidity_2m'] > 60)
]
print(f'Hours > 38 °C: {NHot}')
print(f'Hours < 10 °C: {NCold}')
print(f'Warm and humid hours: {len(WarmHumid)}')

# %%
# 6. Resample to daily / weekly
DailyMean = HartheimData[['temperature_2m', 'humidity_2m']].resample('D').mean()
DailyPrecip = HartheimData[['precipitation']].resample('D').sum()
print(DailyMean.head(3))
print(DailyPrecip.head(3))
print(HartheimData[['temperature_2m']].resample('W').mean().head(3))
print(HartheimData[['precipitation']].resample('W').sum().head(3))

# %%
# 7. Exercise B — soil temperatures at two depths
SoilTemps = HartheimRaw[['soil_temperature_0_2', 'soil_temperature_0_6']]
print('Mean / std shallow (0.2 m):',
      SoilTemps['soil_temperature_0_2'].mean(),
      SoilTemps['soil_temperature_0_2'].std())
print('Mean / std deep (0.6 m):',
      SoilTemps['soil_temperature_0_6'].mean(),
      SoilTemps['soil_temperature_0_6'].std())

ShallowWarmer = SoilTemps['soil_temperature_0_2'] > SoilTemps['soil_temperature_0_6']
DeepWarmer = SoilTemps['soil_temperature_0_6'] > SoilTemps['soil_temperature_0_2']
print('Hours shallow warmer:', int(ShallowWarmer.sum()))
print('Hours deep warmer:', int(DeepWarmer.sum()))
print('UTC times when deep is warmer:')
print(SoilTemps.index[DeepWarmer])

# %%
# 8. Plots → PNG
os.makedirs(FigDir, exist_ok=True)

plt.plot(HartheimData.index, HartheimData['temperature_2m'], label='Temperature 2m')
plt.plot(HartheimData.index, HartheimData['temperature_ground'], label='Temperature ground')
plt.title('Hourly temperatures')
plt.xlabel('UTC time')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{FigDir}/temperatures.png')  # write file instead of plt.show()
plt.close()                                # free the figure; next cell starts clean
print(f'Saved {FigDir}/temperatures.png')

# %%
plt.plot(HartheimData.index, HartheimData['humidity_2m'])
plt.title('Humidity 2m')
plt.xlabel('UTC time')
plt.ylabel('Humidity 2m (%)')
plt.tight_layout()
plt.savefig(f'{FigDir}/humidity.png')
plt.close()
print(f'Saved {FigDir}/humidity.png')

# %%
# 9. Exercise C — VPD and stress hours (inline Tetens formula, as in Class 4)
HartheimData['es_kpa'] = 0.6108 * np.exp(
    17.27 * HartheimData['temperature_2m']
    / (HartheimData['temperature_2m'] + 237.3)
)
HartheimData['vpd_kpa'] = HartheimData['es_kpa'] * (1 - HartheimData['humidity_2m'] / 100)
print(f"Mean VPD: {HartheimData['vpd_kpa'].mean():.3f} kPa")
print(f"Min  VPD: {HartheimData['vpd_kpa'].min():.3f} kPa")
print(f"Max  VPD: {HartheimData['vpd_kpa'].max():.3f} kPa")
print('Time of maximum VPD:',
      HartheimData.index[HartheimData['vpd_kpa'] == HartheimData['vpd_kpa'].max()])

StressMask = HartheimData['vpd_kpa'] > 3
print(f'Stressful hours (VPD > 3 kPa): {int(StressMask.sum())}')

# %%
plt.plot(HartheimData.index, HartheimData['vpd_kpa'], label='VPD')
plt.axhline(y=3, color='red', linestyle='--', label='Stress threshold (3 kPa)')
plt.xlabel('UTC time')
plt.ylabel('VPD (kPa)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{FigDir}/vpd.png')
plt.close()
print(f'Saved {FigDir}/vpd.png')

# %%
# Warmest day (mean T) vs most stressful day (max VPD)
DailyMeanTemp = HartheimData[['temperature_2m']].resample('D').mean()
DailyMaxVpd = HartheimData[['vpd_kpa']].resample('D').max()
MaxTemp = DailyMeanTemp['temperature_2m'].max()
MaxDailyVpd = DailyMaxVpd['vpd_kpa'].max()
print('Warmest day (mean T):',
      DailyMeanTemp.index[DailyMeanTemp['temperature_2m'] == MaxTemp])
print('Most stressful day (max VPD):',
      DailyMaxVpd.index[DailyMaxVpd['vpd_kpa'] == MaxDailyVpd])
