import numpy as np
import matplotlib.pyplot as plt
import random
import math
import statistics as stat

T, N = 1, 1000
t = [i*T/N for i in range(N)]
mu, sigma = 0, 0.5
x = [random.gauss(mu, sigma) for tc in t]
xmean = stat.mean(x)
xsdev = stat.stdev(x)
xvar = stat.variance(x)
x_hist, bin_edges = np.histogram(x, density=True)
bin_centers_x = [(bin_edges[i]+bin_edges[i+1])/2 for i in range(len(bin_edges)-1)]

fig1, (ax1, ax2) = plt.subplots(2)
ax1.plot(t, x, 'b', label='x(t)', alpha = 0.5)
ax1.hlines(xmean, 0, max(t), 'r', linestyle = 'dashed', label='mean')
ax1.hlines(xsdev, 0, max(t), 'g', linestyle = 'dashed', label='rms')
ax1.legend(loc='lower left')
ax1.set_xlabel('Time (sec')
ax2.bar(bin_centers_x,x_hist, width = 0.1)
ax2.set_xlabel('x values', fontsize=12)
ax2.set_xlim([-3,3])
plt.show()


print("mean of x is " + str(xmean))
print("standard deviation of x is " + str(xsdev))
print("variance of x is " + str(xvar))