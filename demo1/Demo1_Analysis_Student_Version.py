import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#plt.close('all') # close all plots

# --------------------------------------
# Load and select data
# --------------------------------------
# To load data from two files at once, you will need to make new variables

# Demo_test_100uF
fileName = "Demo_test_100uF_charge.csv"
fileName2 = "Demo_test_100uF_discharge.csv"

# Read csv file
data = pd.read_csv(fileName)
data2 = pd.read_csv(fileName2)

# Extract data from dataframe
t  = np.array(data.Time)
v1 = np.array(data.V1)
v2 = np.array(data.V2)

t_2  = np.array(data2.Time)
v1_2 = np.array(data2.V1)
v2_2 = np.array(data2.V2)

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

R =  10000# Ohms
C =  100 * 10**-6 # Farads
Tau = R*C# Time constant [s]

Vs = 5 # Supply voltage [V]

# Will need different variables for charging and discharging
VT_charge = Vs*0.63 # expected voltage at t = one time constant past step input [V]
VT_discharge = Vs*(1-.63)

T_step_charge = 2.519044000000001 # Step input time [s]

T_tau_charge = T_step_charge+Tau# t = one time constant past step input [s]

T_step_discharge = 2.5698820000000007 # Step input time [s]

T_tau_discharge = T_step_discharge+Tau# t = one time constant past step input [s]


# --------------------------------------
# Plots
# --------------------------------------
# To plot on single figure from multiple datasets, use plt.subplots

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.tight_layout()

ax1.plot(t, v1, label = "Input Voltage") # plot capacitor voltage
ax1.plot(t, v2, label = "Vc") # plot input voltage
ax1.plot(T_tau_charge, VT_charge, 'rx', label = "Expected Tau Voltage")

ax2.plot(t_2, v1_2, label = "Input Voltage") # plot capacitor voltage
ax2.plot(t_2, v2_2, label = "Vc") # plot input voltage
ax2.plot(T_tau_discharge, VT_discharge, 'rx', label = "Expected Tau Voltage")

# plot expceted voltage at time constant
# can be a single point or horizontal and vertial lines as in example figure
# for horizontal or vertical lines, look up documentation for vlines and hlines

ax1.grid()
ax1.legend()
ax1.title.set_text('Capacitor Charge Voltage vs Time')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Voltage (V)')

ax2.grid()
ax2.legend()
ax2.title.set_text('Capacitor Discharge Voltage vs Time')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Voltage (V)')

plt.show()