#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from constants import *



def setMidpoint(motorL, motorR, colSensorL, colSensorR):
    global midPointL
    global midPointR
    global blackCal
    # Midpoint
    ev3.Sound.speak('Black!').wait()
    midPointL = colSensorL.reflected_light_intensity
    midPointR = colSensorR.reflected_light_intensity
    
    blackCal = (midPointL + midPointR) / 2
    
    motorL.run_timed(time_sp = 500, speed_sp = 300)
    motorR.run_timed(time_sp = 500, speed_sp = 300)
    
    ev3.Sound.speak('White!').wait()
    midPointL = (midPointL + colSensorL.reflected_light_intensity) / 2
    midPointR = (midPointR + colSensorR.reflected_light_intensity) / 2
    
def midpointValue(a):
    if a == 1:
        return blackCal
    elif a == 2:
        return midPointL
    elif a == 3:
        return midPointR