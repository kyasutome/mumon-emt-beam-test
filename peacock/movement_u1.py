import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time
import numpy as np
    
def move_cycle(ser, ith):
    accelerator = '1' #fixed
    waytotravel = '1' #fixed
    posid = "0A" #fixed
    datadir = "/Users/kenji/Documents/mumon-git/mumon-emt-beam-test-hub/peacock/data"
    path_to_posdata = datadir + "/position_u1.txt"
    path_to_veldata = datadir + "/velocity_u1.txt"

    with open(path_to_posdata) as f:
        posdata = f.read().split()
        print(posdata)
    with open(path_to_veldata) as g:
        veldata = g.read().split()
        print(veldata)

    #for i in range(10):
    command = '0MV'
    id = ith
    position = int(posdata[1])
    velocity = int(veldata[1])

    print(position, velocity)
    posconvert = str( format(mm_to_pulse(position), '05x') )
    velconvert = str( format(mmpersec_to_pulse(velocity), '04x'))
    command += velconvert + accelerator + waytotravel + posconvert
    command += '\x0D\x0A'
    print(command)
    ser.write(command.encode())
    time.sleep(1)
    ser.flush()
    response = ser.readline()
    print(response)
    time.sleep(1)

def mm_to_pulse(position):
    pulse = position / 0.005
    print("position", int(pulse))
    return int(pulse)

def mmpersec_to_pulse(velocity):
    pulse = velocity
    print("velocity", int(pulse))
    return int(pulse)
    
def move_once(ser):
    testmovecommand = "test"
    print(testmovecommand)
