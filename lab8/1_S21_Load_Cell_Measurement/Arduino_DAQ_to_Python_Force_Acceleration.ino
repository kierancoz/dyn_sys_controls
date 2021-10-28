#include <Wire.h>              // Must include Wire library for I2C
#include "SparkFun_Qwiic_Scale_NAU7802_Arduino_Library.h" // Click here to get the library: http://librarymanager/All#SparkFun_NAU7802
#include <SparkFunLSM6DSO.h> // Click here to get the library: http://librarymanager/All#SparkFun_MMA8452Q

NAU7802 myScale; //Create instance of the NAU7802 class
LSM6DSO IMU;   

unsigned long timer = 0;    // used to check current time [microseconds]
long loopTime = 0;       // default time between updates, but will be set in python Code [microseconds]
bool initLooptime = false;  // boolean (T/F) to check if loop time has already been set
bool stopProgram = false;

long currentReading = 0; // Raw Force reading

// IMU Readings
int rawAccX = 0;
int rawAccY = 0;
int rawAccZ = 0;

int rawGyroX = 0;
int rawGyroY = 0;
int rawGyroZ = 0;



void setup() {
  Serial.begin(38400);         // Being serial comms and set Baud rate
  Wire.begin();
  if ((myScale.begin() == false) || (IMU.begin() == false)){ // Waits until accelerometer connection is made
    while(1);
  }
  IMU.initialize(BASIC_SETTINGS);
  IMU.setAccelRange(4); 

  timer = micros();             // start timer
}
 
void loop() {

  if (Serial.available() > 0) {       // if data is available
    String str = Serial.readStringUntil('\n');
    readFromPC(str);
  }
  if (initLooptime && !stopProgram)      // once loop time has been initialized
  {
  
    timeSync(loopTime);   // sync up time to mach data rate
    unsigned long currT = micros();  // get current time
    currentReading = myScale.getReading(); // get raw Force data
    rawAccX = IMU.readRawAccelX();     // get X acceleration raw data (Integer value)
    rawAccY = IMU.readRawAccelY();     // get Y acceleration raw data (Integer value)
    rawAccZ = IMU.readRawAccelZ();     // get Z acceleration raw data (Integer value)

    rawGyroX = IMU.readRawGyroX();     // get X gyro raw data (Integer value)
    rawGyroY = IMU.readRawGyroY();     // get Y gyro raw data (Integer value)
    rawGyroZ = IMU.readRawGyroZ();     // get Z gyro raw data (Integer value)

        
    // Send data over serial line to computer
    sendToPC(&currT);
    sendToPC(&currentReading);
    sendToPC(&rawAccX);
    sendToPC(&rawAccY);
    sendToPC(&rawAccZ);
    sendToPC(&rawGyroX);
    sendToPC(&rawGyroY);
    sendToPC(&rawGyroZ);
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
  Serial.write(byteData, 2);
}

void sendToPC(float* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
 
void sendToPC(double* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}

void sendToPC(unsigned long* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}

void sendToPC(long* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
