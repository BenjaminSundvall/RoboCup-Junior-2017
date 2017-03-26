#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
import time

# Define Ports
motorL = ev3.LargeMotor('outD')
motorR = ev3.LargeMotor('outA')

cSL = ev3.ColorSensor('in4')
cSR = ev3.ColorSensor('in1')

# Define other variables
btn = ev3.Button()

direction = 1



# Calibrate White
print ("Calibrate White")
while True:
    if btn.enter == True:
        whiteCal = (cSL.reflected_light_intensity + cSR.reflected_light_intensity)/2  # Calculate average value
        print (whiteCal)
        break  # Exit loop and move on
    else:
        time.sleep(0.01)

time.sleep(1)   # Wait

# Calibrate Black
print ("Calibrate Black")
while True:
    if btn.enter == True:
        blackCal = (cSL.reflected_light_intensity + cSR.reflected_light_intensity)/2  # Calculate average value
        print (blackCal)
        break  # Exit loop and move on
    else:
        time.sleep(0.01)

time.sleep(1)   # Wait

# Calibrate Silver
print ("Calibrate Silver")
while True:
    if btn.enter == True:
        silverCal = (cSL.reflected_light_intensity + cSR.reflected_light_intensity)/2  # Calculate average value
        print (silverCal)
        break  # Exit loop and move on
    else:
        time.sleep(0.01)

time.sleep(1)   # Wait



# Define functions




# Run

while True:
    if cSL.reflected_light_intensity - 4 < cSR.reflected_light_intensity < cSL.reflected_light_intensity + 4:
        motorL.run_timed(time_sp = 30, speed_sp = 300)
        motorR.run_timed(time_sp = 30, speed_sp = 300)

    elif cSL.reflected_light_intensity > blackCal + 5:
        motorL.run_timed(time_sp = 30, speed_sp = 100)
        motorR.run_timed(time_sp = 30, speed_sp = 300)

    elif cSR.reflected_light_intensity > blackCal + 5:
        motorL.run_timed(time_sp = 30, speed_sp = 300)
        motorR.run_timed(time_sp = 30, speed_sp = 100)


# Länk till PID tutorial:
# http://robotshop.com/letsmakerobots/pid-tutorials-line-following