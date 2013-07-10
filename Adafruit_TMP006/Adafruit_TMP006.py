#!/usr/bin/python

import time
from Adafruit_I2C import Adafruit_I2C
from math import sqrt

# ===========================================================================
# TMP006 Class
# ===========================================================================

class TMP006 :
  i2c = None

  # TMP006 Registers
  __TMP006_REG_VOBJ   = 0x00
  __TMP006_REG_TAMB   = 0x01
  __TMP006_REG_CONFIG = 0x02
  __TMP006_REG_MANID  = 0xFE
  __TMP006_REG_DEVID  = 0xFF

  # CONFIG Register Values
  __TMP006_CFG_RESET    = 0x8000
  __TMP006_CFG_MODEON   = 0x7000
  __TMP006_CFG_1SAMPLE  = 0x0000
  __TMP006_CFG_2SAMPLE  = 0x0200
  __TMP006_CFG_4SAMPLE  = 0x0400
  __TMP006_CFG_8SAMPLE  = 0x0600
  __TMP006_CFG_16SAMPLE = 0x0800
  __TMP006_CFG_DRDYEN   = 0x0100
  __TMP006_CFG_DRDY     = 0x0080

  # Manufacturer ID
  __TMP006_MANID = 0x5449

  # Device ID
  __TMP006_DEVID = 0x0067

  # Internal Data
  __TMP006_B0 = -0.0000294
  __TMP006_B1 = -0.00000057
  __TMP006_B2 = 0.00000000463
  __TMP006_C2 = 13.4
  __TMP006_TREF = 298.15
  __TMP006_A2 = -0.00001678
  __TMP006_A1 = 0.00175
  __TMP006_S0 = 6.4  # * 10^-14

  # Constructor
  def __init__(self, address=0x40, mode=1, debug=False):
    self.i2c = Adafruit_I2C(address)

    self.address = address
    self.debug = debug
    self.started = False

  # Destructor
  def __del__(self):
    if self.started:
      self.i2c.write16(self.__TMP006_REG_CONFIG, 0);

  # Start Sampling
  def begin(self, samplerate=__TMP006_CFG_16SAMPLE):
    self.i2c.write16(self.__TMP006_REG_CONFIG,
                     self.__TMP006_CFG_MODEON | self.__TMP006_CFG_DRDYEN | samplerate);

    self.started = True

    mid = self.i2c.readU16(self.__TMP006_REG_MANID)
    did = self.i2c.readU16(self.__TMP006_REG_DEVID)

    if self.debug:
      print "mid = 0x%x" % mid
      print "did = 0x%x" % did

    if mid != self.__TMP006_MANID:
      print "WARN TMP006: Manufacturer ID Mismatch (%04X)" % mid
    if did != self.__TMP006_DEVID:
      print "WARN TMP006: Device ID Mismatch (%04X)" % did

  def readRawDieTemperature(self):
    "Read the raw die temperature"
    raw = self.i2c.readS16(self.__TMP006_REG_TAMB)
    raw >>= 2
    if self.debug:
      C = raw * 0.03125
      print "Raw Tambient: 0x%04X (%f C)" % (raw, C)
    return raw

  def readRawVoltage(self):
    "Read the raw voltage"
    raw = self.i2c.readS16(self.__TMP006_REG_VOBJ)
    if self.debug:
      v = raw
      v *= 156.25
      v /= 1000
      print "Raw voltage: 0x%04X (%f uV)" % (raw, v)
    return raw

  def readDieTempC(self):
   Tdie = self.readRawDieTemperature()
   Tdie *= 0.03125 # convert to celsius
   if self.debug:
     print "Tdie = ", Tdie
   return Tdie

  def readObjTempC(self):
    Tdie = self.readRawDieTemperature()
    Vobj = self.readRawVoltage()
    Vobj *= 156.25  # 156.25 nV per LSB
    Vobj /= 1000    # nV -> uV
    Vobj /= 1000    # uV -> mV
    Vobj /= 1000    # mV -> V
    Tdie *= 0.03125 # convert to celsius
    Tdie += 273.15  # convert to kelvin

    if self.debug:
      print "Vobj = ", Vobj * 1000000, "uV"
      print "Tdie = ", Tdie, " C"
   
    tdie_tref = Tdie - self.__TMP006_TREF
    S = 1 + self.__TMP006_A1 * tdie_tref \
        + self.__TMP006_A2 * tdie_tref * tdie_tref
    S *= self.__TMP006_S0
    S /= 10000000
    S /= 10000000
   
    Vos = self.__TMP006_B0 + self.__TMP006_B1 * tdie_tref \
        + self.__TMP006_B2 * tdie_tref * tdie_tref
   
    fVobj = (Vobj - Vos) + self.__TMP006_C2 * (Vobj-Vos)*(Vobj-Vos)
    Tobj = sqrt(sqrt(Tdie * Tdie * Tdie * Tdie + fVobj/S))
   
    Tobj -= 273.15 # Kelvin -> *C
    return Tobj
