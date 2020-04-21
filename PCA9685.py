import time
import pigpio
import math

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:
  """
   This class provides an interface to the I2C PCA9685 PWM chip.

   The chip provides 16 PWM channels.

   All channels use the same frequency which may be set in the
   range 24 to 1526 Hz.

   If used to drive servos the frequency should normally be set
   in the range 50 to 60 Hz.

   The duty cycle for each channel may be independently set
   between 0 and 100%.

   It is also possible to specify the desired pulse width in
   microseconds rather than the duty cycle.  This may be more
   convenient when the chip is used to drive servos.

   The chip has 12 bit resolution, i.e. there are 4096 steps
   between off and full on.
   """
  
  # Registers/etc.
  _MODE1         = 0x00
  _MODE2         = 0x01
  _SUBADR1       = 0x02
  _SUBADR2       = 0x03
  _SUBADR3       = 0x04
  _PRESCALE      = 0xFE
  _LED0_ON_L     = 0x06
  _LED0_ON_H     = 0x07
  _LED0_OFF_L    = 0x08
  _LED0_OFF_H    = 0x09
  _ALL_LED_ON_L  = 0xFA
  _ALL_LED_ON_H  = 0xFB
  _ALL_LED_OFF_L = 0xFC
  _ALL_LED_OFF_H = 0xFD

  _RESTART = 1<<7
  _AI      = 1<<5
  _SLEEP   = 1<<4
  _ALLCALL = 1<<0

  _OCH    = 1<<3
  _OUTDRV = 1<<2


  def __init__(self, pi, bus=1, address=0x40, debug=False):
    self._pi = pi
    self._bus = bus
    self._address = address
    self._debug = debug

    self._h = pi.i2c_open(bus, address)

    self._write_reg(self._MODE1, self._AI | self._ALLCALL)
    self._write_reg(self._MODE2, self._OCH | self._OUTDRV)

    time.sleep(0.0005)

    mode = self._read_reg(self._MODE1)
    self._write_reg(self._MODE1, mode & ~self._SLEEP)

    time.sleep(0.0005)

    self.set_frequency(50)
    self.set_duty_cycle(-1, 0)    


  def _write_reg(self, reg, byte):
    "Writes an 8-bit value to the specified register/address"
    self._pi.i2c_write_byte_data(self._h, reg, byte)
    if (self._debug):
      print("I2C: Write 0x%02X to register 0x%02X" % (byte, reg))


  def _read_reg(self, reg):
    "Read an unsigned byte from the I2C device"
    result = self._pi.i2c_read_byte_data(self._h, reg)
    if (self._debug):
      print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
    return result
	

  def get_frequency(self):
    "Returns the PWM frequency."
    return self._frequency


  def set_frequency(self, frequency):
    "Sets the PWM frequency."
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(frequency)
    prescaleval -= 1.0
    # i.e. prescale = int(round(25000000.0 / (4096.0 * frequency)) - 1)
    if (self._debug):
      print("Setting PWM frequency to %d Hz" % frequency)
      print("Estimated pre-scale: %d" % prescaleval)
    
    prescale = math.floor(prescaleval + 0.5)
    if prescale < 3:
      prescale = 3
    elif prescale > 255:
      prescale = 255

    mode = self._read_reg(self._MODE1)
    self._write_reg(self._MODE1, (mode & ~self._SLEEP) | self._SLEEP)   # go to sleep
    self._write_reg(self._PRESCALE, prescale)
    self._write_reg(self._MODE1, mode)

    time.sleep(0.0005)

    self._write_reg(self._MODE1, mode | self._RESTART)

    self._frequency = (25000000.0 / 4096.0) / (prescale + 1)
    self._pulse_width = (1000000.0 / self._frequency)


  def set_duty_cycle(self, channel, percent):
    "Sets the duty cycle for a channel.  Use -1 for all channels."
    steps = int(round(percent * (4096.0 / 100.0)))

    # remnain in 12bit control window
    if steps < 0:
      on = 0
      off = 4096
    elif steps > 4095:
      on = 4096
      off = 0
    else:
      on = 0
      off = steps

    # PCA9685 has 16 channels
    if (channel >= 0) and (channel <= 15):
      self._pi.i2c_write_i2c_block_data(self._h, self._LED0_ON_L+4*channel, [on & 0xFF, on >> 8, off & 0xFF, off >> 8])
    else:
      self._pi.i2c_write_i2c_block_data(self._h, self._ALL_LED_ON_L, [on & 0xFF, on >> 8, off & 0xFF, off >> 8])
    if (self._debug):
      print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))


  def set_pulse_width(self, channel, width):
    "Sets the pulse width for a channel.  Use -1 for all channels."
    self.set_duty_cycle(channel, (float(width) / self._pulse_width) * 100.0)


  def cancel(self):
    "Switches all PWM channels off and releases resources."
    self.set_duty_cycle(-1, 0)
    self._pi.i2c_close(self._h)


# if called standalone, showcase servo movement
if __name__=='__main__':
  exit(0)
