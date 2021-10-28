#include <Wire.h>              // Must include Wire library for I2C
#include "SparkFun_Qwiic_Scale_NAU7802_Arduino_Library.h" // Click here to get the library: http://librarymanager/All#SparkFun_NAU7802

NAU7802 myScale; //Create instance of the NAU7802 class

unsigned long timer = 0;    // used to check current time [microseconds]
long loopTime = 0;       // default time between updates, but will be set in python Code [microseconds]
bool initLooptime = false;  // boolean (T/F) to check if loop time has already been set
bool stopProgram = false;

long currentReading = 0;

void setup() {
  SerialUSB.begin(19200);         // Being SerialUSB comms and set Baud rate
  Wire.begin();
  if (myScale.begin() == false){ // Waits until accelerometer connection is made
    while(1);
  }  
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
    unsigned long currT = micros();  // get current time
    currentReading = myScale.getReading();

        
    // Send data over SerialUSB line to computer
    sendToPC(&currT);
    sendToPC(&currentReading);
  
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
  // "r,50"
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

void sendToPC(long* data)
{
  byte* byteData = (byte*)(data);
  SerialUSB.write(byteData, 4);
}
