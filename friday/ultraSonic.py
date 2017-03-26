#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from constants import *
from calibration import *

def Obstacle(motorL, motorR, colSensorL, colSensorR, uSonic):
    Found_Line = False
    time.sleep(0.5)
    if 50 > uSonic.distance_centimeters:
        while uSonic.distance_centimeters < 120:
            motorL.run_forever(speed_sp = -200)
            motorR.run_forever(speed_sp = -200)
        motorL.run_timed(time_sp = 1000, speed_sp = -200)
        motorR.run_timed(time_sp = 1000, speed_sp = 200)
        time.sleep(1)
        while Found_Line == False:
            motorL.run_forever(speed_sp = 207)
            motorR.run_forever(speed_sp = 92)
            if colSensorL.reflected_light_intensity < 10:
                Found_Line = True
                motorL.run_timed(time_sp = 100, speed_sp = -50)
                motorR.run_timed(time_sp = 100, speed_sp = -50)
                Finding_Line(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))

def Finding_Line(motorL, motorR, colSensorL, colSensorR):
    # Make variables global
    global value
    global prevValue
    global integralSingle
    global derivativeSingle
    
    for _ in range(50):
        prevValue = value # Save previous value
        value = midpointValue(2) - colSensorL.reflected_light_intensity  # Set new value
        
        integralSingle = integralSingle + value  # Set integral
        
        derivativeSingle = value - prevValue    # Set derivative
        
        speed = (KP*value*2 + KI*integralSingle + KD*derivativeSingle*2) * (GAIN)  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 - speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 + speed))   # Set speed for right motor