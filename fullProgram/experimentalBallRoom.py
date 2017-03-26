#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from constants import *
from calibration import *

#'''
motorL = ev3.LargeMotor('outD')
assert motorL.connected, "Error while connecting left LargeMotor"
motorR = ev3.LargeMotor('outA')
assert motorR.connected, "Error while connecting right LargeMotor"

servoL = ev3.MediumMotor('outC')
assert servoL.connected, "Error while connecting left servo"
servoR = ev3.MediumMotor('outB')
assert servoR.connected, "Error while connecting right servo"

# Connect color sensors
colSensorL = ev3.ColorSensor('in4')
assert colSensorL.connected, "Error while connecting left ColorSensor"
colSensorR = ev3.ColorSensor('in1')
assert colSensorR.connected, "Error while connecting right ColorSensor"
    
# Connect ultrasonic sensors
uSonic = ev3.UltrasonicSensor('in2')
assert uSonic.connected, "Error while connecting UltrasonicSensor"
sideSonic = ev3.UltrasonicSensor('in3')
assert sideSonic.connected, "Error while connecting Side UltrasonicSensor"

ev3.Sound.speak('Sensors connected!').wait()
#'''

def followSide():
    LI = colSensorL.reflected_light_intensity   # Set left brightness value
    RI = colSensorR.reflected_light_intensity   # Set right brightnes value
    distance = sideSonic.distance_centimeters
    
    prevSDiff = sDiff   # Save previous diff
    sDiff = distance - 10
    
    integral = integral + sDiff  # Set integral
    
    derivative = sDiff - prevSDiff    # Set derivative
    
    speed = (KP*sDiff + KI*integral + KD*derivative) * GAIN  # Set speed change
    
    motorL.run_forever(speed_sp = Limit_Speed(BASE_SPEED + speed))   # Set speed for left motor
    motorR.run_forever(speed_sp = Limit_Speed(BASE_SPEED - speed))   # Set speed for right motor

def nextCorner():
    motorL.run_forever(speed_sp = 180)
    motorR.run_forever(speed_sp = 180)
    
    while uSonic.distance_centimeters > 120:    # Go to next wall
        followSide()
    
    motorL.run_timed(time_sp = 1000, speed_sp = 210)   # Turn RIGHT
    motorR.run_timed(time_sp = 1000, speed_sp = -210)    # Turn RIGHT
    time.sleep(1)
    motorL.run_timed(time_sp = 3000, speed_sp = -200)   # Back up
    motorR.run_timed(time_sp = 3000, speed_sp = -200)   # Back up

def mapRoom():
    nextCorner()
    side1 = uSonic.distance_centimeters
    corner1 = (colSensorL.reflected_light_intensity + colSensorR.reflected_light_intensity) / 2
    
    nextCorner()
    side2 = uSonic.distance_centimeters
    corner2 = (colSensorL.reflected_light_intensity + colSensorR.reflected_light_intensity) / 2
    
    nextCorner()
    side3 = uSonic.distance_centimeters
    corner3 = (colSensorL.reflected_light_intensity + colSensorR.reflected_light_intensity) / 2
    
    if corner1 < corner2 and corner3:
        evac = 1
    elif corner2 < corner1 and corner3:
        evac = 2
    elif corner3 < corner1 and corner2:
        evac = 3
    
    side1 = (side1 + side3) / 2
    
    print("EVAC: " + evac)
    print("SIDE 1: " + side1)
    print("SIDE 2: " + side2)
'''
def goToCorner(corner):
    if corner == 2:
        
    elif corner == 3:
        
    elif corner == 4:
        '''



mapRoom()