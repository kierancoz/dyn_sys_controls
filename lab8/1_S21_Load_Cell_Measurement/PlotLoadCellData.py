import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

plt.close('all')


filename = 'LoadCell_0g.csv'
data = pd.read_csv(filename)

t = np.array(data.Time)
x = np.array(data.Force) # [counts]


x_bar = np.mean(x) # Mean of x data [g]
x_std = np.std(x)  # Standard dev of x data [g]

print("Mean []: " + str(x_bar) + ", Std []: " + str(x_std))


plt.figure()
plt.plot(t, x, label='x')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [counts]')
plt.title('Raw Data vs Time')
plt.show()

