#!/usr/local/bin/python3    #
import ev3dev.ev3 as ev3    #

motorL = ev3.LargeMotor('outB') #
motorR = ev3.LargeMotor('outA') #

colSensorL = ev3.ColorSensor('in4') #
colSensorR = ev3.ColorSensor('in1') #

uSonic = ev3.UltrasonicSensor('in2')    #

def currentCorner
def currentLap

################################################################################
if currentLap < 4 #As long as it has made 3 laps or less continue

    currentCorner = 1 #Four corners are one lap
    if currentCorner = 5 #Four corners are one lap
        currentCorner = 1 #Four corners are one lap
        currentLap = currentLap ++ #Four corners are one lap
    if currentCorner <= 4
        if (uSonic.distance_centimeters > (100*currentLap)) #If not close to wall
            if (colSensorR.reflected_light_intensity <= (blackCal + 10) or colSensorL.reflected_light_intensity <= (blackCal + 10)) #If sees black
                motorR.run_timed(time_sp = 500, speed_sp = -180) #Turn right
                motorL.run_timed(time_sp = 500, speed_sp = 180) #Turn left  
                if (uSonic.distance_centimeters <= 100) #If close to wall
                    motorR.run_timed(time_sp = 500, speed_sp = 360) #Turn left
                    motorL.run_timed(time_sp = 500, speed_sp = -360) #Turn left
            currentCorner = (currentCorner ++)


        else #If close to wall
            motorR.run_timed(time_sp = 500, speed_sp = -180) #Turn right
            motorL.run_timed(time_sp = 500, speed_sp = 180) #Turn left
            if (uSonic.distance_centimeters <= (100*currentLap)) #If close to wall
                motorR.run_timed(time_sp = 500, speed_sp = 360) #Turn left
                motorL.run_timed(time_sp = 500, speed_sp = -360) #Turn left
            currentCorner = (currentCorner ++)

'''
Turn code
motorR.run_timed(time_sp = 500, speed_sp = -180)
motorL.run_timed(time_sp = 500, speed_sp = 180)
if (uSonic.distance_centimeters <= 100)
    motorR.run_timed(time_sp = 500, speed_sp = 360)
    motorL.run_timed(time_sp = 500, speed_sp = -360)
'''







'''
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html
'''



    



















































































