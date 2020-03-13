/* 
  Speeds for Navigation.c
  
  Navigate by making your ActivityBot go certain speeds for certain amounts
  of time.

  http://learn.parallax.com/activitybot/set-certain-speeds
*/


#include "simpletools.h"                      // simpletools library
#include "abdrive360.h"                          // abdrive library
#include "adcDCpropab.h" 

int main()                   
{
  //left
  //stop
  //turn around(180)
  //forward
  //distance monitor?
 //drive_speed(64, 64);                       // Forward 64 tps for 2 s
// pause(2000);
 //drive_speed(0, 0);
// drive_speed(26, 0);                        // Turn 26 tps for 1 s
// pause(1000);
// drive_speed(0, 0);
// drive_speed(128, 128);                     // Forward 128 tps for 1 s
// pause(1000);
// drive_speed(0, 0);
// freqout(10, 1000, 3000);  
// pause(1000);

 int var = 5;
 adc_init(21, 20, 19, 18); 
 float v1,v2;
  ////int buzzer = output(10);
  //dac_ctr(2, 0, 194);
 while (var < 7){
 float cam_data = input(11);
 v1 = adc_volts(3);
 v2 = adc_volts(2);
 print("A/D3 = %f V%c\n", v2, CLREOL);     // Display volts
  pause(1000);
 }    
}