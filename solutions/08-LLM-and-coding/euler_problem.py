# Script to solve Euler problem from class 06

# Problem
# Apply Euler to a temperate pine stand with $L = 2.5$, $k = 0.25$ (close to Olson's pine example), starting from a low litter stock after disturbance (2.0). Calculate the Litterfall carbon of the system for the next 20 years and plot your result.

# Tasks in plain English
# 1. store the model parameters (litterfall, decay rate, initial stock, time-step, number of steps)
# 2. prepare a place to keep the litter carbon stock for every year, and put the initial stock in the first year
# 3. for each year: compute how fast the stock changes, then step forward to the next year with Euler
# 4. build the list of years and plot litter carbon against time

# Pseudocode
# 1. Set litterfall L=2.5, decay k=0.25, initial stock C0=2.0, time-step dt=1, number of steps NSteps=20
# 2. Create an empty array LitterC of length NSteps + 1
#    put C0 in the first slot of LitterC
# 3. create function rate = litterfall minus decay times current stock
#    Loop over each year n (all years except the last)
#    next stock = current stock + dt times rate
# 4. Plot Years against LitterC
#    create Years from 0 to NSteps (multiplied by dt)
#    Add labels and title