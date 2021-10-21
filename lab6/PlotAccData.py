import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


plt.close('all')


filename = 'periodic_rotational.csv'
data = pd.read_csv(filename)

zelta = 530
# 4.5in to 6.5in TRANSLATIONAL
time = np.array(data.Time[zelta:])
x = np.array(data.accX[zelta:]) # [counts]
y = np.array(data.accY[zelta:]) # [counts]
z = np.array(data.accZ[zelta:]) # [counts]
wx = np.array(data.wx[zelta:])  # [counts]
wy = np.array(data.wy[zelta:])  # [counts]
wz = np.array(data.wz[zelta:])  # [counts]

#convert counts to gs
conv_accel = 0.061e-3 # conversion rate from raw data [counts] to units of [g]
x_g = x*conv_accel   # [g]
y_g =  y*conv_accel  # [g] 
z_g =  z*conv_accel  # [g]

conv_gyro = 17.50e-3    # conversion rate from raw data [counts] to [dps]
wx_dps = wx*conv_gyro   # [dps]
wy_dps = wy*conv_gyro   # [dps]
wz_dps = wz*conv_gyro   # [dps]

print("Mean value for accel x - y - z")
print(np.mean(x_g),np.mean(y_g),np.mean(z_g))
print("Standard deviation for accel x - y - z")
print(np.std(x_g),np.std(y_g),np.std(z_g))
print("\nMean value for angular speed x - y - z")
print(np.mean(wx_dps),np.mean(wy_dps),np.mean(wz_dps))
print("Standard deviation for angular speed x - y - z")
print(np.std(wx_dps),np.std(wy_dps),np.std(wz_dps))

plt.figure()
plt.plot(time, x, label='x')
plt.plot(time, y, label='y')
plt.plot(time, z, label='z')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [counts]')
plt.title('Acceleration Raw Data vs Time')
plt.show()

plt.figure()
plt.plot(time, x_g, label='x')
plt.plot(time, y_g, label='y')
plt.plot(time, z_g, label='z')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel("Acceleration [g]")
plt.title("Acceleration vs Time")
plt.show()

plt.figure()
plt.plot(time, wx, label='wx')
plt.plot(time, wy, label='wy')
plt.plot(time, wz, label='wz')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [counts]')
plt.title('Gyro Raw Data vs Time')
plt.show()

plt.figure()
plt.plot(time, wx_dps, label='wx')
plt.plot(time, wy_dps, label='wy')
plt.plot(time, wz_dps, label='wz')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel("Angular Velocity [dps]")
plt.title("Angular Velocity vs Time")
plt.show()