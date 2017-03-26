''' GREEN ENABLED AND WORKING '''
#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
import time


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

'''
# Connect pixy cam and set mode
pixy = ev3.Sensor('in2')
assert pixy.connected, "Error while connecting Pixy camera"
pixy.mode = 'SIG1'
'''

# Constants
KP = 0.5    # Proportional constant
KI = 0.01   # Integral cons¤tant
KD = 0.005  # Derivative constant
GAIN = 10   # Gain for motorspeed
BASE_SPEED = 200  # Base speed

# PID variables
diff = 0    # Difference in brightness between sensors
prevDiff = 0    # Previous brightness difference
integral = 0    # Memory
derivative = 0  # Guess

'''
# Make PID variables global
global diff
global prevDiff
global integral
global derivative
'''

def Limit_Speed(speed):
    # Limit speed in range [-900,900]
    if speed > 900:
        speed = 900
    elif speed < -900:
        speed = -900
    return speed

# Define line following function
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

# Define color checking function
def Check_Color():
    if colSensorL.color == 3 or colSensorR.color == 3:
        if colSensorL.color == 3 or colSensorR.color == 3:
            motorL.run_forever(speed_sp = 0)
            motorR.run_forever(speed_sp = 0)
            ev3.Sound.speak('Found green!').wait()
            exit()

ev3.Sound.speak('Starting').wait()

# Run full loop
while True:
    for _ in range(8):
        Follow_Line()
    Check_Color()