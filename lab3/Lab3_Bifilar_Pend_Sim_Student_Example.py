#-----------------------------------------------------------------
# Lab 3 - Bifilar Pendulum Simulation vs Experimental Data
# Student and TA Example File
# 9/14/20
#
# This file is to be used to show students how to iteratively match
# the simulation omega to the experimentally measured omega of the
# bifilar pendulum
#
# Sample data file "Bifilar_Pend_Test.csv" required
# See Canvas Files --> lab03_Bifilar_Pend_Simulation folder for data
#
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# Import Required Packages
# NOTE: rk file must be saved in same folder as this python file to work
#-----------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import rk

plt.close('all')

#-----------------------------------------------------------------
# Bifilar Pend Variables
# Using Ogata PDF variable denotation
# Variables below are for my Samsung S8 phone + case
#-----------------------------------------------------------------
g = 9.81           # [m/s^2], gravitational acc
L = 0.356 # [m],  bifilar string length
R = 0.0413 # [m],  length between files/2
Lp = 0.1447 # [m],  length of phone (horizontal --> parallel to ground)
t = 0.008 # [m],  thickness of phone
m = 0.151 # [kg], phone mass

#-----------------------------------------------------------------
# Adjust J, b, and x0 values to match simulation to experiment
# J values from LE 2:
# Jexp = 0.000297    # [kg*m^2], Lab 2 Experimental value
# Jth  = 0.000354    # [kg*m^2], Lab 2 Theoretical value
#
# Start with theoretical J, no damping, and estimated initial angle
#
#-----------------------------------------------------------------
J   = 0.000223 # [kg*m^2]
b   = 0.000007    # [Solve for units], damping coefficient
x_0 = 50        # [deg] 


#-----------------------------------------------------------------
# Read CSV file
#-----------------------------------------------------------------
filename  = 'raw_data_45.csv'
csvdata   = pd.read_csv(filename)

#-----------------------------------------------------------------
# Index into the columns using the renamed column header names
#-----------------------------------------------------------------
Tcsv = np.array(csvdata['Time'])
wx   = np.array(csvdata['omegax'])
wy   = np.array(csvdata['omegay'])
wz   = np.array(csvdata['omegaz'])

# Use nonzero function to find iteration values near the desired times T1 & T2
T1, T2 = 0, Tcsv[-1]
it1 = np.nonzero(Tcsv > T1)[0][0]
it2 = np.nonzero(Tcsv < T2)[0][-1]
#it1, it2 = 0,21088
it1 = 3430
it2 = 8300
Tpend  = Tcsv[it1:it2] - Tcsv[it1] # Resets time to zero seconds
wxpend = wx[it1:it2]

#-----------------------------------------------------------------
# Simulation Variables
#-----------------------------------------------------------------
x0 = np.array([x_0,0])*(np.pi/180) # [rad, rad/s]

#-----------------------------------------------------------------
# Simulation Function
#-----------------------------------------------------------------
# define the system ODEs
def bifilar_pend(x, t, m, g, R, L, J, b):
	xdot1 = x[1]
	xdot2 = (1/J)*(-(R**2*m*g/L)*np.sin(x[0]) - b*x[1])
	# specify outputs
	y = 0

	return np.array([xdot1, xdot2]), y

#-----------------------------------------------------------------
# Run Simulation
#-----------------------------------------------------------------
args = (m,g,R,L,J,b)
T    = np.arange(0, Tcsv[it2-it1], 0.001)
X    = rk.rk4fixed(bifilar_pend, x0, T, args)

# Simulation state vars
Theta, Omega = X[:,0], X[:,1]

#-----------------------------------------------------------------
# Find the peaks of the simulation and experiment
#-----------------------------------------------------------------
# Exp Data
wx_its, _ = find_peaks(list(wxpend),height=0,distance = 50)
wx_peaks  = wxpend[wx_its] # Solves for peak values using wx_its iteration values
Tx_peaks  = Tpend[wx_its]  # Solves for time peak values occur using wx_its iteration values

# Sim Data
w_its, _ = find_peaks(list(Omega),height=0,distance = 50)
w_pks    = Omega[w_its] # Solves for peak values using w_its iteration values
T_pks    = T[w_its]  # Solves for time peak values occur using w_its iteration values



# Theta and Omega symbol codes
theta_sym = '\u03B8 [rad]'
omega_sym = '$\u03C9_{sim}$ [rad/s]'
omega_exp = '$\u03C9_{exp}$ [rad/s]'

# Plot simulated and experimental angular velocities w/ peaks
f, (ax1, ax2) = plt.subplots(2,1,sharex=True)

ax1.plot(T, Omega, 'tab:orange')
ax1.plot(Tpend,wxpend, 'tab:blue')
ax1.plot(T_pks, w_pks, '-xg')
ax1.plot(Tx_peaks, wx_peaks, '-xr')
ax1.set_xlabel('T [s]')
ax1.set_ylabel('Angular Velocity [rad/s]')
ax1.legend([omega_sym, omega_exp, 'Sim peaks', 'Exp peaks'])
# ax1.set_title("Angular Velocity Matching: %5.1f [deg] Exp vs Sim" %(x_0))
# plt.xlim([0,20])
ax1.grid()
ax2.grid()
ax2.plot(T, Theta, 'tab:orange')
ax2.set_xlabel('T [s]')
ax2.set_ylabel('Angular position [rad]')
plt.show()