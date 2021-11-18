#
# PMDC motor model
# R.G. Longoria 8-4-20 v1
import math
import numpy as np
import matplotlib.pyplot as plt
import rk

# define the system ODEs
def pmdc(x, t, rm, Rm, Bm, Jm, To, ton, toff, vb):
	# the two states are shaft speed and position
	omegam, thetam = x[0], x[1]

	# this model has a voltage that turns on and off
	if (t>ton) and (t<toff):
		vinc = vb
	else:
		vinc = 0

	im = (vinc - rm*omegam)/Rm
	omegamdot = (rm*im - Bm*omegam - To*np.sign(omegam))/Jm
	thetadot = omegam

	# specify outputs
	y = [im, vinc]

	return np.array([omegamdot, thetadot]), y

# all parameter units in SI
rm = 0.0109		# motor constant, N*m/A
Rm = 27.4 		# motor armature resistance, ohms
# below is an estimate of Jm based on the parts examined from
# the dismantled motor; only the rotor and magnetic disc are included
# total mass 9 grams, rough diameter 0.5 inch; model as equivalent disc
Jm = 0.5*0.009*(0.25/39.37)**2		# motor inertia, kg*m^2, ignores gears
print("Jm = " + str(Jm))
GR = 48			# gear ratio
Bm = 0.000178475e-3	# motor damping, from steady-state testing data
To = 1*0.1838e-3 # coulombic bearing torque in motor; from ss testing data

vb = 174/255*5		# bus voltage
ton, toff = 0.1, 1 		# turn on voltage

dt, t0, tf = 0.001, 0.0, 1.5
N = math.floor((tf-t0)/dt)
x0 = np.array([0,0]) # initial values of omegam, and thetam
t = np.linspace(0, tf, N)
sol = rk.rk4fixed(pmdc, x0, t, args=(rm, Rm, Bm, Jm, To, ton, toff, vb))
# compute outputs
omega = sol[:,0] # rad/sec
theta = 180*sol[:,1]/GR/math.pi # use thetam of motor to get output shaft in deg

im = np.zeros(len(t))
vin = np.zeros(len(t))
for i in range(len(t)):
	_, y = pmdc(sol[i,:], t[i], rm, Rm, Bm, Jm, To, ton, toff, vb)
	im[i] = 1000*y[0] 	# current in mA
	vin[i] = y[1]		# input voltage

# fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
# fig.suptitle('PMDC simulation')
# ax1.plot(t, vin, label='vin')
# ax1.legend(loc="upper right")
# ax1.set_ylabel('volts')
# ax2.plot(t, im, label='current')
# ax2.legend(loc="upper right")
# ax2.set_ylabel('mA')
# ax3.plot(t, omega, label='omega')
# ax3.set_ylabel('rad/sec')
# ax3.legend(loc="upper right")
# ax4.plot(t, theta, label='theta')
# ax4.set_ylabel('deg')
# ax4.legend(loc="upper right")
# plt.xlabel('Time (sec)')
# plt.tight_layout()
# plt.grid()
# plt.show()

print(omega[int(len(omega)/2)])
print(vb/5*255)