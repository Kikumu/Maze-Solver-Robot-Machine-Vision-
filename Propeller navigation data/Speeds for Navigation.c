#include "simpletools.h"                      // simpletools library
#include "abdrive.h"                          // abdrive library
#include "adcDCpropab.h" 

int main()                   
{
int var = 5;
float v0,v1,v2,v3,v4,turn_around,status;
//26,13,5
//--------------------------------------loop-----------------------------------------------//
 while (var < 7){
v0 = input(0);//26
v1 = input(1);//13
v2 = input(2);//5(6 for the model b pi3)
v3 = input(3);//16
v4 = input(4);//20
//forward
if(v0 > 0){
  drive_ramp(25, 25);
  }
else if(v0 < 1){
  drive_ramp(0, 0);
}
 
//adjust left
if(v1 > 0){
    drive_ramp(15, 0);
}
//adjust right
if(v2 > 0)
{
  drive_ramp(0, 15);
} 
//turn right 45
if (v3 > 0)
{
  drive_ramp(25,25);
  pause(200);
  drive_ramp(0,52);
  pause(1000);
}
if (v4 > 0){
  drive_ramp(0,52);
  pause(200);
  drive_ramp(-52,0);
  pause(200);
}

//turn left 45
//if (v4 > 0)
//{
//  drive_speed(52,0);
//}
//print("A/D3 = %f V%c\n", v3, CLREOL);     // Display volts
//pause(1000);
 }    
}
