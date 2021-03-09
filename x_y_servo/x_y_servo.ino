#include <Servo.h>

Servo x_axis;
Servo y_axis;

long int data;

void setup() {
  Serial.begin(115200);
  
  x_axis.attach(9); 
  x_axis.write(90);
  
  y_axis.attach(10); 
  y_axis.write(115);
}

void loop() {  
   if(Serial.available() > 2){
    data =Serial.parseInt();
    
    if (data < 0){
      x_axis.write(-1 * data);
     }
     
    else{
      y_axis.write(data);
     }
   }  
} 
