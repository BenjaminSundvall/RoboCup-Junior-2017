import ev3dev.ev3 as ev3
from constants import *
from calibration import *
import time

##### FOLLOW LINE ##############################################################

def Follow_Line(motorL, motorR, colSensorL, colSensorR, blackTicks):
    # Make variables global
    global diff
    global prevDiff
    global integral
    global derivative

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
        
    if LI < (midpointValue(1) + 5) or RI < (midpointValue(1) + 5):  # Increase/decrease ticks
        blackTicks = min(blackTicks+1, 8)
    else:
        blackTicks = max(blackTicks-1, 0)
    
    return(LI, RI, blackTicks)   # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

##### TURN LEFT ################################################################

def Turn_Left(motorL, motorR, colSensorL, colSensorR):
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

def Turn_Right(motorL, motorR, colSensorL, colSensorR):
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

def Turn_Around(motorL, motorR, colSensorL, colSensorR):
    found_line = False
    motorL.run_forever(speed_sp = 200)
    motorR.run_forever(speed_sp = -200)
    time.sleep(1.5)
    while found_line == False:
        if colSensorL.reflected_light_intensity < 20:
            found_line = True
            motorL.stop(brake)
            motorR.stop(brake)    # Stop motors

##### CHECK COLOR ##############################################################

# Define color checking function
def Check_Color(motorL, motorR, colSensorL, colSensorR):
    if (colSensorL.color == 3 or colSensorR.color == 3) and blackTicks < 5:      # Check color
        LC = colSensorL.color   # Set left color value
        RC = colSensorR.color   # Set right color value
        
        if LC == 3 or RC == 3:                              # Double check color
            if LC == 3 and RC != 3:                         # Turn left
                ev3.Sound.speak('Left!')
                Turn_Left(motorL, motorR, colSensorL, colSensorR)
            
            elif LC != 3 and RC == 3:                       # Turn right
                ev3.Sound.speak('Right!')
                Turn_Right(motor<l, motor<r, colSensorL, colSensorR)
            
            elif LC == 3 and RC == 3:                       # Turn around
                ev3.Sound.speak('Turn!')
                Turn_Around(motorL, motorR, colSensorL, colSensorR)
