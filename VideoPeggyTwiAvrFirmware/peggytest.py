#!/usr/bin/python
#
# Copyright 2008 by Jay Clegg.  Released under GPL license.
#
# a simple test app that sends some data to the serial peggy. 
# It just makes a scrolling test pattern, with  a 'chaser' led at the bottom,
# which can be used to verify throughput speed.

import serial, array, sys
import time

# LOOK!: change the port variable to match your serial port name
#portName = '/dev/tty.SparkFun-BT-SerialPort-1'
portName = '/dev/tty.usbserial-XXXXXXX'


###########################################################################

# initialize serialPort
def initSerial(name):
	# globally scoped variable
	global serialPort
	# open a port at 115k baud
	serialPort = serial.Serial(name, 115200)   #, timeout=1)
	
###########################################################################

# standard header is 0xdeadbeef (sent in big endian order), 
# followed by a 1 and a 0 (currently these are reserved values)
header = chr(0xde) + chr(0xad) + chr(0xbe) + chr(0xef) + chr(1) + chr(0)

#
# write an array of packed bytes to the serial port, prepending
# the header bytes first
#
def writeFrame(lst):
	# writing one byte at a time is inefficient... 
	# buffering into an array is much faster.
	st = array.array('B', lst).tostring();

	# wait for any previous bytes to get flushed out...
	# keeps the port from getting "backed up", and seems to
	# save the CPU a lot of work..
	serialPort.flush() 
	# write the magic header
	
	serialPort.write(header);
	serialPort.write(st);

###########################################################################

def loopTestPattern():
	v = 0
	frameCounter =0
	
	while 1:
		lst = []
		
		# moving testpattern on first 24 rows
		v= frameCounter % 16
		
		# write ascending brightness values, and
		for i in xrange(24):  # first 24 rows
			for j in xrange(13):   # 25 cols * 4bits == 13 bytes (rounded)
				lst.append( (v) % 16 |  ((v + 1) % 16)  << 4) 
				v=v+2
			v=v+5  # tweak for asthetic reasons
	
		# 'chaser' led on the last row.  
		v = 0
		for i in xrange(26):
		
			if (i == (frameCounter % 25)):
				v = (v >> 4) | 0xf0	
			else:
				v = (v >> 4) 
	
			if ((i%2) == 1):
				lst.append( v % 256 )
	
		#Send it out...	
		writeFrame(lst)
		frameCounter = frameCounter + 1
		
###########################################################################


#  " main method "

print "Sending test pattern, Press Control-C to exit";
time.sleep(1.2)

try:
	initSerial(portName)
	loopTestPattern()
except KeyboardInterrupt:
	print "User abort!"
#except:
#    print "Unexpected error:", sys.exc_info()[0]
    	
if (serialPort):
	print "Closing serial port..."
	serialPort.close()



