#!/usr/local/bin/python3
import ev3dev.ev3 as ev3
from multiprocessing import Process
import time

mRight = ev3.LargeMotor('outA')
mLeft = ev3.LargeMotor('outD')

sRight = ev3.ColorSensor('in1')
sLeft = ev3.ColorSensor('in4')
Gyro = ev3.GyroSensor('in3') 

lightRight = 0
lightLeft = 0

difference = 0

Green = 3

#Checking the color on both the sensors
def colorCheck():
    global rGreenCheck
    global lGreenCheck
    rGreenCheck = sRight.color
    lGreenCheck = sLeft.color

colorCheck()
#Turn right program
def turnRight():
    mRight.run_forever(speed_sp = 250 - abs(difference) * 7.5 )
    mLeft.run_forever(speed_sp = 250)

#Turn left program
def turnLeft():
    mRight.run_forever(speed_sp = 250)
    mLeft.run_forever(speed_sp = 250 - abs(difference) * 7.5)

#Go forward program
def turnForward():
    mRight.run_forever(speed_sp = 300)
    mLeft.run_forever(tspeed_sp = 300)

#Checking the lightintenity on both the sensors
def lightIntensity():
    global lightRight
    global lightLeft
    lightRight = sRight.reflected_light_intensity
    lightLeft = sLeft.reflected_light_intensity
    
#Checking the difference between the two light intensities
def lineCalculation(a, b):
    global difference
    difference = a-b
    
    if difference < 0:
        turnRight()
    elif difference > 0:
        turnLeft()
    else:
        turnForward()
        
#Program that runs if the sensors sense green
def greenProgram():
    def mRightProgram():
        mRight.run_timed(time_sp = 500 ,speed_sp = 200)
            
    def mLeftProgram():
        mLeft.run_timed(time_sp = 500, speed_sp = 200)
                
    pRight = Process(target = mRightProgram)
    pLeft = Process(target = mLeftProgram)
        
    if rGreenCheck == Green:
        global rGreenCheck
        while rGreenCheck == Green:
            mRight.run_timed(time_sp = 50, speed_sp = 200)
            mLeft.run_timed(time_sp = 50, speed_sp = 200)
            rGreenCheck
            
        pRight.start()
        pLeft.start()
        pRight.join()
        pLeft.join()
            
        gyroValue = Gyro.degrees
        while Gyro.degrees < (gyroValue + 90):
            mRight.run_timed(time_sp = 50, speed_sp = -150)
            mLeft.run_timed(time_sp = 50, speed_sp = 150)
            Gyro.degrees
        
        global rGreenCheck        
        while rGreenCheck == Green:
            mRight.run_timed(time_sp = 50, speed_sp = 200)
            mLeft.run_timed(time_sp = 50, speed_sp = 200)
            rGreenCheck
                    
    elif lGreenCheck == Green:
        global lGreenCheck
        while lGreenCheck == Green:
            mRight.run_timed(time_sp = 50, speed_sp = 200)
            mLeft.run_timed(time_sp = 50, speed_sp = 200)
            lGreenCheck
                
        pRight.start()
        pLeft.start()
        pRight.join()
        pLeft.join()
                
        gyroValue = Gyro.degrees
        while Gyro.degrees > (gyroValue - 90):
            mRight.run_timed(time_sp = 50, speed_sp = 150)
            mLeft.run_timed(time_sp = 50, speed_sp = -150)
            Gyro.degrees
        
        global lGreenCheck
        while lGreenCheck == Green:
            mRight.run_timed(time_sp = 50, speed_sp = 200)
            mLeft.run_timed(time_sp = 50, speed_sp = 200)
            lGreenCheck
                        
    else: 
        lineFollowingLoop()

#Sensor difference program
def lineFollowingLoop():
    for x in range(0, 15):
        if x == 14:
            colorCheck()
            if rGreenCheck == Green or lGreenCheck == Green:
                print("Green")
                greenProgram()
                
            else:
                lineFollowingLoop()
        
        else:
            lightIntensity()
            
            lineCalculation(lightRight, lightLeft)
            

lineFollowingLoop()
