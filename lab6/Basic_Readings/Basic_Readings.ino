/******************************************************************************
Basic_Readings.ino

https://github.com/sparkfun/SparkFun_Qwiic_6DoF_LSM6DSO
https://github.com/sparkfun/SparkFun_Qwiic_6DoF_LSM6DSO_Arduino_Library

Description:
Most basic example of use.

Example using the LSM6DSO with basic settings.  This sketch collects Gyro and
Accelerometer data every second, then presents it on the SerialUSB monitor.

Development environment tested:
Arduino IDE 1.8.2

This code is released under the [MIT License](http://opensource.org/licenses/MIT).
Please review the LICENSE.md file included with this example. If you have any questions 
or concerns with licensing, please contact techsupport@sparkfun.com.
Distributed as-is; no warranty is given.
******************************************************************************/

#include "SparkFunLSM6DSO.h"
#include "Wire.h"
//#include "SPI.h"

LSM6DSO myIMU; //Default constructor is I2C, addr 0x6B

void setup() {


  SerialUSB.begin(115200);
  delay(500); 
  
  Wire.begin();
  delay(10);
  if( myIMU.begin() )
    SerialUSB.println("Ready.");
  else { 
    SerialUSB.println("Could not connect to IMU.");
    SerialUSB.println("Freezing");
  }

  if( myIMU.initialize(BASIC_SETTINGS) )
    SerialUSB.println("Loaded Settings.");

}


void loop()
{
  //Get all parameters
  SerialUSB.print("\nAccelerometer:\n");
  SerialUSB.print(" X = ");
  SerialUSB.println(myIMU.readFloatAccelX(), 3);
  SerialUSB.print(" Y = ");
  SerialUSB.println(myIMU.readFloatAccelY(), 3);
  SerialUSB.print(" Z = ");
  SerialUSB.println(myIMU.readFloatAccelZ(), 3);

  SerialUSB.print("\nGyroscope:\n");
  SerialUSB.print(" X = ");
  SerialUSB.println(myIMU.readFloatGyroX(), 3);
  SerialUSB.print(" Y = ");
  SerialUSB.println(myIMU.readFloatGyroY(), 3);
  SerialUSB.print(" Z = ");
  SerialUSB.println(myIMU.readFloatGyroZ(), 3);

  SerialUSB.print("\nThermometer:\n");
  SerialUSB.print(" Degrees F = ");
  SerialUSB.println(myIMU.readTempF(), 3);
  
  delay(1000);
}
