#!/usr/bin/env python3
 
import pigpio
import PCA9685
import time

pi = pigpio.pi()

if not pi.connected:
  exit(0)
  
pwm = PCA9685.PCA9685(pi) # defaults to bus 1, address 0x40

pwm.set_frequency(50) # for servos

for dc in range(5, 11):
  pwm.set_duty_cycle(-1, dc)  # -1 for all channels
  time.sleep(1)
  
for pw in range(1000, 2050, 50):
  pwm.set_pulse_width(-1, pw)  # -1 for all channels
  time.sleep(1)
  
pwm.cancel()

pi.stop()
