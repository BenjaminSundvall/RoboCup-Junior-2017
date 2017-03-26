#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
import time

SensorR = ev3.ColorSensor('in1')
SensorL = ev3.ColorSensor('in4')

colSensorL = ev3.ColorSensor('in4')
colSensorR = ev3.ColorSensor('in1')

# Constants
KP = 0.5    # Proportional constant
KI = 0.01   # Integral constant
KD = 0.005  # Derivative constant
GAIN = 10   # Gain for motorspeed
BASE_SPEED = 150  # Base speed

# PID variables
diff = 0    # Previous brightness diff
prevDiff = 0    # Previous diff value

integral = 0    # Memory
derivative = 0  # Guess

##### LIMIT SPEEDS #############################################################

def Limit_Speed(speed):
    # Limit speed for line following
    if speed > 900:
        speed = 900
    elif speed < -900:
        speed = -900
    return speed

def Limit_Speed_Slow(speed):
    # Limit speed for cornering
    if speed > 300:
        speed = 300
    elif speed < -300:
        speed = -300
    return speed

##### FOLLOW LINE ##############################################################

def Follow_Line():
    # Make variables global
    global diff
    global prevDiff
    global integral
    global derivative
    
    while == True:
        LI = colSensorL.reflected_light_intensity   # Set left brightness value
        RI = colSensorR.reflected_light_intensity   # Set right brightnes value
        
        if abs(LI - RI) < 5:                        #<<<<<<<<<<<<<<<<<<<<<<<<<<<
            RI = LI                                 #<<<<<<<<<<<<<<<<<<<<<<<<<<<
        
        prevDiff = diff # Save previous diff
        diff = LI - RI  # Set new diff
        
        integral = integral + diff  # Set integral
        
        derivative = diff - prevDiff    # Set derivative
        
        speed = (KP*diff + KI*integral + KD*derivative) * GAIN  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed(BASE_SPEED + speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed(BASE_SPEED - speed))   # Set speed for right motor