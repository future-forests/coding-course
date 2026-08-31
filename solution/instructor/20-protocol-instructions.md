# FF-MET-042 sampling protocol — instructor sheet (class of 20)

Give each student **one number**. In **Exercise C** (GitLab collaboration), they add **only their line** to the shared `protocol_staufen.md` via a Merge Request.

Starter file on GitLab (push before class):

```markdown
# FF-MET-042 sampling protocol

- Wind conditions: do not sample if wind > 10 m/s
- Sensor check: record battery level before each visit
```

---

## 1. Instructions to assign (one per student)

| # | Line to add to `protocol_staufen.md` |
| --- | --- |
| 1 | Rain events: do not sample during active precipitation; wait 30 min after rain stops |
| 2 | Sampling time: record start and end time (UTC) in the field log for every visit |
| 3 | GPS coordinates: note the exact sensor location at the start of each field season |
| 4 | Photos: take one photo of the station setup at each visit for documentation |
| 5 | Calibration: check the temperature sensor against a reference thermometer once per month |
| 6 | Data logger: download raw data within 48 h after each field visit |
| 7 | Vegetation: record mean vegetation height within 10 m of the mast at monthly intervals |
| 8 | Soil moisture: insert the probe at 10 cm depth, 2 m north of the mast |
| 9 | Precipitation gauge: empty the manual gauge at 09:00 UTC on sampling days |
| 10 | Wildlife: note any animal disturbance (tracks, damaged cables) in the field log |
| 11 | Cleaning: wipe the solar panel and rain gauge funnel if dirty or leaf-covered |
| 12 | Backup: copy the day's data to the shared uc3 folder before leaving the site |
| 13 | Incidents: report equipment failure or missing data to the group chat the same day |
| 14 | Site access: confirm landowner permission is valid before the first visit of the month |
| 15 | Safety: wear high-visibility vest and safety boots on site at all times |
| 16 | Turbulence: discard flux data when station instability (Δst) exceeds 0.05 |
| 17 | Night visits: avoid night sampling unless approved for a specific campaign |
| 18 | Data upload: upload processed files to GitLab within one week of collection |
| 19 | Frost: do not touch metal masts with bare hands when air temperature < 0 °C |
| 20 | Wind direction: note dominant wind direction during each 30 min sampling window |

---

## 2. Suggested branch names (Exercise C)

| # | Branch name example |
| --- | --- |
| 1 | `protocol/rain-events` |
| 2 | `protocol/sampling-time` |
| 3 | `protocol/gps-coordinates` |
| … | `protocol/` + short keyword from the instruction |

## 3. Suggested commit message template

```
Add protocol rule: [short keyword]
```

Example: `Add protocol rule: rain events`

## 4. Optional merge-conflict demo (pair students 1 and 16)

Both edit the **wind** line on different branches — student 1 adds rain rules on `main` while someone changes wind threshold on another branch. Or assign students **1** and **2** both a conflicting edit to the same starter line for a controlled conflict exercise.

**Conflict pair (advanced):** students **A** and **B** both receive:

> Change the wind line to: `Wind conditions: do not sample if wind > 8 m/s`

vs

> Change the wind line to: `Wind conditions: do not sample if wind > 12 m/s`

They must resolve the conflict in the MR.
