#!/usr/local/bin/python3
import ev3dev.ev3 as ev3

# Define Ports
motorL = ev3.LargeMotor('outD')
motorR = ev3.LargeMotor('outA')

colorSensL = ev3.ColorSensor('in4')
colorSensR = ev3.ColorSensor('in1')
extButton = ev3.Button('in2')

# whiteCal on touch
#--
whiteCalL = colorSensL.reflected_light_intensity
#--
whiteCalR = colorSensR.reflected_light_intensity

# Print whiteCal
print ('wCalL: ' + whiteCalL + ' wCalR: ' + whiteCalR)

# Set sensor mode to color
colorSensL.mode='COL-COLOR'
colorSensL.mode='COL-COLOR'

# Start
while True:
    # ------- Check color for both sensors
    