#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from constants import *
from calibration import *
from lineFollowing import *
from ultraSonic import *
from ballRoom import *
import os
import time

os.system('constants.py')

##### CONNECTING SENSORS AND MOTORS ############################################

connect()

##### CALIBRATION ##############################################################

setMidpoint(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))       # Set midpoint

##### LINE FOLLOWING  ##########################################################

ev3.Sound.speak('Line!').wait()  # Announce start of line following

motorL = motor('LL')
motorR = motor('LR')
colSensorL = sensor('CL')
colSensorR = sensor('CR')
uSonic = sensor('US')
TICKS = 0

while True:
    try:
        #if uSonic.distance_centimeters < 25:
            #Obstacle(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'), sensor('US'))
        LI, RI, TICKS = Follow_Line(motorL, motorR, colSensorL, colSensorR, TICKS)
        print("Ticks: ", TICKS, "LI: ", LI, "RI: ", RI)
        
        if TICKS < 5:
            if LI < 20 or RI < 20:
                Check_Color(motorL, motorR, colSensorL, colSensorR)
            '''
            elif LI == 100 and RI == 100:
                motorL.stop(brake)
                motorR.stop(brake)
                time.sleep(0.5)
                if colSensorL.reflected_light_intensity == 100 and colSensorR.reflected_light_intensity == 100:
                    mapRoom(motorL, motorR, colSensorL, colSensorR, uSonic)
            '''
    except:
        motorR.stop(brake)
        motorL.stop(brake)
        ev3.Sound.speak('Error found!').wait()  # Announce error
