# Lab 5 - Python Review and Signal Analysis
# FFT of Bifilar Data

from scipy.fft import fft
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

plt.close('all') # close all plots

#%% Section 1: Read and Plot Data

# Constants
File = '../../lab3/raw_data_45.csv'

#---------------------------
# Read from the Test file
#---------------------------
data = pd.read_csv(File)

# Time,omegax,omegay,omegaz,Absolute (rad/s)
T  = np.array(data["Time"])
Wx = np.array(data["omegax"])
Wy = np.array(data["omegay"])
Wz = np.array(data["omegaz"])

dt = np.mean(np.diff(T)) # Calculate delta_t [s]

#---------------------------
# Plot the X axis Gyroscope data
# Add a title and X/Y labels
#---------------------------
plt.figure()
plt.plot( T, Wx)
plt.title('Angular Velocity vs Time')
plt.xlabel('Angular Velocity (rad/s)')
plt.ylabel('Time (s)')
plt.grid()
plt.show()


#%% Section 2: Index data, find peaks, and plot

#---------------------------
# Index data we want to analyze
#---------------------------

# Choose time frames
# For example "Good data", choose 2.38, 40
T1, T2 = 0, T[-1]             
it1 = 3430
it2 = 8300

Tfft, Wxfft = T[it1:it2], Wx[it1:it2]

#---------------------------
# Find the Peaks and Calculate Avg Period
# Find a value of dist that allows for better peak accuracy
#---------------------------
dist = 50

wx_its, _ = find_peaks(Wxfft, height=0, distance = dist)
wx_peaks  = Wxfft[wx_its] # Solves for peak values using wx_its iteration values
Tx_peaks  = Tfft[wx_its]
Tp_avg    = np.mean(np.diff(Tx_peaks))

print("----------------------------------------------")
print("Pk to Pk Frequency is: % 3.4f Hz" %(1/Tp_avg))
print("Pk to Pk period is: % 3.4f seconds" %(Tp_avg))
print("----------------------------------------------")

plt.figure()
plt.plot(T,Wx)
plt.plot(Tx_peaks,wx_peaks,'rx')
plt.title('W [rad/s] vs Time [s]')
plt.legend(['Wx','Peaks'])
plt.xlabel('Angular Velocity (rad/s)')
plt.ylabel('Time (s)')
plt.grid()
plt.show()


#%% Section 3: Apply FFT and compare to Peak to Peak Output

#---------------------------
# Apply FFT
#---------------------------
# Number of sample points
N     = len(Tfft)
fs    = 1/dt  # sampling rate   [Hz]
Ts    = dt    # sampling period [s]
Wf    = fft(Wxfft)
xf    = np.linspace(0.0, 1.0/(2.0*Ts), N//2) # Create frequency array
f_amp = 2.0/N * np.abs(Wf[0:N//2])  # Calculate Freq. Amplitude

#---------------------------
# Calculate dominant frequency and period
#---------------------------
maxInd = f_amp.argmax()
primary_freq = xf[maxInd]
primary_freq_amp = f_amp[maxInd]
experimental_period = 1.0/primary_freq

print("Dominant FFT Frequency is: % 3.4f Hz" %(primary_freq))
print("Experimental FFT period is: % 3.4f seconds" %(experimental_period))
print("----------------------------------------------")

plt.figure()
plt.plot(xf, f_amp)
plt.plot(primary_freq, primary_freq_amp, 'xr', label='Primary frequency')
plt.ylabel("Amplitude [don't worry about units]")
plt.grid()
plt.xlim([0, 20])
plt.xlabel("Freq [Hz]")
plt.show()






