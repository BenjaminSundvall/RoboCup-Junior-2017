#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
import time

'''
01 CONSTANTS
02 MIDPOINT CALIBRATION
03 LINE FOLLOWING
04 ULTRASONIC
05 BALL ROOM
06 RUN PROGRAM
'''

'''
################################################################################
#####01 CONSTANTS ##############################################################
################################################################################
'''

##### CONNECT SENSORS AND MOTORS ###############################################

# Connect Motors
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

ev3.Sound.speak('Sensors connected!').wait()    # Announce sensors connected

##### DEFINE CONSTANTS AND VARIABLES ###########################################

# PID Constants
KP = 0.5    # Proportional constant
KI = 0.01   # Integral constant
KD = 0.005  # Derivative constant
GAIN = 10   # Gain for motorspeed
BASE_SPEED = 150  # Base speed

SILVER = 95 # Reflect value on silver

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

def Limit_Speed_Slow(speed):
    # Limit speed for cornering
    if speed > 300:
        speed = 300
    elif speed < -300:
        speed = -300

'''
################################################################################
#####02 MIDPOINT CALIBRATION ###################################################
################################################################################
'''
##### DEFINE MIDPOINT ##########################################################

#ev3.Sound.speak('Black!').wait()
blackL = colSensorL.reflected_light_intensity
blackR = colSensorR.reflected_light_intensity

blackCal = (blackL + blackR) / 2

motorL.run_timed(time_sp = 500, speed_sp = 300)
motorR.run_timed(time_sp = 500, speed_sp = 300)

#ev3.Sound.speak('White!').wait()
midPointL = (blackL + colSensorL.reflected_light_intensity) / 2
midPointR = (blackR + colSensorR.reflected_light_intensity) / 2

'''
################################################################################
#####03 LINE FOLLOWING #########################################################
################################################################################
'''

##### FOLLOW LINE ##############################################################

def Follow_Line():
    # Make variables global
    global diff
    global prevDiff
    global integral
    global derivative
    global blackTicks
    global LI
    global RI
    
    for _ in range(1):
        LI = colSensorL.reflected_light_intensity   # Set left brightness value
        RI = colSensorR.reflected_light_intensity   # Set right brightnes value
        
        if abs(LI - RI) < 5:    # Round intensities
            RI = LI
        
        prevDiff = diff # Save previous diff
        diff = LI - RI  # Set new diff
        
        integral = integral + diff  # Set integral
        
        derivative = diff - prevDiff    # Set derivative
        
        speed = (KP*diff + KI*integral + KD*derivative) * GAIN  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed(BASE_SPEED + speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed(BASE_SPEED - speed))   # Set speed for right motor
        
        if LI < (blackCal + 5) or RI < (blackCal + 5):  # Increase/decrease ticks
            blackTicks = min(blackTicks+1, 8)
            #print(blackTicks)
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
        value = midpointValue(2) - colSensorL.reflected_light_intensity  # Set new value
        
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
        value = midpointValue(3) - colSensorR.reflected_light_intensity  # Set new value
        
        integralSingle = integralSingle + value  # Set integral
        
        derivativeSingle = value - prevValue    # Set derivative
        
        speed = (KP*value + KI*integralSingle + KD*derivativeSingle) * (GAIN / 2)  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 + speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 - speed))   # Set speed for right motor

##### TURN AROUND ##############################################################

def Turn_Around():
    motorL.run_forever(speed_sp = 200)
    motorR.run_forever(speed_sp = -200)
    time.sleep(1.5)
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

'''
################################################################################
#####04 ULTRASONIC #############################################################
################################################################################
'''

def Obstacle():
    Found_Line = False
    time.sleep(0.5)
    if 120 > uSonic.distance_centimeters:
        motorR.run_timed(time_sp = 1000, speed_sp = 200)
        motorL.run_timed(time_sp = 1000, speed_sp = -200)
        time.sleep(1)
        while Found_Line == False:
            motorR.run_forever(speed_sp = 92)
            motorL.run_forever(speed_sp = 207)
            if colSensorL.reflected_light_intensity < 10:
                Found_Line = True
                motorR.run_timed(time_sp = 100, speed_sp = -50)
                motorL.run_timed(time_sp = 100, speed_sp = -50)
                Finding_Line()

def Finding_Line():
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
        
        speed = (KP*value*2 + KI*integralSingle + KD*derivativeSingle*2) * (GAIN)  # Set speed change
        
        motorL.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 - speed))   # Set speed for left motor
        motorR.run_forever(speed_sp = Limit_Speed_Slow(BASE_SPEED/2 + speed))   # Set speed for right motor

'''
################################################################################
#####05 BALL ROOM ##############################################################
################################################################################
'''



'''
################################################################################
#####06 RUN PROGRAM ############################################################
################################################################################
'''

while True:
    if uSonic.distance_centimeters < 120:
        Obstacle()
    Follow_Line()
    if LI > SILVER or RI > SILVER:
        ''' BALL ROOM '''
    if LI < 15 or RI < 15:
        Check_Color()