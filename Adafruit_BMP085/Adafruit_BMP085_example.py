#!/usr/bin/python

from time import sleep
from Adafruit_BMP085 import BMP085

def C_to_F(C):
  return C * (180.0 / 100.0) + 32.0

def m_to_ft(m):
  return 3.2808399 * m

def hPa_to_inHg(hPa):
  return hPa / 33.86389

def hPa_to_psi(hPa):
  return hPa / 0.0145037

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True)
bmp = BMP085(0x77)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode

while True:
  temp = bmp.readTemperature()
  pressure = bmp.readPressure()
  altitude = bmp.readAltitude()

  print "Temperature: %.2f C / %.2f F" % (temp, C_to_F(temp))
  print "Pressure:    %.2f hPa / %.2f inHg" % ((pressure / 100.0), hPa_to_inHg(pressure / 100.0))
  print "Altitude:    %.2f m / %.1f ft" % (altitude, m_to_ft(altitude))
  sleep(2.0)
