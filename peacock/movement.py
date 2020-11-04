import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import subprocess
import os
import time

import measurement
import matsusada_power
import yokogawa_power
    
def move_cycle(self, ser_a3, ser_u1, a3, u1):
    if(a3==True):
        accelerator = '\x30\x32' #fixed
        waytotravel = '\x31' #fixed
        posid = "0A" #fixed

        target_pos1 = float(self.textbox_target_pos1.text())
        target_vel1 = float(self.textbox_target_vel1.text())
        target_pos2 = float(self.textbox_target_pos2.text())
        target_vel2 = float(self.textbox_target_vel2.text())
        target_pos3 = float(self.textbox_target_pos3.text())
        target_vel3 = float(self.textbox_target_vel3.text())
        
        if(target_pos1 < 0 or target_pos1 >= 50):
            target_pos1 = 10
            
            if(target_vel1 < 0 or target_vel1 >= 10):
                target_vel1 = 5
                
        command = '0MV'
                
        for i in range(4):
            if(i==0):
                position = target_pos1
                velocity = target_vel1

            if(i==1):
                position = target_pos2
                velocity = target_vel2
            
            if(i==2):
                position = target_pos3
                velocity = target_vel3

            if(i==3):
                position = 0
                velocity = 1
        
            print(position, velocity)
            posconvert = str( format( mm_to_pulse(position), '05x') )
            posconvert = posconvert.upper()
            velconvert = str( format( mmpersec_to_pulse(velocity), '03x'))
            velconvert = velconvert.upper()
            command += velconvert + accelerator + waytotravel + posconvert
        
        command += '\x30\x0D\x0A'
        print(command)
        ser_a3.write(command.encode())
        ser_a3.flush()
        response = ser_a3.readline()

    if(u1==True):
        accelerator = '\x31' #fixed
        waytotravel = '\x31' #fixed
        posid = "0A" #fixed
    
        target_pos4 = float(self.textbox_target_pos4.text())
        target_vel4 = float(self.textbox_target_vel4.text())
        
        if(target_pos4 < 0 or target_pos4 >= 500):
            target_pos1 = 10
            
        if(target_vel4 < 0 or target_vel4 >= 100):
            target_vel1 = 5
    
        command = '0MV'
    
        position = target_pos4
        velocity = target_vel4
        print(position, velocity)
        posconvert = str( format( mm_to_pulse(position), '05x') )
        posconvert = posconvert.upper()
        velconvert = str( format( mmpersec_to_pulse(velocity), '04x'))
        velconvert = velconvert.upper()
        command += velconvert + accelerator + waytotravel + posconvert        
        command += '\x0D\x0A'
        print(command)
        ser_u1.write(command.encode())
        response = ser_u1.readline()
        
def mm_to_pulse(position):
    pulse = position / 0.005
    return int(pulse)

def mmpersec_to_pulse(velocity):
    pulse = velocity
    return int(pulse)
    
def move_loop(self, ser_a3, ser_u1, a3, u1):
    yokogawa_power.output_on(self)
    matsusada_power.output_on(self)

    accelerator_u1 = '\x31' 
    waytotravel_u1 = '\x31'

    accelerator_a3 = '\x31\x31' 
    waytotravel_a3 = '\x31'
    datadir = "/Users/kenji/Documents/mumon-git/mumon-emt-beam-test-hub/peacock/data"
    path_to_posdata_a3 = datadir + "/position.txt"
    path_to_veldata_a3 = datadir + "/velocity.txt"
    with open(path_to_posdata_a3) as f:
        posdata_a3 = f.read().split()
    with open(path_to_veldata_a3) as g:
        veldata_a3 = g.read().split()

    path_to_posdata_u1 = datadir + "/position_u1.txt"
    path_to_veldata_u1 = datadir + "/velocity_u1.txt"
    with open(path_to_posdata_u1) as f:
        posdata_u1 = f.read().split()
    with open(path_to_veldata_u1) as g:
        veldata_u1 = g.read().split()

    time.sleep(10) # wait for the controlers ready

    for icycle in range(1):
        if(icycle > 0):
            time.sleep(10)
        for jcycle in range(2):
            if(u1==True):
                command = '0MV'
                position = int(posdata_u1[icycle])
                velocity = int(veldata_u1[icycle])
                print(position, velocity)
                posconvert = str( format( mm_to_pulse(position), '05x') )
                posconvert = posconvert.upper()
                velconvert = str( format( mmpersec_to_pulse(velocity), '04x'))
                velconvert = velconvert.upper()
                command += velconvert + accelerator_u1 + waytotravel_u1 + posconvert
                command += '\x0D\x0A'
                print(command)
                ser_u1.write(command.encode())
                ser_u1.flush()
                response = ser_u1.readline()

            if(a3==True):
                command = '0MV'
                for j in range(4):
                    id = 4*icycle + j
                    position = int(posdata_a3[id])
                    velocity = int(veldata_a3[id])
                    
                    print(position, velocity)
                    posconvert = str( format(int(mm_to_pulse(position)), '05x') )
                    velconvert = str( format(int(mmpersec_to_pulse(velocity)), '03x'))
                    command += velconvert + accelerator_a3 + waytotravel_a3 + posconvert
                command += '0\x0D\x0A'
                print(command)
                ser_a3.write(command.encode())
                time.sleep(2)
                response = ser_a3.readline()
                print(response)
            if(jcycle==0):
                time.sleep(2)            
            
        time.sleep(15)
        yokogawa_power.output_off(self)
        matsusada_power.output_off(self)  
        
