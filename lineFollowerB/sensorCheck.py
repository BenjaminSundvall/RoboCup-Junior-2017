#!/usr/local/bin/python3
import ev3dev.ev3 as ev3    # Import EV3 library
import time                 # Import time library

# Connect color sensors
colSensorL = ev3.ColorSensor('in4')
assert colSensorL.connected, "Error while connecting left ColorSensor"
colSensorR = ev3.ColorSensor('in1')
assert colSensorR.connected, "Error while connecting right ColorSensor"

ev3.Sound.speak('Sensors connected!').wait()

################################################################################

while True:
    print('L: ' + str(colSensorL.reflected_light_intensity) + ' R: ' + str(colSensorR.reflected_light_intensity))
    print('Left Green: ' + str(colSensorL.green) + ' Right Green: ' + str(colSensorR.green))
    print(' ')
    time.sleep(0.5)