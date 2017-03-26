#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from constants import *
from calibration import *
import time

def mapRoom(motorL, motorR, colSensorL, colSensorR, uSonic):
    global evac
    global x
    global y
    x1_check = False
    y_check = False
    x2_check = False
    motorL.run_forever(speed_sp = 180)
    motorR.run_forever(speed_sp = 180)
    while x1_check == False:    
        if uSonic.distance_centimeters < 120:
            x1_check = True
            motorL.stop()
            motorR.stop()
            
            currentCorner = 2
            
            if colSensorL.reflected_light_intensity < midpointValue(1) + 5 or colSensorR.reflected_light_intensity < midpointValue(1) + 5:
                evac = currentCorner
            
            motorL.run_timed(time_sp = 1000, speed_sp = -210)
            motorR.run_timed(time_sp = 1000, speed_sp = 210)
            time.sleep(1)
            
            motorL.run_timed(time_sp = 3000, speed_sp = -200)
            motorR.run_timed(time_sp = 3000, speed_sp = -200)
            
            time.sleep(3)
            
            x1 = uSonic.distance_centimeters
            
            motorL.run_forever(speed_sp = 180)
            motorR.run_forever(speed_sp = 180)
            while y_check == False:
                if uSonic.distance_centimeters < 120:
                    y_check = True
                    motorL.stop()
                    motorR.stop()
                    
                    currentCorner = 3
                    
                    if colSensorL.reflected_light_intensity < midpointValue(1) + 5 or colSensorR.reflected_light_intensity < midpointValue(1) + 5:
                        evac = currentCorner
                        
                    motorL.run_timed(time_sp = 1000, speed_sp = -210)
                    motorR.run_timed(time_sp = 1000, speed_sp = 210)
                    time.sleep(1)
                    
                    motorL.run_timed(time_sp = 3000, speed_sp = -200)
                    motorR.run_timed(time_sp = 3000, speed_sp = -200)
                    
                    time.sleep(3)
                    
                    y = uSonic.distance_centimeters
                    
                    motorL.run_forever(speed_sp = 180)
                    motorR.run_forever(speed_sp = 180)
                    while x2_check == False:
                        if uSonic.distance_centimeters < 120:
                            x2_check = True
                            motorL.stop()
                            motorR.stop()
                            
                            currentCorner = 4
                            
                            if colSensorL.reflected_light_intensity < midpointValue(1) + 5 or colSensorR.reflected_light_intensity < midpointValue(1) + 5:
                                evac = currentCorner
                            
                            motorL.run_timed(time_sp = 1000, speed_sp = -210)
                            motorR.run_timed(time_sp = 1000, speed_sp = 210)
                            time.sleep(1)
                            
                            motorL.run_timed(time_sp = 3000, speed_sp = -200)
                            motorR.run_timed(time_sp = 3000, speed_sp = -200)
                            
                            time.sleep(3)
                            
                            x2 = uSonic.distance_centimeters
                            
                            x = (x1 + x2)/2
                            catchBalls()
                            
def catchBalls():
    print(evac)
    print(x)
    print(y)

'''
connect()
setMidpoint(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))
mapRoom(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'), sensor('US'))
'''