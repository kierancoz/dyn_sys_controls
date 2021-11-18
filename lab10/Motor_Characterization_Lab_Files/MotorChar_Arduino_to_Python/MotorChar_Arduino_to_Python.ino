// ------------------------------------------------------------------------------------------------------------
// Motor Characterization Lab: PWM Step Arduino Code
// This code is meant to show output dynamic motor data for steps in PWM output.  
// Python code required: 
// ------------------------------------------------------------------------------------------------------------
// NOTE TO STUDENTS: Here is a list of things you will have to adjust
// 1) Your Motor Pin definitions (see Define Motor Pins Section).  Make sure these align with the pin numbers you used when wiring to the digital Arduino pins
// 2) Make sure your Python code BAUD rate is set to same value (19200 for this code)
// ------------------------------------------------------------------------------------------------------------
// Use this code to grab data required to characterize motor: Parameters rm & Bm, Torque-Speed Curve, Current Approximations
// ------------------------------------------------------------------------------------------------------------

// ------------------------------------------------------------------------------------------------------------
// Include Libraries
// ------------------------------------------------------------------------------------------------------------
#include <Wire.h>
#include <SparkFun_TB6612.h>


// ------------------------------------------------------------------------------------------------------------
// Define Motor Pins
// ------------------------------------------------------------------------------------------------------------
// Motor Pins
#define AIN1 7
#define AIN2 6
#define PWMA 5 // Has tilde on digital output pin
#define STBY 8

// Motor Vars
const int offsetA = 1;
Motor motor1 = Motor(AIN1, AIN2, PWMA, offsetA, STBY); // This addresses all relevant pins to the motor output
int motorPwm = 0; // 100 is minimum to overcome stiction in my motor
float PWMout = 255;
float PWM_ratio = 0;
int MotorPwm = motorPwm;

// ------------------------------------------------------------------------------------------------------------
// Encoder variable initialization
// ------------------------------------------------------------------------------------------------------------
// Enc_count_rev: Equals 6 or 3 for CHANGE or RISING/FALLING mode per interrupt; Equals 12 for 2 interrupts on CHANGE mode
#define ENC_COUNT_REV 12 
#define ENC_IN 3
#define ENC2_IN 2
volatile long encoderVal1 = 0;
volatile long encoderVal2 = 0;
long interval = 1;
unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
unsigned long dt = 1000;
float rps = 0; // Motor speed: Rotations per second
float output_rps = 0; // Output shaft speed: Rotations per second
float GR = 45; // Gear ratio

// ------------------------------------------------------------------------------------------------------------
// General Variables
// ------------------------------------------------------------------------------------------------------------
float Enval = 0;
float dtval = 0;
int Pin0    = 0;
int int_A0  = 0;
float f_A0  = 0;
float int2V = 0.00488759; // 5V range divided by 10-bit (0-1023) integer value
float Tval  = 0;
float Tc_test    = 0;
float Tstep = 0;
float Vbus  = 5; // DC Power Supply Voltage [V]
float n     = 6;

// Loop Timing vars
unsigned long timer = 0;    // used to check current time (microseconds)
long loopTime = 500000;       // microseconds
bool initLooptime = false;  // boolean to check if loop time has already been set
bool stopProgram = false;

// ------------------------------------------------------------------------------------------------------------
// Setup
// ------------------------------------------------------------------------------------------------------------
void setup() {
  // initialize serial communications at 115200 bps:
  Wire.begin();
  SerialUSB.begin(19200);

  // Set encoder as input with internal pullup
  pinMode(ENC_IN, INPUT);
  pinMode(ENC2_IN, INPUT);

  // Attach interrupt
  attachInterrupt(digitalPinToInterrupt(ENC_IN), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC2_IN), updateEncoder2, CHANGE);
}

// ------------------------------------------------------------------------------------------------------------
// Begin Loop
// ------------------------------------------------------------------------------------------------------------
void loop() {
  if (SerialUSB.available() > 0) {       // if data is available
    String str = SerialUSB.readStringUntil('\n');
    readFromPC(str);
  }
  if (initLooptime && !stopProgram)      // once loop time has been initialized
  {
    unsigned long currT = micros();  // set current time
    currentMillis = currT;
    dt = currentMillis - previousMillis;
    if (dt >= loopTime) {
      // Estimate motor and shaft speed based on number of encoder pulses
      previousMillis = currentMillis;
      Enval = (float) (encoderVal1 + encoderVal2);
      dtval = (float) dt;
      rps   = (float) Enval*1000000 / (ENC_COUNT_REV*dtval);
      output_rps = (rps / GR);
  
    // Step changes in PWM output based on time
    Tval  = (float) currT/1000000;
    Tstep = Tval - Tc_test;
  
    // Steps PWM +20 every n seconds
    // 14 Total changes, Tval needs to be greater than n*14
    n = 6;
    if (Tval > 90) {
      motorPwm = 0;}
    else if (Tstep >= n){
      motorPwm = motorPwm + 20;
      Tc_test = Tc_test + n;
    }
    
    
    if (motorPwm > 255) 
      motorPwm = 255;
    else if (motorPwm < -255)
      motorPwm = -255;
  
    // Send PWM to motor
    motor1.drive(motorPwm);  
    
    // Outputs
    PWMout = (float) motorPwm;
    PWM_ratio = PWMout/255; // Gives decimal from [-1,1] 
  
    // Read Vbus voltage
    int_A0 = analogRead(Pin0);
    f_A0   = (float) int_A0;
    Vbus   = (float) int2V*f_A0;
    float wm = rps*2*3.14159;    // [rad/s]
  
    // send data over
    sendToPC(&currT);    // Current Time [us]
    sendToPC(&Enval);    // Number of total pulses --> from both encoders (12 pulses per rev)
    sendToPC(&wm);       // Motor Speed [rad/s]
    sendToPC(&motorPwm); // PWM sent to motor [int]
    sendToPC(&Vbus);     // Bus Voltage input [V]
  
    // Reset encoder value before next loop
    encoderVal1 = 0;
    encoderVal2 = 0;
  
    }
  }
    else if (initLooptime && stopProgram)
  {
    motor1.drive(0);  // make sure motor stops
  }
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
// Update Encoder Function
// ------------------------------------------------------------------------------------------------------------
void updateEncoder()
{
  // Increment value for each pulse from encoder
  encoderVal1++;
}

void updateEncoder2()
{
  // Increment value for each pulse from encoder
  encoderVal2++;
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

void sendToPC(volatile long* data)
{
  byte* byteData = (byte*)(data);
  SerialUSB.write(byteData, 4);
}
