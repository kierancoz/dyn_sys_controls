import numpy as np
import matplotlib.pyplot as plt

load = np.array([0, 100, 200, 400, 500, 700, 800, 900, 1100, 1300, 1500, 1700, 1900, 2000])*9.81/1000
length = np.array([9, 9.05, 9.25, 10.25, 12.5, 13.5, 14.75, 15.5, 16.5, 17.75, 18.5, 19.25, 19.75, 19.8])

plt.scatter(length,load)
plt.xlabel("Load (N)")
plt.ylabel("Displacement (in)")
plt.show()