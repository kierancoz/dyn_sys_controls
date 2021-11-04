#
# mass-bungee (spring-damper) simulation
# allows entering bungee force vs displacement data
# uses interpolation in simulation 
#
# ME 144L lab, Fall 2021
#
import math
import numpy as np
import matplotlib.pyplot as plt
import rk
import random
from scipy.interpolate import interp1d

plt.close('all')

# define the system ODEs
def bungee(x, t, m, Fk_bungee, g, b1, L_bungee):
	vm, xm, xk = x[0], x[1], x[2]
	# xm is mass position relative to unstretched bungee
	# xk is bungee stretch
	# Fk_bungee() must be defined using interp1d()
	# from the scipy.interpolate package
	if xk > 0.0:
		# bungee is stretching
		if xk>L_bungee:
			# bungee hits max length
			Fkbungee = Fk_bungee(L_bungee)
		else:
			Fkbungee = Fk_bungee(xk)

		Fb = b1*vm # linear bungee damping
		
	else:
		# if xk<0, bungee is 'slack', so no forces
		Fkbungee = 0.0
		Fb = 0.0

	vk = vm
	vmdot = (-Fkbungee - Fb + m*g)/m
	xmdot = vm
	xkdot = vk

	# specify outputs
	y = np.array([Fkbungee, vmdot])

	return np.array([vmdot, xmdot, xkdot]), y

g = 9.81
m = 0.310 # this is the mass attached
L_bungee = 9/39.37 # max bungee length
# define the force-displacement curve for bungee
# this is to be measured in lab
xin = np.array([9, 9.05, 9.25, 10.25, 12.5, 13.5, 14.75, 15.5, 16.5, 17.75, 18.5, 19.25, 19.75, 19.8]) - 9
xa = [xc/39.37 for xc in xin] 
Fa = np.array([0, 100, 200, 400, 500, 700, 800, 900, 1100, 1300, 1500, 1700, 1900, 2000])*9.81/1000
# define the bungee nonlinear spring model with interp1d()
Fk_bungee = interp1d(xa, Fa, kind='cubic')
# now to get Fk_bungee at x, just say Fk_bungee(x)
# linear damping in bungee
b1 = 0.5

dt, t0, tf = 0.001, 0.0, 5
N = math.floor((tf-t0)/dt)
# Initial conditions
vm0 = 0 # release from rest
# if xk0 is less than 0, simulates a bungee drop
xk0 = 0  # extension of bungee
xm0 = xk0 + L_bungee # position relative to load cell

x0 = np.array([vm0, xm0, xk0])
t = np.linspace(0, tf, N)
sol = rk.rk4fixed(bungee, x0, t, args=(m, Fk_bungee, g, b1, L_bungee))
# compute outputs
vm = sol[:,0]
xm = sol[:,1]
xk = sol[:,2]
Fkbungee = np.zeros(len(t))
am = np.zeros(len(t))
for i in range(len(t)):
	_, y = bungee(sol[i,:], t[i], m, Fk_bungee, g, b1,L_bungee)
	Fkbungee[i] = y[0]
	am[i] = y[1]/g

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
fig.suptitle('Bungee simulation')
ax1.plot(t, am, label='am')
ax1.legend(loc="upper right")
ax2.plot(t, -xm, label='xm') 
# note sign flip so it negative down
ax2.legend(loc="upper right")
ax3.plot(t, -xk, label='xk')
ax3.legend(loc="upper right")
ax4.plot(t, Fkbungee, label='Fkbungee')
ax4.legend(loc="upper right")
plt.xlabel('Time (sec)')
plt.grid()
plt.show()


dis = np.linspace(xa[0], xa[-1],100)
Fk_bungee_plot = Fk_bungee(dis)

plt.figure()
plt.plot(dis, Fk_bungee_plot,label='interpolation')
plt.plot(xa, Fa, 'or', label='measurements')
plt.legend()
plt.grid()
plt.xlabel('displacement [m]')
plt.ylabel('Force [N]')
plt.title('Bungee Force vs Displacement')
plt.show()
