#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from constants import *
from calibration import *
import time

def mapRoom(motorL, motorR, colSensorL, colSensorR, uSonic, uSonic2):
    global evac
    global x
    global y
    cycles = 0
    closeToWall = False
    turnNumber = 0
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
                            catchBalls(motorL, motorR, colSensorL, colSensorR, uSonic, uSonic2)
        
    
            
            
            
            '''
            while closeToWall == False:
                motorL.run_forever(speed_sp = 180)
                motorR.run_forever(speed_sp = 180)
                if uSonic.distance_centimeters < 120
            '''
                           
def catchBalls(motorL, motorR, colSensorL, colSensorR, uSonic, uSonic2):
    if evac == 2:
        
        ballGathering(motorL, motorR, colSensorL, colSenosrR, uSonic, uSonic2, right)

    
    elif evac == 3:
        motorL.run_forever(speed_sp = 180)
        motorR.run_forever(speed_sp = 180)
        while closeToWall == False:    
            if uSonic.distance_centimeters < 120:
                closeToWall = True
                motorL.stop()
                motorR.stop()            
        motorL.run_timed(timep_sp = 1000, speed_sp = -420)
        motorR.run_timed(timep_sp = 1000, speed_sp = 420)
        
        motorL.run_forever(speed_sp = 180)
        motorR.run_forever(speed_sp = 180)
        
        motorL.run_timed(time_sp, 1000 speed_sp = 420)
        motorR.run_timed(time_sp, 1000 speed_sp = -420)
        
        ballGathering(motorL, motorR, colSensorL, colSenosrR, uSonic, uSonic2, left)
        
    elif evac == 4:
        
        motorL.run_forever(speed_sp = 180)
        motorR.run_forever(speed_sp = 180)
        if (uSonic.distance_centimeters < 120):
            motorL.run_timed(time_sp = 1000, speed_sp = -210)
            motorR.run_timed(time_sp = 1000, speed_sp = 210)

        motorL.run_forever(speed_sp = 180)
        motorR.run_forever(speed_sp = 180)
        if (uSonic.distance_centimeters < 120):
            motorL.run_timed(time_sp = 1000, speed_sp = -210)
            motorR.run_timed(time_sp = 1000, speed_sp = 210)

        ballGathering(motorL, motorR, colSensorL, colSenosrR, uSonic, uSonic2, right)


def gatherBalls(motorL, motorR, colSensorL, colSensorR, uSonic, uSonic2, direction):

    while cycles < 11:
    
        if direction == left:
            motorL.run_forever(speed_sp = 180)
            motorR.run_forever(speed_sp = 180)
            if (uSonic.distance_centimeters < 120):
                motorL.run_timed(time_sp = 1000, speed_sp = -210)
                motorR.run_timed(time_sp = 1000, speed_sp = 210)
            motorL.run_forever(speed_sp = 180) 
            motorR.run_forever(speed_sp = 180)
            if colSensorL.reflected_light_intensity < midpointValue(1) + 5 or colSensorR.reflected_light_intensity < midpointValue(1) + 5:
                motorL.run_timed(time_sp = 200, speed_sp = 200)
                motorL.run_timed(time_sp = 200, speed_sp = 200)
            while uSonic.distance_centimeter < (x*(1-(cycles*0.1))):
        
            cycles = cycles + 1
        
            motorL.run_timed(time_sp = 1000, speed_sp = 210)
            motorR.run_timed(time_sp = 1000, speed_sp =-210)
        
            motorL.run_timed(time_sp = 5000, speed_sp = 180)
            motorR.run_timed(time_sp = 5000, speed_sp = 180)



    if direction == right:
        
        while cycles < 11:
    
        if direction == left:
            motorL.run_forever(speed_sp = 180)
            motorR.run_forever(speed_sp = 180)
            if (uSonic.distance_centimeters < 120):
                motorL.run_timed(time_sp = 1000, speed_sp = 210)
                motorR.run_timed(time_sp = 1000, speed_sp = -210)
            motorL.run_forever(speed_sp = 180) 
            motorR.run_forever(speed_sp = 180)
            if colSensorL.reflected_light_intensity < midpointValue(1) + 5 or colSensorR.reflected_light_intensity < midpointValue(1) + 5:
                motorL.run_timed(time_sp = 200, speed_sp = 200)
                motorL.run_timed(time_sp = 200, speed_sp = 200)
            while uSonic.distance_centimeter < (x*(1-(cycles*0.1))):
        
            cycles = cycles + 1
        
            motorL.run_timed(time_sp = 1000, speed_sp = -210)
            motorR.run_timed(time_sp = 1000, speed_sp = 210)
        
            motorL.run_timed(time_sp = 5000, speed_sp = 180)
            motorR.run_timed(time_sp = 5000, speed_sp = 180)

connect()
setMidpoint(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))
mapRoom(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'), sensor('US'))