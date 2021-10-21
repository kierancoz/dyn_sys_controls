/* 
 * ------------------------------------------------------------------------------
 * This Arduino sketch sends time data and specified signals to Python
 * Data is sent over as byte packets
 * This version sends time and one voltage signal from analog input A0
 * Students will need to update the code to read signal from another analog input
 * channel and send that data over to the computer
 * It is only necessary to update code within the 3 EDIT/END-EDIT sections
 * Data types in Python DAQ code need to match data types output from this sketch
 * ------------------------------------------------------------------------------
 */

unsigned long timer = 0;    // used to check current time [microseconds]
long loopTime = 0;       // default time between updates, but will be set in python Code [microseconds]
bool initLooptime = false;  // boolean (T/F) to check if loop time has already been set
bool stopProgram = false;

const int pin0 = A0;          // Pin use to collect analog data from potenitometer
int analogVal0 = 0;          // variable to store potentiometer data [ints]
float voltage0 = 0;          // variable to store potentiometer voltage [V] 

const int pin1 = A1;          // Pin use to collect analog data from potenitometer
int analogVal1 = 0;          // variable to store potentiometer data [ints]
float voltage1 = 0;          // variable to store potentiometer voltage [V] 

// ------EDIT------------- //
// Initialize variables to collect data from other analog input here


// -----END-EDIT---------- //


float int2volt = 5.0/1023.0; // Conversion constant from ints to volts [V/int]

void setup() {
  SerialUSB.begin(19200);         // Being SerialUSB comms and set Baud rate
  pinMode(LED_BUILTIN, OUTPUT); // Set builting LED pin (13) to output
  timer = micros();             // start timer
}
 
void loop() {

  if (SerialUSB.available() > 0) {       // if data is available
    String str = SerialUSB.readStringUntil('\n');
    readFromPC(str);
  }
  if (initLooptime && !stopProgram)      // once loop time has been initialized
  {
  
    timeSync(loopTime);   // sync up time to mach data rate
  
    analogVal0 = analogRead(pin0); // get analog data from pin
    voltage0 = (float)analogVal0*int2volt; // convert to volts

    analogVal1 = analogRead(pin1); // get analog data from pin
    voltage1 = (float)analogVal1*int2volt; // convert to volts

  // ------EDIT------------- //
  // read and convert inputs from other analog input here
  
  // -----END-EDIT---------- //
  
    unsigned long currT = micros();  // get current time
    
    // Send data over SerialUSB line to computer
    sendToPC(&currT);
    sendToPC(&voltage0);
    sendToPC(&voltage1);
    
  // ------EDIT------------- //
  // Send voltage value from other analog input here
  // -----END-EDIT---------- //
  
  }
  else if (initLooptime && stopProgram)
  {
    // Do nothing
  }

}

/*
 * Timesync calculates the time the arduino needs to wait so it 
 * outputs data at the specified rate
 * Input: deltaT - the data transfer period in microseconds
 */
void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();  // get current time
  long timeToDelay = deltaT - (currTime - timer); // calculate how much time to delay for [us]
  
  if (timeToDelay > 5000) // if time to delay is large 
  {
    // Split up delay commands into delay(milliseconds)
    delay(timeToDelay / 1000);

    // and delayMicroseconds(microseconds)
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0) // If time to delay is positive and small
  {
    // Use delayMicroseconds command
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative or zero so don't delay at all
  }
  timer = currTime + timeToDelay;
}


void readFromPC(const String input)
{
  int commaIndex = input.indexOf(',');
  char command = input.charAt(commaIndex - 1);
  String data = input.substring(commaIndex + 1);    
  int rate = 0;
  switch(command)
  {
    case 'r':
      // rate command
      rate = data.toInt();
      loopTime = 1000000/rate;         // set loop time in microseconds to 1/frequency sent
      initLooptime = true;             // no longer check for data
      timer = micros();
      break;
    case 's':
      // stop command
      stopProgram = true;
      break;
    default:
    // Otherwise, do nothing
      break;
  
  }

}

// ------------------------------------------------------------------------------------------------------------
// Send Data to PC: Methods to send different types of data to PC
// ------------------------------------------------------------------------------------------------------------

void sendToPC(int* data)
{
  byte* byteData = (byte*)(data);
  SerialUSB.write(byteData, 2);
}

void sendToPC(float* data)
{
  byte* byteData = (byte*)(data);
  SerialUSB.write(byteData, 4);
}
 
void sendToPC(double* data)
{
  byte* byteData = (byte*)(data);
  SerialUSB.write(byteData, 4);
}

void sendToPC(unsigned long* data)
{
  byte* byteData = (byte*)(data);
  SerialUSB.write(byteData, 4);
}
