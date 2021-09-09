#-----------------------------------------------------------------
# Import Required Packages
#-----------------------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean
from scipy.signal import find_peaks
import math


#-----------------------------------------------------------------
#-----------------------------------------------------------------
# When reading from your own data:
#    --> Go to File and Open 
#    --> Open CSV file in Python and rename first row variables: Time,omegax,omegay,omegaz,omegaa
#    --> Then save and close the CSV file
#-----------------------------------------------------------------
#-----------------------------------------------------------------
filename  = 'raw_data.csv' # Update filename with your own data file


#-----------------------------------------------------------------
# Bifilar Pendulum variables
# Fill in Bifilar and phone dimensions
# Based on Ogata PDF variable names
#-----------------------------------------------------------------
h = 0.7112 # [m],  bifilar string length
a = 0.0445 # [m],  length between files/2
L = 0.1447 # [m],  length of phone (horizontal --> parallel to ground)
t = 0.008 # [m],  thickness of phone
m = 0.151 # [kg], phone mass

#-----------------------------------------------------------------
# Read CSV file and index the columns using the renamed column header names
#-----------------------------------------------------------------
csvdata   = pd.read_csv(filename)

T  = csvdata.Time
wx = csvdata.omegax
wy = csvdata.omegay
wz = csvdata.omegaz
    
#-----------------------------------------------------------------
# Plot raw data: wx, wy, and wz versus Time [s]
# --> Use this to find the time values where your oscillation begins/ends
#----------------------------------------------------------------- 
plt.figure(1)
plt.plot(T, wx)
plt.plot(T, wy)
plt.plot(T, wz)
plt.xlabel("Time (s)")
plt.ylabel("Angular Velocity (rad/s)")
plt.legend(["wx", "wy", "wz"])
plt.title("Angular Velocity vs Time")
plt.grid()
plt.show()

#-----------------------------------------------------------------
# Analyze a subset of the data
# --> it1 is the time index right before the oscillation begins
# --> it1 is the time index where the oscillation ends
# --> Example: I wanted to analyze a signal from T = 6 - 60 seconds
#              so I found the T[it1] value that was close to 6 s
#              and the T[it2] value that was close to 60 s
#-----------------------------------------------------------------

it1,it2 = 6800,21088    # Update these iteration values for your own data
Tpend   = T[it1:it2]
wxpend  = wx[it1:it2]


#-----------------------------------------------------------------
#-----------------------------------------------------------------
# Find the peaks of the subset
# This section should work without any code updates
# **Only update the distance value here if peaks are not matching**
#      --> Larger distance integer value forces more points between peaks
#-----------------------------------------------------------------
#-----------------------------------------------------------------
wx_its, _ = find_peaks(list(wxpend),height=0,distance = 50) # solves for peak iteration values
wx_its    = wx_its+it1     # Shifts iteration values by it1
wx_peaks  = wxpend[wx_its] # Solves for peak values using wx_its iteration values
Tx_peaks  = Tpend[wx_its]  # Solves for time peak values occur using wx_its iteration values

#-----------------------------------------------------------------
# Calculate Average Period
# **This section does not require updating**
#
# For loop is used to calculate time between peaks
# Mean function is used to calculate average period
#-----------------------------------------------------------------
Tperiod = []
for i in range(len(wx_peaks)):
    if(i>0):
        Tperiod.append(Tx_peaks[wx_its[i]] - Tx_peaks[wx_its[i-1]])

Tp_avg = mean(Tperiod)
print("T Avg [s] =",Tp_avg)

#-----------------------------------------------------------------
# Solve for J values
# Theoretical (th) uses only phone mass and dimensions
# Experimental (exp) uses measured period, phone mass, and filar dimensions
#-----------------------------------------------------------------
Jth  = 1/12*m*(t**2 + L**2)
Jexp = (Tp_avg/2/math.pi)**2*m*9.81*(a)**2/h

# Print functions do not require updates
print("J experimental [kg*m^2] = % 5.6f" %(Jexp))
print("J theoretical  [kg*m^2] = % 5.6f" %(Jth))

#-----------------------------------------------------------------
# Plot oscillation and peak data
#     --> Plot Tpend and wxpend data
#     --> Scatter plot Tx_peaks and wx_peaks with red x markers
#-----------------------------------------------------------------
plt.figure(2)
plt.plot(Tpend, wxpend)
plt.scatter(Tx_peaks, wx_peaks, marker='x', color = 'r')
plt.xlabel("Time (s)")
plt.ylabel("Angular Velocity (rad/s)")
plt.title("Angular Velocity vs Time")
plt.legend(["All data", "Peak data"])
plt.grid()
plt.show()