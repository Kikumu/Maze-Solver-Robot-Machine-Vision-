#include "simpletools.h"
#include "abdrive.h"

int distLeft[4], distRight[4];
 
int main()
{
  drive_getTicks(&distLeft[0], &distRight[0]);
  //int var = 5;
  //adc_init(21, 20, 19, 18); 
 // float v1,v2;
  ////int buzzer = output(10);
  //dac_ctr(2, 0, 194);
 //while (var < 7){
  //float cam_data = input(11);
 // v1 = adc_volts(3);
 // v2 = adc_volts(2);
 // print("A/D3 = %f V%c\n", v2, CLREOL);     // Display volts
 // pause(1000);
//}  
  print("distLeft[0] = %d, distRight[0] = %d\n", distLeft[0], distRight[0]);
  int var = 5;
  
  while(var < 7){
     drive_speed(64, 64);                       // Forward 64 tps for 2 s
  pause(2000);
  drive_speed(0, 0);

  drive_speed(26, 0);                        // Turn 26 tps for 1 s
  pause(1000);
  drive_speed(0, 0);

  drive_speed(128, 128);                     // Forward 128 tps for 1 s
  pause(1000);
  drive_speed(0, 0);
  drive_speed(80, 60);
  pause(2000);
  drive_speed(0, 0);

  drive_getTicks(&distLeft[1], &distRight[1]);

  print("distLeft[1] = %d, distRight[1] = %d\n", distLeft[1], distRight[1]);
    }
 
}