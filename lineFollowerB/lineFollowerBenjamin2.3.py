#!/usr/local/bin/python3
import ev3dev.ev3 as ev3    # Import EV3 library
import time                 # Import time library

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
BASE_SPEED = 200  # Base speed

# Midpoint
ev3.Sound.speak('Black!').wait()
midPointL = colSensorL.reflected_light_intensity
midPointR = colSensorR.reflected_light_intensity

motorL.run_timed(time_sp = 500, speed_sp = 300)
motorR.run_timed(time_sp = 500, speed_sp = 300)

ev3.Sound.speak('White!').wait()
midPointL = midPointL + (midPointL + colSensorL.reflected_light_intensity) / 2
midPointR = midPointR + (midPointR + colSensorR.reflected_light_intensity) / 2

# PID variables
diff = 0    # Previous brightness diff
prevDiff = 0    # Previous diff value

value = 0   # Value of reflected light
prevValue = 0   # Previous brightness value

integral = 0    # Memory
derivative = 0  # Guess

# Other variables
colHistory = 0

turning = True

##### LIMIT SPEEDS #############################################################

def Limit_Speed(speed):
    # Limit speed in range [-900,900] for line following
    if speed > 900:
        speed = 900
    elif speed < -900:
        speed = -900
    return speed

def Limit_Speed_Slow(speed):
    # Limit speed in range [-500,500] for cornering
    if speed > 500:
        speed = 500
    elif speed < -500:
        speed = -500
    return speed

##### FOLLOW LINE ##############################################################

def Follow_Line():
    # Make variables global
    global diff
    global prevDiff
    global integral
    global derivative
    
    prevDiff = diff # Save previous diff
    diff = colSensorL.reflected_light_intensity - colSensorR.reflected_light_intensity  # Set new diff
    
    integral = integral + diff  # Set integral
    
    derivative = diff - prevDiff    # Set derivative
    
    speed = (KP*diff + KI*integral + KD*derivative) * GAIN  # Set speed change
    
    motorL.run_forever(speed_sp = Limit_Speed(BASE_SPEED + speed))   # Set speed for left motor
    motorR.run_forever(speed_sp = Limit_Speed(BASE_SPEED - speed))   # Set speed for right motor

##### TURN LEFT ################################################################

def Turn_Left():
    # Make variables global
    global value
    global prevValue
    global integral
    global derivative
    
    prevValue = value # Save previous value
    value = midPointL - colSensorL.reflected_light_intensity  # Set new value
    
    integral = integral + value  # Set integral
    
    derivative = value - prevValue    # Set derivative
    
    speed = (KP*value + KI*integral + KD*derivative*1.1) * (GAIN / 2)  # Set speed change
    
    motorL.run_forever(speed_sp = Limit_Speed_Slow((BASE_SPEED - speed) / 3))   # Set speed for left motor
    motorR.run_forever(speed_sp = Limit_Speed_Slow((BASE_SPEED + speed) / 3))   # Set speed for right motor

##### TURN RIGHT ###############################################################

def Turn_Right():
    # Make variables global
    global value
    global prevValue
    global integral
    global derivative
    
    prevValue = value # Save previous value
    value = midPointR - colSensorR.reflected_light_intensity  # Set new value
    
    integral = integral + value  # Set integral
    
    derivative = value - prevValue    # Set derivative
    
    speed = (KP*value + KI*integral + KD*derivative*1.1) * (GAIN / 2)  # Set speed change
    
    motorL.run_forever(speed_sp = Limit_Speed_Slow((BASE_SPEED + speed) / 3))   # Set speed for left motor
    motorR.run_forever(speed_sp = Limit_Speed_Slow((BASE_SPEED - speed) / 3))   # Set speed for right motor

##### TURN AROUND ##############################################################

def Turn_Around():
    if colSensorL.reflected_light_intensity < 20:
        motorL.run_forever(speed_sp = 0)    # Stop motors
        motorR.run_forever(speed_sp = 0)    # Stop motors
        turning = False

##### CHECK COLOR ##############################################################

# Define color checking function
def Check_Color():
    global colHistory
    if colSensorL.color == 1 or colSensorR.color == 1:      # Color history
        colHistory = 0
    else:
        colHistory = colHistory + 1
    
    if colSensorL.color == 3 or colSensorR.color == 3:      # Check color
        LC = colSensorL.color   # Set left color value
        RC = colSensorR.color   # Set right color value
        if LC == 3 or RC == 3 and colHistory < 5:          # Double check color
            motorL.run_forever(speed_sp = 0)    # Stop motors
            motorR.run_forever(speed_sp = 0)    # Stop motors
            
            if LC == 3 and RC != 3:                         # Turn left
                ev3.Sound.speak('Left!')
                for _ in range(50):
                    Turn_Left()
            
            elif LC != 3 and RC == 3:                       # Turn right
                ev3.Sound.speak('Right!')
                for _ in range(50):
                    Turn_Right()
            
            elif LC == 3 and RC == 3:                       # Turn around
                ev3.Sound.speak('Turn!')
                motorL.run_forever(speed_sp = 300)
                motorR.run_forever(speed_sp = -300)
                time.sleep(1)
                while turning == True:
                    Turn_Around()

##### RUN PROGRAM ##############################################################
cameraIsGreen = False
ev3.Sound.speak('Run!').wait()

while True:
    for _ in range(3):
        Follow_Line()
        Check_Color()