# Class 6 — debugging practice.
# Goal: find the longest heat spell = consecutive hours with
#        temperature_2m > 30 °C. Report start time and end time.

# %%
import matplotlib.pyplot as plt
import pandas as pd

# %%
DataPath = '../../processed_data/26030350_hourly.csv'
ThresholdC = 30

HartheimData = pd.read_csv(DataPath, parse_dates=['utc_time']).set_index('utc_time')
Temps = HartheimData['temperature_2m']

# %%
plt.plot(Temps.index, Temps)
plt.axhline(y=ThresholdC, color='red')
plt.xlabel('UTC time')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
BestLen, CurLen = 0, 0
BestStart, CurStart = None, None
BestEnd = None

for i, TempC in enumerate(Temps):
    if TempC > ThresholdC:
        if CurLen == 0:      # remember when this spell began
            CurStart = Temps.index[i]
        CurLen = CurLen + 1  # one more consecutive hot hour
    else:
        # temperature dropped: current spell (if any) has just ended
        if CurLen > BestLen:
            # this spell was longer than the best so far —> keep it
            BestLen, BestStart = CurLen, CurStart
            BestEnd = Temps.index[i - 1]  # last hot hour = hour before this cold one
        # clear current-spell counters so the next hot run starts fresh
        #CurLen = 0

print(f'Longest heat spell: {BestLen} hours')
print(f'Start: {BestStart}')
print(f'End:   {BestEnd}')

# %%
