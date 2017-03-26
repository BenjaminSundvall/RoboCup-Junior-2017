''' GREEN DISABLED '''
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
KP = 0.4    # Proportional constant
KI = 0.01   # Integral constant
KD = 0.005  # Derivative constant
GAIN = 10   # Gain for motorspeed
BASE_SPEED = 400  # Base speed

# Initialize PID variables
diff = 0
prevDiff = 0
integral = 0

while True:
    prevDiff = diff
    diff = colSensorL.reflected_light_intensity - colSensorR.reflected_light_intensity
    
    integral = integral + diff
    derivative = diff - prevDiff
    
    speed = (KP*diff + KI*integral + KD*derivative) * GAIN
    
    motorL.run_forever(speed_sp = BASE_SPEED + speed)
    motorR.run_forever(speed_sp = BASE_SPEED - speed)



''' START OF NOTES

LEFT = POSITIVE
RIGHT = NEGATIVE

Byt display till tom:
    sudo chvt 6

Visa terminal på display:
    sudo conspy

Gå ut ur terminal på display:
    3x ESC

Byt display till Brickman:
    sudo chvt 1

END OF NOTES '''