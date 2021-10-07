import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.close('all') # close all plots

# --------------------------------------
# Load and select data
# --------------------------------------
# To load data from two files at once, you will need to make new variables

# Demo_test_100uF
fileName = "Demo_test_100uF_charge.csv"
# fileName2 = "Demo_test_100uF_discharge.csv"

# Read csv file
data = pd.read_csv(fileName)

# Extract data from dataframe
t  = np.array(data.Time)
v1 = np.array(data.V1)
v2 = np.array(data.V2)

# Get data at times of interest
T1,T2 = 0, t[-1]
it1 = np.nonzero(t > T1)[0][0]
it2 = np.nonzero(t < T2)[0][-1]

T  = t[it1:it2] - t[it1] # Resets time to zero seconds
V1 = v1[it1:it2]
V2 = v2[it1:it2]

# --------------------------------------
# Data analysis
# --------------------------------------

R =  # Ohms
C =  # Farads
Tau = # Time constant [s]

Vs = 5 # Supply voltage [V]

# Will need different variables for charging and discharging
VT =   # expected voltage at t = one time constant past step input [V]

T_step =  # Step input time [s]

T_tau = # t = one time constant past step input [s]



# --------------------------------------
# Plots
# --------------------------------------
# To plot on single figure from multiple datasets, use plt.subplots

plt.plot() # plot capacitor voltage
plt.plot() # plot input voltage

# plot expceted voltage at time constant
# can be a single point or horizontal and vertial lines as in example figure
# for horizontal or vertical lines, look up documentation for vlines and hlines

plt.grid()
plt.legend()
plt.title('')
plt.xlabel('')
plt.ylabel('')