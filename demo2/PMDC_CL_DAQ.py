from ArduinoDAQ import SerialConnect


# EDIT HERE START #
portName = 'COM5'                      # Communications port name. Make sure it matches port in Arduino IDE
# portName = '/dev/ttyUSB0'
baudRate   = 19200                     # Baud Rate
dataRate   = 20                       # Acquisition data rate (Hz), do not exceed 500
recordTime = 20                        # Number of seconds to record data
# END EDIT HERE #

numDataPoints = recordTime * dataRate  # Total number of data points to be saved

#%% Data lists and Arduino commands
#----------------------------------------------------------------------
# Data to read from Arduino file
# Do not edit anything in this section
#----------------------------------------------------------------------
dataNames = ['Time', 'wm_ref', 'wm','PWM']
dataTypes = [  '=L',     '=f', '=f', '=h']


#%%  Controller Gains
# Update with your own values

# EDIT HERE START #
# OL Gain
OLgain = 0.5 # [PWM/(rad/s)]

# Closed loop gains
Kp = 0.6   # Determine units     
Ki = 0.6   # Determine units      
Kd = 0.004  # Determine units
ref_speed = 300 # rad/s change as needed
# run_time = distance / speed = 12in / (v = wr)
# run_time = 12 / (125 rad/s * 1 in)
# 2pi rad = 2*pi in
run_time = 12/(ref_speed/45)       # time run motor 
# END EDIT HERE #

#%% Commands to send

# Commands:
# You will only need to send f, P, I, D, c, and k for this demo
# 'r' : Send data rate
# 'f' : Send OL Gain
# 'P', 'I', 'D' : Send Kp, Ki, and Kd gains, respectively
# 's' : Start sine control
# 'k' : Update wm_ref and use OL Control method
# 'c' : Update wm_ref and use CL Control method


# File name
fileName     = 'Demonstration_2.csv'

# EDIT HERE START #
# Fill out to get desired motion
# Starting commands will lift weight only
# You need to edit to get full motion
commandTimes = [     0,   0,   0,   0,   1,         1+run_time*1.05, 6+run_time, 6+run_time*2*.975 ] # Time to send command
commandData  = [OLgain,  Kp,  Ki,  Kd,   ref_speed, 0,          -ref_speed,0 ] # Value to send over
commandTypes = [   'f', 'P', 'I', 'D', 'c',       'c',        'c' , 'c'] # Type of command to send
print(commandTimes)
print(commandData)
# END EDIT HERE #

#%% Communication with Arduino
#----------------------------------------------------------------------
# Do not edit code below
#----------------------------------------------------------------------
# initializes all required variables
s = SerialConnect(portName, fileName, baudRate, dataRate, \
                  dataNames, dataTypes, commandTimes, commandData, commandTypes)

# Connect to Arduino and send over rate
s.connectToArduino()

# Start Recording Data
print("Recording...")

# Collect data
while len(s.dataStore[0]) < numDataPoints:
    s.getSerialData()
    
    s.sendCommand() # send command to arduino if ready
    
    # Print number of seconds that have passed
    if len(s.dataStore[0]) % dataRate == 0:
        print(len(s.dataStore[0]) /dataRate)   

# Close Arduino connection and save data
s.close()
