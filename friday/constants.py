import ev3dev.ev3 as ev3



##### CONNECT SENSORS AND MOTORS ###############################################
    
def connect():# Connect Motors
    global motorL
    global motorR
    global servoL
    global servoR
    global colSensorL
    global colSensorR
    global uSonic

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
        
    # Connect ultrasonic sensor
    uSonic = ev3.UltrasonicSensor('in2')
    assert uSonic.connected, "Error while connecting UltrasonicSensor"
    
    ev3.Sound.speak('Sensors connected!').wait()

def motor(a):
    if a == 'LL':
        return motorL
    elif a == 'LR':
        return motorR
    elif a == 'SL':
        return servoL
    elif a == 'SR':
        return servoR
        
def sensor(a):
    if a == 'CL':
        return colSensorL
    if a == 'CR':
        return colSensorR
    if a == 'US':
        return uSonic

##### DEFINE CONSTANTS AND VARIABLES ###########################################

    # Constants
KP = 0.5    # Proportional constant
KI = 0.01   # Integral constant
KD = 0.005  # Derivative constant
GAIN = 10   # Gain for motorspeed
BASE_SPEED = 120  # Base speed
    
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

##### LIMIT SPEEDS #############################################################

def Limit_Speed(speed):
    # Limit speed for line following
    if speed > 800:
        speed = 800
    elif speed < -800:
        speed = -800
    return speed

def Limit_Speed_Slow(speed):
    # Limit speed for cornering
    if speed > 300:
        speed = 300
    elif speed < -300:
        speed = -300
    return speed
