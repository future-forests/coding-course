"""Class 6 — Advanced Python: profiling.

The same garden-temperature exercise from Classes 3a and 3b, timed so
you can see the cost of each approach.

Task (identical in all three classes):
- store five garden temperatures: 20.4, 20.8, 21.1, 20.3, 21.2 °C
- compute the average in °C
- convert every value to °F for your American cousin
- compute the average in °F
"""

import statistics as stat
import time

import numpy as np

TempsC = [20.4, 20.8, 21.1, 20.3, 21.2]


print("Part 1 — Original exercise (5 locations)")
print()

# Class 3a: one variable per measurement, convert each by hand
Start = time.perf_counter()

TempStat1 = 20.4
TempStat2 = 20.8
TempStat3 = 21.1
TempStat4 = 20.3
TempStat5 = 21.2

AvgTempC = stat.mean([TempStat1, TempStat2, TempStat3, TempStat4, TempStat5])

TempStatF1 = TempStat1 * 9 / 5 + 32
TempStatF2 = TempStat2 * 9 / 5 + 32
TempStatF3 = TempStat3 * 9 / 5 + 32
TempStatF4 = TempStat4 * 9 / 5 + 32
TempStatF5 = TempStat5 * 9 / 5 + 32

AvgTempF = stat.mean([TempStatF1, TempStatF2, TempStatF3, TempStatF4, TempStatF5])

Elapsed3a = time.perf_counter() - Start
print(f"Average (°C): {AvgTempC}")
print(f"Average (°F): {AvgTempF}")
print(f"Class 3a — one variable per location: {Elapsed3a:.6f} s")
print()

# Class 3b: NumPy array + for loop (Exercise A)
Start = time.perf_counter()

TempGardenC = np.array(TempsC)

AvgTempC = stat.mean(TempGardenC)

TempGardenF = np.zeros(np.size(TempGardenC))
for i in range(np.size(TempGardenC)):
    TempGardenF[i] = TempGardenC[i] * 9 / 5 + 32

AvgTempF = stat.mean(TempGardenF)

Elapsed3bLoop = time.perf_counter() - Start
print(f"Average (°C): {AvgTempC}")
print(f"Average (°F): {AvgTempF}")
print(f"Class 3b — array + for loop:          {Elapsed3bLoop:.6f} s")
print()

# Class 3b: vectorisation (Exercise E)
Start = time.perf_counter()

TempGardenC = np.array(TempsC)

AvgTempC = np.mean(TempGardenC)
TempGardenF = TempGardenC * 9 / 5 + 32
AvgTempF = np.mean(TempGardenF)

Elapsed3bVec = time.perf_counter() - Start
print(f"Average (°C): {AvgTempC}")
print(f"Average (°F): {AvgTempF}")
print(f"Class 3b — vectorisation:             {Elapsed3bVec:.6f} s")
print()

print("With only 5 numbers, all three finish in a fraction of a millisecond.")
print("Class 3a cannot even be written for a large dataset: you would need")
print("one named variable per measurement. The next part repeats the same")
print("five values a million times, and times only the approaches that scale.")
print()

print("Part 2 — Same conversion, 1 000 000 measurements")
print()

NRepeat = 200_000
TempGardenC = np.tile(TempsC, NRepeat)  # 1 000 000 values, same five readings
N = np.size(TempGardenC)

# Class 3b: NumPy array + for loop
Start = time.perf_counter()
TempGardenF = np.zeros(N)
for i in range(N):
    TempGardenF[i] = TempGardenC[i] * 9 / 5 + 32
AvgTempF = np.mean(TempGardenF)
Elapsed3bLoopLarge = time.perf_counter() - Start
print(f"Average (°F): {AvgTempF}")
print(f"Class 3b — array + for loop:          {Elapsed3bLoopLarge:.4f} s")

# Class 3b: vectorisation
Start = time.perf_counter()
TempGardenF = TempGardenC * 9 / 5 + 32
AvgTempF = np.mean(TempGardenF)
Elapsed3bVecLarge = time.perf_counter() - Start
print(f"Average (°F): {AvgTempF}")
print(f"Class 3b — vectorisation:             {Elapsed3bVecLarge:.4f} s")
print()
print(
    f"Vectorisation is {Elapsed3bLoopLarge / Elapsed3bVecLarge:.0f}× faster "
    "than the for-loop on 1 000 000 values."
)
