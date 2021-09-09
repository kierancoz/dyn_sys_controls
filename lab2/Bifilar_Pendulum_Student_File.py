#-----------------------------------------------------------------
# Import Required Packages
#-----------------------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean
from scipy.signal import find_peaks


#-----------------------------------------------------------------
#-----------------------------------------------------------------
# When reading from your own data:
#    --> Go to File and Open 
#    --> Open CSV file in Python and rename first row variables: Time,omegax,omegay,omegaz,omegaa
#    --> Then save and close the CSV file
#-----------------------------------------------------------------
#-----------------------------------------------------------------
filename  = 'raw_data_test.csv' # Update filename with your own data file


#-----------------------------------------------------------------
# Bifilar Pendulum variables
# Fill in Bifilar and phone dimensions
# Based on Ogata PDF variable names
#-----------------------------------------------------------------
h =      # [m],  bifilar string length
a =      # [m],  length between files/2
L =      # [m],  length of phone (horizontal --> parallel to ground)
t =      # [m],  thickness of phone
m =      # [kg], phone mass

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
plt.figure()
plt.plot()
plt.xlabel()
plt.ylabel()
plt.legend()
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

it1,it2 = 0,len(T)    # Update these iteration values for your own data
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
Jth  = 
Jexp = 

# Print functions do not require updates
print("J experimental [kg*m^2] = % 5.6f" %(Jexp))
print("J theoretical  [kg*m^2] = % 5.6f" %(Jth))

#-----------------------------------------------------------------
# Plot oscillation and peak data
#     --> Plot Tpend and wxpend data
#     --> Scatter plot Tx_peaks and wx_peaks with red x markers
#-----------------------------------------------------------------
plt.figure()
plt.plot()
plt.scatter()
plt.xlabel()
plt.ylabel()
plt.title()
plt.legend()
plt.grid()
plt.show()


