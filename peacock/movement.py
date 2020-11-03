import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time
    
def move_cycle(self, ser):
    accelerator = '\x30\x32' #fixed
    waytotravel = '\x31' #fixed
    posid = "0A" #fixed

    target_pos = float(self.textbox_target_pos.text())
    target_vel = float(self.textbox_target_vel.text())

    print("targetpos", target_pos, "targetvel", target_vel)

    if(target_pos < 0 or target_pos >= 50):
        target_pos = 10

    if(target_vel < 0 or target_vel >= 10):
        target_vel = 5
    
    command = '0MV'
    for j in range(4):
        position = target_pos
        velocity = target_vel
        
        print(position, velocity)
        posconvert = str( format( mm_to_pulse(position), '05x') )
        posconvert = posconvert.upper()
        velconvert = str( format( mmpersec_to_pulse(velocity), '03x'))
        velconvert = velconvert.upper()
        command += velconvert + accelerator + waytotravel + posconvert

    command += '\x30\x0D\x0A'
    print(command)
    ser.write(command.encode())
    time.sleep(3)
    ser.flush()
    response = ser.readline()
    print(response)
    time.sleep(3)

def mm_to_pulse(position):

    pulse = position / 0.005
    return int(pulse)

def mmpersec_to_pulse(velocity):
    pulse = velocity
    return int(pulse)
    
def move_loop(ser):
    accelerator = "22" #fixed
    waytotravel = "2" #fixed
    posid = "0A" #fixed
    datadir = "/Users/kenji/Documents/mumon-git/mumon-emt-beam-test-hub/peacock/data"
    path_to_posdata = datadir + "/position.txt"
    path_to_veldata = datadir + "/velocity.txt"

    with open(path_to_posdata) as f:
        posdata = f.read().split()
        print(posdata)
    with open(path_to_veldata) as g:
        veldata = g.read().split()
        print(veldata)

    for i in range(1):
        command = '0MV'
        for j in range(4):
            id = 4*i + j
            position = int(posdata[id])
            velocity = int(veldata[id])

            print(position, velocity)
            posconvert = str( format(int(mm_to_pulse(position)), '05x') )
            velconvert = str( format(int(mmpersec_to_pulse(velocity)), '03x'))
            command += velconvert + accelerator + waytotravel + posconvert
        print(command)
        command += '0\x0D\x0A'
        ser.write(command.encode())
        time.sleep(2)
        ser.flush()
        response = ser.readline()
        print(response)
        time.sleep(20)
