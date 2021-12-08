# Student Edition of PMDC Control - CL Response
# 11/27

# Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.close('all')

# %% Read CSV File and collect data

#---------------------------
# Import file and read data
#---------------------------
filename     = 'Demonstration_2.csv'  

data = pd.read_csv(filename)

# dataNames = ['Time', 'wm_ref', 'wm','PWM']
time    = np.array(data.Time)   # [s]
wm_ref  = np.array(data.wm_ref) # [rad/s]
wm_exp  = np.array(data.wm)     # [rad/s]
PWM     = np.array(data.PWM)    # [int]

# Raw Data Figures
plt.figure()
plt.plot(time, wm_ref, label='$\omega_{m, ref}$ [rad/s]')
plt.plot(time, wm_exp, label='$\omega_m$ [rad/s]')
plt.step(time,PWM,label='PWM [Int]')
plt.title("Raw Data: Motor Speed and PWM output vs Time")
plt.grid()
plt.legend()
plt.ylabel("Amplitude")
plt.xlabel("Time [s]")



#----------------------------------------------------------------------
# Speed Control Results
# 
# Calculate error and plot over time
# Can use this plot to tabulate error for each wm_ref value
# Remember: wm_ref values are set in DAQ code using variable 'wm_ref_vals'
#----------------------------------------------------------------------

# Calculate Error
wm_error = wm_ref - wm_exp

# Plot Error vs Time
plt.figure()
plt.plot(time, wm_error, label='$\omega_{m}$ error [rad/s]')
plt.step(time,PWM,label='PWM [int]')
plt.title("OL Speed Control Error and PWM output vs Time")
plt.grid()
plt.legend()
plt.ylabel("Amplitude")
plt.xlabel("Time [s]")
plt.show()




















