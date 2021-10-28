import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression 


plt.close('all')

# %% Section 1: Beam Parameters and Calculations

#---------------------------
# Experimental Beam Measurements/Variables
# Parameters set for an Aluminum ruler cantilever beam setup
# Note: E and rho based on 6061 Aluminum
#---------------------------
# L = 11.1*0.0254   # [m]
# h = 0.05*0.0254   # [m]
# w = 1.2*0.0254    # [m]
# E = 68.9e9        # [Pa]
# I = (1/12)*w*h**3 # [m^3]
# rho = 2700        # [kg/m^3]
# Mbeam = L*h*w*rho # [kg]
# Mlump = (20 + 4*5.6 + 5)/1000 # [kg], includes quarters/zip tie/duct tape

L = 0.28 #25.5cm   # [m]
h = 0.00317   # [m]
w = .0255    # [m]
E = 68.9e9        # [Pa]
I = (1/12)*w*h**3 # [m^3]
rho = 2700        # [kg/m^3]
Mbeam = L*h*w*rho # [kg]
Mlump = (63+3.5)/1000 # [kg], includes quarters/zip tie/duct tape


# Calculate Theoretical Stiffness
Kth = 3*E*I/(L**3)

# Calculate Natural Frequency Bounds
wn_th_min = np.sqrt(Kth/(Mlump+Mbeam))
wn_th_DH  = np.sqrt(Kth/(0.23*Mbeam+Mlump))
wn_th_max = np.sqrt(Kth/Mlump)


# %% Section 2: Read CSV File and Calibrate Raw Data

#---------------------------
# Import file and read data
#---------------------------
filename = 'Lab7_test.csv'
data = pd.read_csv(filename)

time = np.array(data.Time)
x = np.array(data.accX) # [counts]
y = np.array(data.accY) # [counts]
z = np.array(data.accZ) # [counts]

#---------------------------
# Convert raw data: counts to gs
#---------------------------
conv = 0.061e-3 #1/1024  # conversion rate from raw data [counts] to units of [g]
x_g = x*conv   # [g]
y_g = y*conv   # [g] 
z_g = z*conv   # [g]

#---------------------------
# Remove Mean from z_g to find acceleration from equilibrium
#---------------------------
z_g = z_g - np.mean(z_g)


# %% Section 3: Analyze Data Subset

#---------------------------
# Cut data at beginning and end of dynamic oscillation:
#---------------------------
T1, T2 = 4.8, 29
it1 = np.nonzero(time > T1)[0][0]
it2 = np.nonzero(time < T2)[0][-1]

Tz, Az = time[it1:it2], z_g[it1:it2]


#---------------------------
# Assess Z axis acceleration
# Find the Peaks and Calculate Avg Period
# Find a value of dist that allows for better peak accuracy
#---------------------------
dist = 20

Az_its, _ = find_peaks(Az, height=0, distance = dist)
Az_peaks  = Az[Az_its] # Solves for peak values using wx_its iteration values
Tz_peaks  = Tz[Az_its]
Tz_avg    = np.mean(np.diff(Tz_peaks))
wd_exp    = 2*np.pi/Tz_avg


#---------------------------
# Solve for zeta:
# 1) Apply Logarithmic Decrement
# 2) Apply Linear Regression to find slope
# 3) Use slope (Beta) value to solve for zeta
#
# Note: LinearRegression function takes column vectors
#---------------------------
N      = 30
Nvec   = np.arange(1,N+1,1)
A0     = Az_peaks[0]
lnA0An = np.log(A0/Az_peaks[Nvec]) #np.ones(np.size(Nvec))

# Reshape Nvec and LnA0An for Linear Regression
Nvec   = Nvec.reshape(-1, 1)
lnA0An = lnA0An.reshape(-1, 1)

# Linear Regression
Zmodel = LinearRegression(fit_intercept = False).fit(Nvec, lnA0An)
ZR2    = Zmodel.score(Nvec, lnA0An)
Beta, Zint = float(Zmodel.coef_), float(Zmodel.intercept_)

# Solve for zeta
zeta = Beta/np.sqrt(4*np.pi**2+Beta**2)

# Equation for wd = wn*sqrt(1 - zeta^2)
wn_exp = wd_exp/np.sqrt(1-zeta**2) # [rad/s]

# Solve for effective mass
m_eff   = Kth/(wn_exp**2)
m_diff  = (m_eff - Mlump)
mb_diff = m_diff/Mbeam*100

# Solve for damping coefficient (b) value
bexp = 2*zeta*wn_exp*m_eff


# %% Section 4: Print all calculated values

#---------------------------
# All Print Commands
#---------------------------
print('---------------------------------------------------------')
print('Theoretical Stiffness and Natural Frequency Bounds:')
print("Theoretical Stiffness [N/m] = %3.2f" %(Kth))
print("Omega_n Min [rad/s] = %3.6f" %(wn_th_min))
print("Omega_n DH  [rad/s] = %3.6f" %(wn_th_DH))
print("Omega_n Max [rad/s] = %3.6f" %(wn_th_max))
print('---------------------------------------------------------')
print('---------------------------------------------------------')
print("Experimental Signal Freq. [Hz] = %3.4f" %(1/Tz_avg))
print("Experimental period [s]        = %3.4f" %(Tz_avg))
print("Damped Natural Freq. [rad/s]   = %3.4f" %(wd_exp))
print('---------------------------------------------------------')
print('---------------------------------------------------------')
print("Beta (slope) = % 3.5f" %(Beta))
print("R squared    = % 3.5f" %(ZR2))
print("Zeta         = % 3.5f" %(zeta))
print('---------------------------------------------------------')
print('---------------------------------------------------------')
print('Experimental Damped and Natural Frequencies Results:')
print("Omega_d Exp [rad/s] = %3.6f" %(wd_exp))
print("Omega_n Exp [rad/s] = %3.6f" %(wn_exp))
print('---------------------------------------------------------')
print('---------------------------------------------------------')
print("Effective Mass [kg] = %3.6f" %(m_eff))
print("Percentage of beam mass in Effective Mass [%%] = %3.2f" %(mb_diff))
print("(Compare to DH Method value of 23%)")
print('---------------------------------------------------------')
print('---------------------------------------------------------')
print("Damping Coefficient, b [N*s/m] = %3.5f" %(bexp))
print('---------------------------------------------------------')


# %% Section 5: Plot all figures

#---------------------------
# All Figures
#---------------------------
# Acceleration vs time
# plt.figure()
# plt.plot(time, x_g, label='x')
# plt.plot(time, y_g, label='y')
# plt.plot(time, z_g, label='z')
# plt.grid()
# plt.legend()
# plt.xlabel('Time [s]')
# plt.ylabel("Acceleration [g]")
# plt.title("Acceleration vs Time")
# plt.show()

# # Z axis window with peaks
# plt.figure()
# plt.plot(Tz,Az)
# plt.plot(Tz_peaks,Az_peaks,'rx')
# plt.title('Z acceleration vs Time')
# plt.legend(['Zacc','Peaks'])
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude [g]')
# plt.grid()
# plt.show()


# # Log. Dec. plot
# plt.figure()
# plt.plot(Nvec, lnA0An,'o')
# plt.plot(Nvec,Nvec*Beta)
# plt.grid()
# plt.xlim([0, N+1])
# plt.xlabel('Peak Number')
# plt.ylabel('ln(A0/An)')
# plt.legend(["ln(A0/An)","Regression"])
# plt.show()


# %% Section 6: Extra --> FFT (if time permits)
    
# #---------------------------
# # Extra: FFT
# #---------------------------
# from scipy.fft import fft
# # Number of sample points
# dt    = np.mean(np.diff(time))
# Nf    = len(Tz)
# fs    = 1/dt  # sampling rate   [Hz]
# Ts    = dt    # sampling period [s]
# Af    = fft(Az)
# xf    = np.linspace(0.0, 1.0/(2.0*Ts), Nf//2) # Create frequency array
# f_amp = 2.0/Nf * np.abs(Af[0:Nf//2])  # Calculate Freq. Amplitude


# plt.figure()
# plt.plot(xf, f_amp)
# plt.ylabel("Amp [g/sqrt(Hz)]")
# plt.grid()
# plt.xlim([0, 20])
# plt.xlabel("Freq [Hz]")
# plt.show()




#CHALLENGE

wx = np.array(data.wx) # [counts]
wy = np.array(data.wy) # [counts]
wz = np.array(data.wz) # [counts]

conv = 1/1024  # conversion rate from raw data [counts] to units of [g]
x_g = x*conv   # [g]
y_g = y*conv   # [g] 
z_g = z*conv   # [g]

theta = [0]
theta_alt = [0]
wx_u = wx[1000:2000]
time_u = time[1000:2000]
z_u = z_g[1000:2000]

dist = 20
peak_its, _ = find_peaks(abs(wx_u), height=0, distance = dist)
peaks  = wx_u[peak_its]

i_0 = 0
for i in range(0, len(wx_u)-1):
    theta_i = np.trapz(wx_u[i_0:i], x=time_u[i_0:i])
    if wx_u[i] in peaks:
       theta_i = 0
       i_0 = i
    theta.append(theta_i/180*3.314)

    theta_alt.append((m_eff*z_u[i])*L**2/2/E/I*60/3.314+.5)

theta = np.array(theta)



# Acceleration vs time
plt.figure()
#plt.scatter(time_u, wx_u)

plt.plot(time_u, theta_alt)
plt.plot(time_u, theta)
#plt.scatter(time[peak_its], peaks)
#plt.scatter(np.array(data.Time), wx)
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel("Angle [degrees]")
plt.title("Angle vs Time")
plt.show()