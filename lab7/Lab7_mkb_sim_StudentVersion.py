#
# Mass-spring-damper simulation
#
import numpy as np
import matplotlib.pyplot as plt
import rk
import pandas as pd

# %% Section 1: Simulation

# define the system ODEs
def mkb(x, t, m, k, b, F0):
    Fb  = b*x[1]           # Linear Damping
    Fnl = F0*np.sign(x[1]) # Nonlinear Damping
    xdot1 = x[1]
    xdot2 = (-k*x[0] - Fb - Fnl)/m
    # specify outputs (y can be vector)
    y = xdot2/9.81 
    
    return np.array([xdot1, xdot2]), y

m  = 0.424471
k  = 637.4
b  = 0.207
F0 = 0
args = (m,k,b,F0)
# initially deflect and release mass from rest
x0 = np.array([0.01, 0.0])

t = np.arange(0, 20, 0.001)
sol = rk.rk4fixed(mkb, x0, t, args)

Az_sim = []
for i in range(len(t)):
    xdot,y = mkb(sol[i,:],t[i],m,k,b,F0)
    Az_sim.append(y)


# %% Section 2: Import Experimental Data

#---------------------------
# Import file and read data
#---------------------------
filename = 'Lab7_test.csv'
data     = pd.read_csv(filename)

time = np.array(data.Time)
x = np.array(data.accX) # [counts]
y = np.array(data.accY) # [counts]
z = np.array(data.accZ) # [counts]

#---------------------------
# Convert raw data: counts to gs
#---------------------------
conv =  0.061e-3#1/1024  # conversion rate from raw data [counts] to units of [g] # NOT CORRECT FOR EXPERIMENT LATER
x_g = x*conv   # [g]
y_g = y*conv   # [g] 
z_g = z*conv   # [g]

#---------------------------
# Remove Mean from z_g to find acceleration from equilibrium
#---------------------------
z_g = z_g - np.mean(z_g)

#---------------------------
# Cut data at beginning and end of dynamic oscillation:
#---------------------------
T1, T2 = 4.8, 29
it1 = np.nonzero(time > T1)[0][0]
it2 = np.nonzero(time < T2)[0][-1]

Tz, Az = time[it1:it2] - time[it1], z_g[it1:it2]

# %% Figure

plt.figure()
#plt.plot(t,sol[:,0], label='Position')
plt.plot(Tz, Az, label='Experiment')
plt.plot(t, Az_sim, label='Simulation')
plt.xlabel('Time [s]')
plt.ylabel('Acceleration [m/s^2]')
plt.title('Mass Spring Damper: Acceleration vs Time')
plt.legend()
plt.grid()
plt.show()






