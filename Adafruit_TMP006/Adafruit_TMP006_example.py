#!/usr/bin/python

from Adafruit_TMP006 import TMP006
from time import sleep

def C_to_F(C):
  return C * (180.0 / 100.0) + 32.0

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the TMP006 and use defaults
# tmp = TMP006(0x40, debug=True)
tmp = TMP006(0x41)

# Start sampling
tmp.begin()

# Wait a short bit for sample averaging
while True:
  print "Pausing 2.0 s..."
  sleep(2.0)

  dietemp = tmp.readDieTempC()
  objtemp = tmp.readObjTempC()

  print "Die Temperature:    %.2f C / %.2f F" % (dietemp, C_to_F(dietemp))
  print "Object Temperature: %.2f C / %.2f F" % (objtemp, C_to_F(objtemp))

