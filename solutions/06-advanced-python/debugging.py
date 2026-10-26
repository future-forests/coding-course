# Class 6 — debugging practice (intentional bug).
# Goal: report how many hours are warmer than 38 °C at 2 m,
#        and the mean 2 m temperature on those hot hours.
#
# Run this file. The numbers look wrong — use print() to trace where.

# %%
import pandas as pd

# %%
DataPath = '../../processed_data/26030350_hourly.csv'

HartheimRaw = pd.read_csv(DataPath, parse_dates=['utc_time'])
HartheimRaw = HartheimRaw.set_index('utc_time')

HartheimData = HartheimRaw[
    ['temperature_2m', 'humidity_2m', 'temperature_ground', 'precipitation']
].copy()

# %%
# --- buggy analysis ---
# BUG (find it by printing): wrong column used in the filter
HotHours = HartheimData[HartheimData['temperature_ground'] > 38]
NHot = len(HotHours)
MeanHot = HotHours['temperature_2m'].mean()

print(f'Hours warmer than 38 °C: {NHot}')
print(f'Mean 2 m temperature on those hours: {MeanHot:.2f} °C')
