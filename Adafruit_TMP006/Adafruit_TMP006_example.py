#!/usr/bin/python

from Adafruit_TMP006 import TMP006
from time import sleep

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the TMP006 and use defaults
# tmp = TMP006(0x40, debug=True)
tmp = TMP006(0x40)

# Start sampling
tmp.begin()

# Wait a short bit for sample averaging
sleep(1.5)

dietemp = tmp.readDieTempC()
objtemp = tmp.readObjTempC()

print "Die Temperature:    %.2f C" % dietemp
print "Object Temperature: %.2f C" % objtemp

