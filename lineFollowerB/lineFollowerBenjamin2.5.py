#!/usr/local/bin/python3
import ev3dev.ev3 as ev3    # Import EV3 library
import time                 # Import time library
import math                 # Import math library

# Connect Motors
motorL = ev3.LargeMotor('outD')
assert motorL.connected, "Error while connecting left LargeMotor"
motorR = ev3.LargeMotor('outA')
assert motorR.connected, "Error while connecting right LargeMotor"

# Connect color sensors
colSensorL = ev3.ColorSensor('in4')
assert colSensorL.connected, "Error while connecting left ColorSensor"
colSensorR = ev3.ColorSensor('in1')
assert colSensorR.connected, "Error while connecting right ColorSensor"

ev3.Sound.speak('Sensors connected!').wait()

##### DEFINE CONSTANTS AND VARIABLES ###########################################

# Constants
KP = 0.5    # Proportional constant
KI = 0.01   # Integral constant
KD = 0.005  # Derivative constant
GAIN = 10   # Gain for motorspeed
BASE_SPEED = 150  # Base speed

# Midpoint
ev3.Sound.speak('Black!').wait()
midPointL = colSensorL.reflected_light_intensity
midPointR = colSensorR.reflected_light_intensity

blackCal = (midPointL + midPointR) / 2

motorL.run_timed(time_sp = 500, speed_sp = 300)
motorR.run_timed(time_sp = 500, speed_sp = 300)

ev3.Sound.speak('White!').wait()
midPointL = midPointL + (midPointL + colSensorL.reflected_light_intensity) / 2
midPointR = midPointR + (midPointR + colSensorR.reflected_light_intensity) / 2

# PID variables
diff = 0    # Previous brightness diff
prevDiff = 0    # Previous diff value

integral = 0    # Memory
derivative = 0  # Guess

value = 0   # Value of reflected light
prevValue = 0   # Previous brightness value

integralSingle = 0    # Memory
derivativeSingle = 0  # Guess

blackTicks = 0

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
    global blackTicks
    
    for _ in range(4):
        LI = colSensorL.reflected_light_intensity   # Set left brightness value
        RI = colSensorR.reflected_light_intensity   # Set right brightnes value
        
        prevDiff = diff # Save previous diff
        diff = LI - RI  # Set new diff
        
        integral = integral + diff  # Set integral
        
        derivative = diff - prevDiff    # Set derivative
        
        speed = (KP*diff + KI*integral + KD*derivative) * GAIN  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed(BASE_SPEED + speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed(BASE_SPEED - speed))   # Set speed for right motor
        
        if LI < (blackCal + 5) or RI < (blackCal + 5):  # Increase/decrease ticks
            blackTicks = min(blackTicks+1, 8)
            print(blackTicks)
        else:
            blackTicks = max(blackTicks-1, 0)

##### TURN LEFT ################################################################

def Turn_Left():
    # Make variables global
    global value
    global prevValue
    global integralSingle
    global derivativeSingle
    
    for _ in range(50):
        prevValue = value # Save previous value
        value = midPointL - colSensorL.reflected_light_intensity  # Set new value
        
        integralSingle = integralSingle + value  # Set integral
        
        derivativeSingle = value - prevValue    # Set derivative
        
        speed = (KP*value + KI*integralSingle + KD*derivativeSingle) * (GAIN / 2)  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 - speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 + speed))   # Set speed for right motor

##### TURN RIGHT ###############################################################

def Turn_Right():
    # Make variables global
    global value
    global prevValue
    global integralSingle
    global derivativeSingle
    
    for _ in range(50):
        prevValue = value # Save previous value
        value = midPointR - colSensorR.reflected_light_intensity  # Set new value
        
        integralSingle = integralSingle + value  # Set integral
        
        derivativeSingle = value - prevValue    # Set derivative
        
        speed = (KP*value + KI*integralSingle + KD*derivativeSingle) * (GAIN / 2)  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 + speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 - speed))   # Set speed for right motor

##### TURN AROUND ##############################################################

def Turn_Around():
    motorL.run_forever(speed_sp = 200)
    motorR.run_forever(speed_sp = -200)
    time.wait(1.5)
    if colSensorL.reflected_light_intensity < 20:
        motorL.run_forever(speed_sp = 0)    # Stop motors
        motorR.run_forever(speed_sp = 0)    # Stop motors

##### CHECK COLOR ##############################################################

# Define color checking function
def Check_Color():
    if (colSensorL.color == 3 or colSensorR.color == 3) and blackTicks < 5:      # Check color
        LC = colSensorL.color   # Set left color value
        RC = colSensorR.color   # Set right color value
        
        if LC == 3 or RC == 3:                              # Double check color
            if LC == 3 and RC != 3:                         # Turn left
                ev3.Sound.speak('Left!')
                Turn_Left()
            
            elif LC != 3 and RC == 3:                       # Turn right
                ev3.Sound.speak('Right!')
                Turn_Right()
            
            elif LC == 3 and RC == 3:                       # Turn around
                ev3.Sound.speak('Turn!')
                Turn_Around()

##### RUN PROGRAM ##############################################################

ev3.Sound.speak('Run!').wait()

while True:
    Follow_Line()
    Check_Color()