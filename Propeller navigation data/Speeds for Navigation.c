/* 
  Speeds for Navigation.c
  
  Navigate by making your ActivityBot go certain speeds for certain amounts
  of time.

  http://learn.parallax.com/activitybot/set-certain-speeds
*/


#include "simpletools.h"                      // simpletools library
#include "abdrive.h"                          // abdrive library
#include "adcDCpropab.h" 

int distLeft[4], distRight[4];
int main()                   
{
//adc_init(21, 20, 19, 18); 
int var = 5;
//float v1,v2,v3,v0,turn_around
int v1,v2,v3,v0,turn_around,status;
drive_getTicks(&distLeft[0], &distRight[0]);
print("distLeft[0] = %d, distRight[0] = %d\n", distLeft[0], distRight[0]);
int count = 0;
//--------------------------------------loop-----------------------------------------------//
 while (var < 7){
//v3 = adc_volts(3);  //left 26
//v2 = adc_volts(2);  //right 20
//v1 = adc_volts(1);  //forward 16
//v0 = adc_volts(0);  //turn around 21
turn_around = input(10);
v1 = input(1);
v2 = input(0);
v3 = input(2);

if(v1 >= 0){ //16
//forward movement
    switch(v1)
   {
     case 1:
      drive_speed(25, 25);
      status = 1;
      break;
     case 0:
      drive_speed(0, 0);
      status = 0;
      break;      
   }                    
  }
else if(turn_around >= 0){ //21
//360 movement
 switch(turn_around){
   case 1:
    if(status==0){
      drive_speed(45, 0);                       
      drive_speed(0, -45);
      }     
      break;
   case 0:
    if(status == 1){drive_speed(25, 25);}
    break;
   }
}
else if(v2 >= 0){ //20
//left
   switch(v2)
   {
     case 1:
      drive_speed(25, 0);
      break;
     case 0:
      if (status == 1){drive_speed(25, 25);}
      else if(status == 0){drive_speed(0, 0);}
      break;      
   }                        
 } 
else if(v3 >= 0){ //26
//right
    switch(v3)
   {
     case 1:
      drive_speed(0, 25);
      break;
     case 0:
      if (status == 1){drive_speed(25, 25);}
      else if(status == 0){drive_speed(0, 0);}
      break;      
   }                   
} 
//---------------remaining code is to turn 90 so that it can keep 'one hand on wall'
//print("A/D3 = %f V%c\n", turn_around, CLREOL);     // Display volts
 }    
}