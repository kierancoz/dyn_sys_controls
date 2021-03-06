import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

plt.close('all')


filename = 'LoadCellIMU_500g_static.csv'

data = pd.read_csv(filename)

t = np.array(data.Time)
f = np.array(data.Force) # [counts]
x_a = np.array(data.accX)
y_a = np.array(data.accY)
z_a = np.array(data.accZ)
wx = np.array(data.wx)
wy = np.array(data.wy)
wz = np.array(data.wz)

# Select data
T1, T2 = 0, t[-1]
it1 = np.nonzero(t > T1)[0][0]
it2 = np.nonzero(t < T2)[0][-1]
time = t[it1:it2]
f = f[it1:it2]
z_a = z_a[it1:it2]
wx = wx[it1:it2]*0.061e-3
wy = wy[it1:it2]*0.061e-3
wz = wz[it1:it2]*0.061e-3

# enter parameters
m_bungee_g = 30.669+0.000321*(654496)-200
cal_slope  = 0.000321
cal_int    = 30.669
m_weight = 0.5 # kg
f_N = ((f*cal_slope + cal_int) - m_bungee_g)/1000.*9.81 # Force in newtowns

# Get acceleration data
acc_coeff = 2*0.061e-3
z_a_ms2 = z_a*acc_coeff * 9.81 # Acceleration in meters/s^2


# estimage the force due to the mass acceleration
f_acc = -z_a_ms2*m_weight


# Plots
fig, (ax1, ax2, ax3) = plt.subplots(3,1,sharex=True)

print(sum(f_N)/len(f_N))
ax1.plot(time, f_N, label='force_meas')
ax1.plot(time, f_acc, label='force_acc')
ax1.grid()
ax1.legend()
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Force [N]')

ax2.plot(time, z_a_ms2, label='acceleration')
ax2.grid()
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('acc [m/s^2]')

ax3.plot(time, wx, label='wx')
ax3.plot(time, wy, label='wy')
ax3.plot(time, wz, label='wz')
ax3.grid()
ax3.legend()
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('angular velocity (dps)')

plt.show()


