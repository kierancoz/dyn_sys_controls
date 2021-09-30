#
# Pendulum simulation
#
import numpy as np
import matplotlib.pyplot as plt
import rk

# define the system ODEs
def pendulum(x, t, m, g, l):
	xdot1 = x[1]
	xdot2 = -g*np.sin(x[0])/l
	# specify outputs
	y = 0

	return np.array([xdot1, xdot2]), y

m = 1
g = 9.81
l = g/(4 * np.pi * np.pi)
# initially deflect and release mass from rest
x0 = np.array([np.pi/2, 0.0])

t1 = np.linspace(0, 4, 1001)
sol1 = rk.rk1fixed(pendulum, x0, t1, args=(m,g,l))
t4 = np.linspace(0, 4, 101)
sol4 = rk.rk4fixed(pendulum, x0, t4, args=(m,g,l))

plt.plot(t4, sol4[:, 0], 'o', label='rk4fixed')
plt.plot(t1, sol1[:, 0], label='rk1fixed')
plt.xlabel('t')
plt.grid()
plt.show()
