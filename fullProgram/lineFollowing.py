import ev3dev.ev3 as ev3
from constants import *
from calibration import *

##### FOLLOW LINE ##############################################################

def Follow_Line(motorL, motorR, colSensorL, colSensorR):
    # Make variables global
    global diff
    global prevDiff
    global integral
    global derivative
    global blackTicks
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
        
        if LI < (midpointValue(1) + 5) or RI < (midpointValue(1) + 5):  # Increase/decrease ticks
            blackTicks = min(blackTicks+1, 8)
            #print(blackTicks)
        else:
            blackTicks = max(blackTicks-1, 0)
        
        return(LI, RI)   # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

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
    motorL.run_forever(speed_sp = 200)
    motorR.run_forever(speed_sp = -200)
    time.sleep(1.5)
    if colSensorL.reflected_light_intensity < 20:
        motorL.run_forever(speed_sp = 0)    # Stop motors
        motorR.run_forever(speed_sp = 0)    # Stop motors

##### CHECK COLOR ##############################################################

# Define color checking function
def Check_Color(motorL, motorR, colSensorL, colSensorR):
    motorL.stop()
    motorR.stop()
    if colSensorL.color == 3 or colSensorR.color == 3:      # Check color
        LC = colSensorL.color   # Set left color value
        RC = colSensorR.color   # Set right color value
        
        if LC == 3 or RC == 3:                              # Double check color
            if LC == 3 and RC != 3:                         # Turn left
                ev3.Sound.speak('Left!')
                Turn_Left(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))
            
            elif LC != 3 and RC == 3:                       # Turn right
                ev3.Sound.speak('Right!')
                Turn_Right(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))
            
            elif LC == 3 and RC == 3:                       # Turn around
                ev3.Sound.speak('Turn!')
                Turn_Around(motor('LL'), motor('LR'), sensor('CL'), sensor('CR'))
    