# interactive-led-matrix
Interactive LED matrix project based off the Peggy2 board (http://www.evilmadscientist.com/2008/peggy-version-2-0/) consisting of two parts:

1. A Peggy2 LED matrix board (http://www.evilmadscientist.com/2008/peggy-version-2-0)
2. Arduino Diecimila (https://www.arduino.cc/en/Main/arduinoBoardDiecimila)

The Peggy2 LED board has 625 addressible LEDs (25 x 25) with 16-level brightness capability. This project involves sending serialized byte arrays (frame buffers) via USB to an Arduino acting as a TWI/I2C master device, which then transmits the data over 3-wire TWI/I2C to a modified Peggy2 board for real-time display.

#Installation + Setup
These instructions have been compiled from the firmware README provided by [Jay Clegg](http://planetclegg.com/projects/Twi2Peggy.html) and my own setup steps.
###Firmware Installation (Peggy2 board)
The Peggy2 LED board must be configured as a TWI/I2C slave device. See the [README](https://github.com/russdot/interactive-led-matrix/blob/master/VideoPeggyTwiAvrFirmware/README.txt) for installing firmware code on unmodified Peggy2.
###Wiring
See [Hardware Interfacing Instructions](http://planetclegg.com/projects/Twi2Peggy.html)
###Serial Receiver Setup (Arduino)
#####Test Pattern
Using the Arduino development IDE, upload the [TwiSendTestPattern](https://github.com/russdot/interactive-led-matrix/blob/master/VideoPeggyTwiAvrFirmware/TwiSendTestPattern.pde) sketch to the Arduino. Confirm the test pattern is displayed on the LED board.
#####Serial Receiver
Using the Arduino development IDE, upload the [Serial2TwiPeggy](https://github.com/russdot/interactive-led-matrix/blob/master/VideoPeggyTwiAvrFirmware/Serial2TwiPeggy.pde) sketch to the Arduino. This sets up the Arduino to receive serial input from a computer via USB.

###Serial Sender Setup
From a PC (or Raspberry Pi), run the [peggytest](https://github.com/russdot/interactive-led-matrix/blob/master/VideoPeggyTwiAvrFirmware/peggytest.py) python script, taking care to change the serial port to the correct value.

## Credits
- Jay Clegg (http://planetclegg.com/projects/Twi2Peggy.html)
- Evil Mad Scientist (http://www.evilmadscientist.com/2008/peggy-version-2-0/)
