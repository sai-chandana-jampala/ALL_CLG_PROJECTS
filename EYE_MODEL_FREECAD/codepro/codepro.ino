int m=0; // Taking a variable for soil moisture sensor
int red=2;// taking digital pin 2 for output
int blue=3;// taking digital pin 3 for output
const int buzzer = 9; //buzzer to arduino pin 9
void setup() {
  // put your setcode here, to run once:
pinMode(A0, INPUT_PULLUP); //Giving input through Analog pin
pinMode(8,OUTPUT);// And output to the relay
pinMode (red,OUTPUT);
pinMode (blue,OUTPUT);
pinMode(buzzer, OUTPUT);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:s
int value = analogRead(A1);// read the signal of water depth sensor
int m= analogRead(A0); //Read the signal 
Serial.println(m);
delay(200);
  if (m>=800)
{
  digitalWrite(8, HIGH);//MOTOR ON
  
  }

  
else if (m<800)
{
  digitalWrite(8, LOW);//MOTOR OFF
  }
 if (value > 500) {
    Serial.println("water there");//water in container is ok
    digitalWrite (red,HIGH);//red light will not glow
    digitalWrite(blue,LOW);//blue light will glow
 }
else{
    Serial.println("no water");//water in container is about to finish
    digitalWrite (blue,HIGH);//blue light will not glow
    digitalWrite (red,LOW);//red light will glow
    tone(buzzer, 1000); // Send 1KHz sound signal...
  delay(1000);        // ...for 1 sec
  noTone(buzzer);   
  delay(100);
  }
  }
  
