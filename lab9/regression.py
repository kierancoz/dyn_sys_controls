import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# data K1
# volume_1 = np.array([0, 100, 250, 450, 670]) ** (1/2)
# time_1 = np.array([0, 8.78, 14.43, 18.69, 23.74])
# time_1 = time_1.reshape((-1, 1))
# K1 = 1.0989 * 2

# data K2
volume_1 = np.array([0, 100, 200, 300, 400]) ** (1/2)
time_1 = np.array([0, 13.15, 22.04, 26.78, 33.37 ])
time_1 = time_1.reshape((-1, 1))
# K2 = 0.5 * 2

model_1 = LinearRegression().fit(time_1, volume_1)
slope_1 = model_1.coef_[0]
intercept_1 = model_1.intercept_

print("Slope: " + str(slope_1))
print("intercept: " + str(intercept_1))

pred_1 = slope_1*time_1 + intercept_1

plt.close('all')
plt.scatter(time_1, volume_1, label='data', color='r')
plt.plot(time_1,pred_1 , label='fit')
plt.xlabel('Time (s)')
plt.ylabel('Volume (mL)')
plt.title('Can K2 Calculation: Time vs Volume')
plt.grid()
plt.show()