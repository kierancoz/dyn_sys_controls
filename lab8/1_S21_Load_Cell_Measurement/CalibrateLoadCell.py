import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Create array of analog outputs
analog_out = np.array([-98e3,-67e3,-33e3,59e3,215e3,529e3,1.47e6,3.01e6])
analog_out = analog_out.reshape((-1, 1))

# Corresponding masses in [gram]
mass_grams = np.array([0, 10, 20, 50, 100, 200, 500, 1000])

# fit a Linear Model
model = LinearRegression().fit(analog_out, mass_grams) 

# slope and intercept
slope = model.coef_[0]
intercept = model.intercept_

print("Slope: " + str(slope))
print("intercept: " + str(intercept))
print("r^2: " + str(model.score(analog_out, mass_grams)))

# prediction from linear regression
pred = slope*analog_out + intercept

plt.close('all')
plt.scatter(analog_out, mass_grams, label='data', color='r')
plt.plot(analog_out,pred , label='fit')
plt.xlabel('analog out (counts)')
plt.ylabel('mass (grams)')
plt.title('Load Cell Calibration')
plt.grid()
plt.show()

