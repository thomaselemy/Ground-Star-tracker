// Arduino Uno
// Receives A ,Switches on LED on Pin13 for 2 seconds
// Rahul.S

// (c) www.xanthium.in 2021
// Tutorial - https://www.xanthium.in/Cross-Platform-serial-communication-using-Python-and-PySerial
// defines pins numbers
const int stepPin_pan = 2; //step pin for x stepper driver
const int dirPin_pan = 5; //dir pin for x stepper driver

// defines pins numbers
const int stepPin_tilt = 3; //step pin for y stepper driver
const int dirPin_tilt = 6; //dir pin for y stepper driver

const int dirPin_focus = 7;  //6 for y, 7 for z
const int stepPin_focus = 4;  //3 for y, 4 for z

const int enablePin = 8;

int numberOfSteps = 5000;
int teststeps = 8000;
int faststeps = 20000;
//byte ledPin = 13;
int pulseWidthMicros = 20;  // microseconds
int millisbetweenSteps = 1.5; // milliseconds - or try 1000 for slower steps

int fastbetweenstep = 0.8;

void setup()
{
  
pinMode(enablePin,OUTPUT);
pinMode(stepPin_pan,OUTPUT); 
pinMode(dirPin_pan,OUTPUT);

pinMode(stepPin_tilt,OUTPUT); 
pinMode(dirPin_tilt,OUTPUT);

pinMode(stepPin_focus,OUTPUT); 
pinMode(dirPin_focus,OUTPUT);

digitalWrite(enablePin, LOW);
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps 8N1

}

void loop()
{
  char RxedByte = 0;

 if (Serial.available()) 
    {
      
      RxedByte = Serial.read();    
       
      switch(RxedByte)
      {  
        
        //drive the motor up
        case 'U':  //up motor movment from camera
        digitalWrite(dirPin_tilt,HIGH);
        digitalWrite(enablePin,LOW);
        Serial.println('U');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_tilt, HIGH);
         //delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_tilt, LOW);
    
          delay(millisbetweenSteps);
    
 }
                   break;

//also drive the motor up but faster
        case 'u':  //up motor movment from gui
        digitalWrite(dirPin_tilt,HIGH);
        digitalWrite(enablePin,LOW);
        Serial.println('u');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_tilt, HIGH);
         //delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_tilt, LOW);
    
          delay(fastbetweenstep);
    
 }
                   break;
       
        
        case 'D': //down motor movment from camera
        digitalWrite(dirPin_tilt,LOW);
        digitalWrite(enablePin,LOW);
        Serial.println('D');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_tilt, HIGH);
         //delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_tilt, LOW);
    
          delay(millisbetweenSteps);
    
 }
                   break;
  //also drive the motor down but faster 
        case 'd': //down motor movment from camera
        digitalWrite(dirPin_tilt,LOW);
        digitalWrite(enablePin,LOW);
        Serial.println('d');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_tilt, HIGH);
         //delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_tilt, LOW);
    
          delay(fastbetweenstep);
    
 }
                   break;

        case 'L':  //left motor movment from camera
         digitalWrite(dirPin_pan,HIGH);
         digitalWrite(enablePin,LOW);
        Serial.print('L');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_pan, HIGH);
         delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_pan, LOW);
    
          delay(millisbetweenSteps);
 }
                   break;
        //also drive the motor left but faster             
        case 'l':  //left motor movment from gui
        digitalWrite(dirPin_pan,HIGH);
        digitalWrite(enablePin,LOW);
        Serial.print('l');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_pan, HIGH);
         //delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_pan, LOW);
    
          delay(fastbetweenstep);
 }
                   break;
        case 'R': //right motor movment from camera
        digitalWrite(dirPin_pan,LOW);
        digitalWrite(enablePin,LOW);
        Serial.print('U');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_pan, HIGH);
         delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_pan, LOW);
    
          delay(millisbetweenSteps);
 }          
                   break;
    //also drive the motor right but faster                 
        case 'r': //right motor movment from camera
        digitalWrite(dirPin_pan,LOW);
        digitalWrite(enablePin,LOW);
        Serial.print('U');
       for(int n = 0; n < numberOfSteps; n++) {
         digitalWrite(stepPin_pan, HIGH);
         //delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_pan, LOW);
    
          delay(fastbetweenstep);
 }          
                   break;
        case 'F':  //focus forward
        digitalWrite(dirPin_focus,HIGH);
        digitalWrite(enablePin,LOW);
        Serial.print("Focus forward");
       for(int n = 0; n < teststeps; n++) {
         digitalWrite(stepPin_focus, HIGH);
        // delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_focus, LOW);
    
          delay(.9);
 }
                   break;  
         case 'B':  //focus other direction
        digitalWrite(dirPin_focus,LOW);
        digitalWrite(enablePin,LOW);
        Serial.print("Focus backward");
       for(int n = 0; n < teststeps; n++) {
         digitalWrite(stepPin_focus, HIGH);
        // delayMicroseconds(pulseWidthMicros); // this line is probably unnecessary
         digitalWrite(stepPin_focus, LOW);
    
          delay(.9);
 }
                   break;                             
        default:
                   break;
      }//end of switch()
    }//endof if 
}
      