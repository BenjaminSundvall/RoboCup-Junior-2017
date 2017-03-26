#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from constants import *
from calibration import *
from lineFollowing import *
from ultraSonic import *
from ballRoom import *
import time

##### CONNECTING SENSORS AND MOTORS ############################################

connect()

##### CALIBRATION ##############################################################

setMidpoint(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))       # Set midpoint

##### LINE FOLLOWING  ##########################################################

Follow_Line(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))

ev3.Sound.speak('Line!').wait()  # Announce start of line following

motorL = motor('LL')
motorR = motor('LR')
colSensorL = sensor('CL')
colSensorR = sensor('CR')
uSonic = sensor('US')
uSonic2 = sensor('US2')

while True:
    try:
#        if uSonic.distance_centimeters < 25:
#            Obstacle(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'), sensor('US'))
        LI, RI = Follow_Line(motorL, motorR, colSensorL, colSensorR
        if LI < 25 or RI < 25:
            Check_Color(motorL, motorR, colSensorL, colSensorR)
        if LI == 100 and RI == 100:
            motorL.stop()
            motorR.stop()
            time.sleep(1)
            if colSensorL.reflected_light_intensity > 95 or colSensorR.reflected_light_intensity > 95:
                mapRoom(motorL, motorR, colSensorL, colSensorR, uSonic, uSonic2)
    except:
        motorR.stop()
        motorL.stop()
        ev3.Sound.speak('Error found!').wait()  # Announce error
