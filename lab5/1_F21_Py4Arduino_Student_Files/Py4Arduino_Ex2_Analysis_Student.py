import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft

#plt.close('all') # close all plots

# --------------------------------------
# Load and select data
# --------------------------------------
fileName = "Lab5_test.csv"

# Read csv file
data = pd.read_csv(fileName)

# Extract data from dataframe
t  = np.array(data.Time)
v = np.array(data.voltage)
led = np.array(data.LED_on)

# Get data at times of interest
T1,T2 = 0, t[-1]
# T1, T2 = 0.68, 9.7
it1 = np.nonzero(t > T1)[0][0]
it2 = np.nonzero(t < T2)[0][-1]

T  = t[it1:it2] - t[it1] # Resets time to zero seconds
V = v[it1:it2]
L = led[it1:it2]

# --------------------------------------
# FFT of potentiometer signal
# --------------------------------------

# Choose signal 
y_pot = V  # voltage

# Make zero-mean
y_pot = y_pot - 1*np.mean(y_pot)

# Create FFT of potentiometer signal
yf_pot = fft(y_pot)
Tf = np.mean(np.diff(T))  # mean of the sample period
Nf = len(T)  # number of samples
xf = np.linspace(0.0, 1.0/(2.0*Tf), Nf//2) # frequencies corresponding to fft
amplitudef_pot = 2.0/Nf * np.abs(yf_pot[0:Nf//2])  # get magnitude of the fft


maxInd_pot = amplitudef_pot.argmax() # find index maximum value of magnitude
primary_freq_pot =  xf[maxInd_pot]   # get primary frequency of signal

primary_freq_amp_pot = amplitudef_pot[maxInd_pot] # get magnitude of primary frequency
experimental_period_pot = 1/primary_freq_pot   # convert frequency to period

# --------------------------------------
# FFT of LED signal
# --------------------------------------

# Choose signal 
y_LED = L

# Make zero-mean
y_LED = y_LED - np.mean(y_LED)

# Create FFT of potentiometer signal
yf_LED = fft(y_LED)

amplitudef_LED =  2.0/Nf * np.abs(yf_LED[0:Nf//2])# get magnitude of the fft

maxInd_LED = amplitudef_LED.argmax() # find index maximum value of magnitude
primary_freq_LED = xf[maxInd_LED]    # get primary frequency of signal


primary_freq_amp_LED = amplitudef_LED[maxInd_LED] # get magnitude of primary frequency
experimental_period_LED = 1/primary_freq_LED   # convert frequency to period

# --------------------------------------
# Print periods of Potentiometer and LED signals
# --------------------------------------

print("Experimental period of potentiometer data is: % 3.4f seconds" %(experimental_period_pot))
print("Experimental period of LED Data is is: % 3.4f seconds" %(experimental_period_LED))

# --------------------------------------
# Plots
# --------------------------------------

# Plot voltage and LED on/off vs time
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig.suptitle('Potentiometer Voltage and LED On/Off Signal')
ax1.plot(T,V)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Voltage [V]')


ax2.plot(T,L, 'r')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('On/Off [unitless]')

# Figure with FFT of both signals
fig, (ax3, ax4) = plt.subplots(2, 1, sharex=True)
fig.suptitle('Fast Fourier Transforms of Potentiometer and LED signals')

#subplot 1: potentiometer data
ax3.plot(xf ,amplitudef_pot , label='spectral density of potentiometer signal')
ax3.plot(primary_freq_pot, primary_freq_amp_pot, 'rx', label='Primary frequency of potentiometer signal')
ax3.grid()
ax3.set_xlim(0,10)
ax3.legend()
ax3.set_title('Potentiometer')
ax3.set_xlabel('')
ax3.set_ylabel('')

# subplot 2: LED data
ax4.plot(xf , amplitudef_LED, label='spectral density of LED on/off signal')
ax4.plot(primary_freq_LED, primary_freq_amp_LED, 'rx', label='Fundamental frequency of LED signal')
ax4.grid()
ax4.legend('')
ax4.set_title('LED')
ax4.set_xlabel('')
ax4.set_ylabel('')

plt.show()
