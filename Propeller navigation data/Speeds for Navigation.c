#include "simpletools.h"                      // simpletools library
#include "abdrive.h"                          // abdrive library
#include "adcDCpropab.h" 

int main()                   
{
adc_init(21, 20, 19, 18); 
int var = 5;
float v0,v1,v2,v3,turn_around,status;
//26,13,5
//--------------------------------------loop-----------------------------------------------//
 while (var < 7){
turn_around = input(10);
//v2 = input(1);
//v1 = adc_volts(2);
//v0=  adc_volts(1);
v0 = input(0);//26
v1 = input(1);//13
v2 = input(2);//5(6 for the model b pi3)
//forward
if(v0 > 0){
  drive_speed(25, 25);
  }
else if(v0 < 1){
  drive_speed(0, 0);
}
 
//adjust left
if(v1 > 0){
    drive_speed(25, 0);
}
//else if(v1 < 1){
//  drive_speed(0, 0);
//}  


//adjust right
if(v2 > 0)
{
  drive_speed(0, 25);
} 
//else if(v2 < 1)
//{
//   drive_speed(0, 0);
//}  
 
//print("A/D3 = %f V%c\n", v2, CLREOL);     // Display volts
//pause(1000);
 }    
}
