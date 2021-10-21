from ArduinoDAQ import SerialConnect
import numpy as np

portName = 'COM4'                      # Communications port name. Make sure it matches port in Arduino IDE
# portName = '/dev/ttyUSB0'
baudRate   = 19200                     # Baud Rate
dataRate   = 100                       # Acquisition data rate (Hz), do not exceed 500
recordTime = 20                        # Number of seconds to record data
numDataPoints = recordTime * dataRate  # Total number of data points to be saved

#%% Data lists and Arduino commands
#----------------------------------------------------------------------
# Data to read from Arduino file
#----------------------------------------------------------------------
dataNames = ['Time', 'accX', 'accY', 'accZ', 'wx', 'wy', 'wz']
dataTypes = [  '=L',   '=h',   '=h',   '=h', '=h', '=h', '=h']

#---------------------------------------------------------------------- 
# Command strings that can be sent to Arduino
#----------------------------------------------------------------------
rate_c     = 'r' # Data rate command
stop_c     = 's' # Data rate command


#%% Command data structures 
# Set recordTime variable to 10 seconds
#----------------------------------------------------------------------
commandTimes = [recordTime] # Time to send command
commandData  = [0] # Value to send over
commandTypes = ['s'] # Type of command
fileName     = 'periodic_rotational.csv'


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
