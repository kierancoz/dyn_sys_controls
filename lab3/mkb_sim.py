#
# Mass-spring-damper simulation
#
import numpy as np
import matplotlib.pyplot as plt
import rk

# define the system ODEs
def mkb(x, t, m, k, b):
	xdot1 = x[1]
	xdot2 = (-k*x[0]-b*x[1])/m
	# specify outputs (y can be vector)
	y = xdot2

	return np.array([xdot1, xdot2]), y

m = 1
k = 10
b = 1
# initially deflect and release mass from rest
x0 = np.array([0.5, 0.0])

t = np.linspace(0, 10, 101)
sol = rk.rk4fixed(mkb, x0, t, args=(m,k,b))

f, (ax1, ax2, ax3) = plt.subplots(3,1,sharex=True)

ax1.plot(t, sol[:, 0], label='position')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Position (m)')
ax1.grid()

ax2.plot(t, sol[:, 1], label='velocity')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Velocity (m/s)')
ax2.grid()

accels = []
for i in range(len(t)):
	xdot, y = mkb(sol[i,:], t[i], m, k, b)
	accels.append(y)

ax3.plot(t, accels, label='acceleration')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Acceleration (m/s^2)')
ax3.grid()

plt.show()