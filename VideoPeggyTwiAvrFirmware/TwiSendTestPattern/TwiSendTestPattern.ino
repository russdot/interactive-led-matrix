#include <Wire.h>

// code to demonstrate sending a test pattern 
// generated on the Arduino to the Peggy via TWI

#define PEGGY_ADDRESS 34

#define TWI_FREQ 200000

void setup()
{
  Wire.begin();

  // jack up the frequency for TWI.
  TWSR &= ~(1<<TWPS0);
  TWSR &= ~(1<<TWPS1);
  TWBR = ((F_CPU / TWI_FREQ) - 16) / 2;
  
  PORTC |=  (1<<PC5) | (1<<PC4); // enable pullups

}


uint8_t header[6] = { 0xde, 0xad, 0xbe, 0xef, 1,0 };


// the display buffer
#define BUFFER_SIZE 325
uint8_t buffer[BUFFER_SIZE];

// send the buffer contents to the Peggy.
void sendBuffer()
{
  uint8_t *ptr = header;
  int count = sizeof(header);
  
  Wire.beginTransmission(PEGGY_ADDRESS);
  while (count--)
  {
    Wire.write(*ptr++);
  }
  Wire.endTransmission();
  
  ptr = buffer;
  count = BUFFER_SIZE;
  count = 25;  

  while (count-- )
  {
    Wire.beginTransmission(PEGGY_ADDRESS);
    Wire.write(ptr,13);
    ptr+=13;
    Wire.endTransmission();
  }
}

uint8_t v = 0;
int frameCounter =0;


void loop()
{
  v=frameCounter %16;
  
  uint8_t * ptr = buffer;
 
  for (uint8_t i =0; i <24; i++)
  {
    for (uint8_t  j = 0; j < 13; j++)
    {
       *ptr++ =(v % 16) |  (((v+1)%16)<<4);
       v+=2;
    }
    v+=5;
  }
 
  v=0;
  for (uint8_t i =0; i <26; i++)
  {
    if (i == (frameCounter%25))
       v=(v>>4) | 0xf0;
    else
       v=v>>4;
    if (i%2==1)
      *ptr++ =(v%256);
  }
  frameCounter++;
  sendBuffer();  
}
  
  
   
