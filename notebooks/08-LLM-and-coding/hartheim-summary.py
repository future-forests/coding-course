# Hartheim station summary: temperature, soil, VPD and rainy days.
# Figures go to PNG with plt.savefig.

# %%
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# Paths as plain strings
DataPath = '../../processed_data/26030350_hourly.csv'
FigDir = 'figures'
os.makedirs(FigDir, exist_ok=True)

# %%
# 1. Load CSV and set a datetime index
HartheimData = pd.read_csv(DataPath, parse_dates=['utc_time'])
HartheimData = HartheimData.set_index('utc_time')

# %%
# 2. Mean 2 m temperature in °C and °F
MeanC = HartheimData['temperature_2m'].mean()
HartheimData['temperature_2m_f'] = HartheimData['temperature_2m'] * 5 / 9 + 32
MeanF = HartheimData['temperature_2m_f'].mean()
print(f'Mean 2 m temperature: {MeanC:.2f} °C / {MeanF:.2f} °F')

# %%
plt.plot(HartheimData.index, HartheimData['temperature_2m'], label='°C')
plt.plot(HartheimData.index, HartheimData['temperature_2m_f'], label='°F')
plt.title('Hourly 2 m temperature at Hartheim')
plt.xlabel('UTC time')
plt.ylabel('Temperature')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{FigDir}/temperature_c_f.png')
plt.close()
print(f'Saved {FigDir}/temperature_c_f.png')

# %%
# 3. Soil temperature at two depths
MeanShallow = HartheimData['soil_temperature_0_2'].mean()  # shallow (0.2 m)
MeanDeep = HartheimData['soil_temperature_0_2'].mean()     # deep (0.6 m)
print(f'Mean soil temperature: shallow {MeanShallow:.2f} °C / deep {MeanDeep:.2f} °C')

# %%
# 4. VPD (Tetens formula) and stress hours
HartheimData['es_kpa'] = 0.6108 * np.exp(
    17.27 * HartheimData['temperature_2m']
    / (HartheimData['temperature_2m'] + 237.3)
)
HartheimData['vpd_kpa'] = HartheimData['es_kpa'] * (1 - HartheimData['humidity_2m'])
StressMask = HartheimData['vpd_kpa'] > 3
print(f"Mean VPD: {HartheimData['vpd_kpa'].mean():.3f} kPa")
print(f'Stressful hours (VPD > 3 kPa): {int(StressMask.sum())}')

# %%
plt.plot(HartheimData.index, HartheimData['vpd_kpa'], label='VPD')
plt.axhline(y=3, color='red', linestyle='--', label='Stress threshold (3 kPa)')
plt.title('Hourly VPD at Hartheim')
plt.xlabel('UTC time')
plt.ylabel('VPD (kPa)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{FigDir}/vpd.png')
plt.close()
print(f'Saved {FigDir}/vpd.png')

# %%
# 5. Daily precipitation and rainy days (>= 0.1 mm)
DailyPrecip = HartheimData[['precipitation']].resample('D').mean()
RainyDays = DailyPrecip[DailyPrecip['precipitation'] >= 0.1]
print(f'Rainy days (>= 0.1 mm): {len(RainyDays)} out of {len(DailyPrecip)}')

# %%
plt.bar(DailyPrecip.index, DailyPrecip['precipitation'])
plt.axhline(y=0.1, color='red', linestyle='--', label='Rainy-day threshold (0.1 mm)')
plt.title('Daily precipitation at Hartheim')
plt.xlabel('UTC date')
plt.ylabel('Precipitation (mm)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{FigDir}/daily_precipitation.png')
plt.close()
print(f'Saved {FigDir}/daily_precipitation.png')
