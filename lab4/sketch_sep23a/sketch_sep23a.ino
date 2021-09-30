void setup() 
{
  //pinMode(A0, INPUT);
  SerialUSB.begin(9600);
}

void loop() 
{
  //digitalWrite(RX_LED, LOW); // RX LED on
  delay(333);
  SerialUSB.println(analogRead(A0));
}
