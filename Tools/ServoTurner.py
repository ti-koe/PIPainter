#!/usr/bin/env python3


# This example moves a servo its full range (180 degrees by default) and then back.

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 50

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2480)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
servo0 = servo.Servo(pca.channels[0], min_pulse=600, max_pulse=2400)
servo3 = servo.Servo(pca.channels[3], min_pulse=600, max_pulse=2400)
servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2400)
servo11 = servo.Servo(pca.channels[11], min_pulse=600, max_pulse=2400)
servo12 = servo.Servo(pca.channels[12], min_pulse=600, max_pulse=2400)
servo15 = servo.Servo(pca.channels[15], min_pulse=600, max_pulse=2400)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2600)

# The pulse range is 1000 - 2000 by default.
#servo7 = servo.Servo(pca.channels[7])

for i in range(180):
    servo0.angle = i
    servo3.angle = i
    servo7.angle = i
    servo11.angle = i
    servo12.angle = i
    servo15.angle = i
for i in range(180):
    servo0.angle = 180 - i
    servo3.angle = 180 - i
    servo7.angle = 180 - i
    servo11.angle = 180 - i
    servo12.angle = 180 - i
    servo15.angle = 180 - i
pca.deinit()