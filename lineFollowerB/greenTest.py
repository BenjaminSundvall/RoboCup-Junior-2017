#!/usr/local/bin/python3
import ev3dev.ev3 as ev3

# Connect color sensors
colSensorL = ev3.ColorSensor('in4')
colSensorR = ev3.ColorSensor('in1')

def Check_Green():
    intensityL = colSensorL.reflected_light_intensity
    intensityR = colSensorR.reflected_light_intensity
    
    greenL = colSensorL.color
    greenR = colSensorR.color