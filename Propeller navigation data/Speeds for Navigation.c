#include "simpletools.h"                      // simpletools library
#include "abdrive.h"                          // abdrive library
#include "adcDCpropab.h" 

int main()                   
{
int var = 5;
float v0,v1,v2,v3,v4,v7;
//26,13,5
//--------------------------------------loop-----------------------------------------------//
 while (var < 7){
v0 = input(0);//26
v1 = input(1);//13
v2 = input(2);//5(6 for the model b pi3)
v3 = input(3);//16
v4 = input(4);//20
v7 = input(7);//23
//pin(5) 12 is input

//forward
if(v0 > 0){
  high(5);
  drive_speed(25, 25);
  }
else if(v0 < 1){
  low(5);
  drive_speed(0, 0);
}
//adjust left
v1 = input(1);
if(v1 > 0){
  high(5);
  drive_speed(15, 0);
}
//adjust right
v2 = input(2);
if(v2 > 0)
{
  high(5);
  drive_speed(0, 15);
} 
//turn right 45
v3 = input(3);
if (v3 > 0)`
{
  high(5);//12
  drive_speed(30,30);
  pause(400);
  drive_speed(0,0);
  drive_speed(0,50); //52
  pause(1000);
  drive_speed(0,0);
  pause(1000);
}
v7 = input(7);
//turn left 45
if (v7 > 0){
  high(5);
  drive_speed(30,30);
  pause(400);
  drive_speed(0,0);
  drive_speed(50,0); //52
  pause(1000);
  drive_speed(0,0);
  pause(1000); 
}  

//turn around
v4 = input(4);//20(check input status due to pause)
if ((v4 > 0)&&(v0 < 1)&&(v2 < 1)){
 drive_speed(0,52);
 pause(1000);
 drive_speed(-52,0);
 pause(1000);
 drive_speed(0,0);
 pause(1000);
 low(5);
}
//high(5);
//print("A/D3 = %f V%c\n", v7, CLREOL);     // Display volts
//pause(1000);
//low(5);
//pause(1000);
 }    
}