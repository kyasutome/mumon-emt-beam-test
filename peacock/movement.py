import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time
    
def move_cycle(ser, ith):
    accelerator = "C8" #fixed
    waytotravel = "1" #fixed
    posid = "0A" #fixed
    datadir = "/Users/kenji/Documents/mumon-git/mumon-emt-beam-test-automation/actuator/peacock/data"
    path_to_posdata = datadir + "/position.txt"
    path_to_veldata = datadir + "/velocity.txt"

    with open(path_to_posdata) as f:
        posdata = f.read().split()
        print(posdata)
    with open(path_to_veldata) as g:
        veldata = g.read().split()
        print(veldata)

    #for i in range(10):
    command = '0MV'
    for j in range(4):
        id = 4*ith + j
        position = int(posdata[id])
        velocity = int(veldata[id])
        print(position, velocity)
        posconvert = str( format(int(mm_to_pulse(position)), '05x') )
        velconvert = str( format(int(mmpersec_to_pulse(velocity)), '03x'))
        command += velconvert + accelerator + waytotravel + posconvert
    print(command)
    command += '0\x0D\x0A'
    ser.write(command.encode())
    time.sleep(1)
    ser.flush()
    response = ser.readline()
    print(response)
    time.sleep(10)

def mm_to_pulse(position):

    pulse = position / 0.005
    return int(pulse)

def mmpersec_to_pulse(velocity):
    pulse = velocity
    return int(pulse)
    
def move_once(ser):
    testmovecommand = "test"
    print(testmovecommand)
