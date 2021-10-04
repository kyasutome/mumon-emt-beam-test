import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import subprocess
import os
import time
import tkinter
import threading

import measurement
import matsusada_power
import yokogawa_power
    
def move_cycle(self, ser_a3, ser_u1, a3, u1):
    if(self.operation_manual.isChecked()):
        move_cycle_manual(self, ser_a3, ser_u1, a3, u1)

    if(self.operation_sign.isChecked()):
        move_cycle_sign(self, ser_a3, ser_u1, a3, u1)    

def move_cycle_manual(self, ser_a3, ser_u1, a3, u1):
    print("operation mode : Manual")
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

def move_cycle_sign(self, ser_a3, ser_u1, a3, u1):
    print("operation mode : Sign")
    posid = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    #ID = 0
    for i in range(9):
        global ID
        print(self.cb_type_preset.currentText(), posid[i])
        if(self.cb_type_preset.currentText() == posid[i]):
            ID = i
            print("id", i)
            break
            
    print("id", ID)
    
    datadir = "/home/nd280up/2020-11/mumon-emt-beam-test/automation/peacock/data"
    path_to_posdata_a3 = datadir + "/position.txt"
    path_to_veldata_a3 = datadir + "/velocity.txt"
    with open(path_to_posdata_a3) as f:
        posdata_a3 = f.read().split()
    with open(path_to_veldata_a3) as g:
        veldata_a3 = g.read().split()

    path_to_posdata_u1 = datadir + "/position-u1.txt"
    path_to_veldata_u1 = datadir + "/velocity-u1.txt"
    with open(path_to_posdata_u1) as f:
        posdata_u1 = f.read().split()
    with open(path_to_veldata_u1) as g:
        veldata_u1 = g.read().split()
    
    if(u1==True):
        accelerator = '\x31' #fixed
        waytotravel = '\x31' #fixed
        command = '0MV'
        position = int(posdata_u1[ID])
        velocity = int(veldata_u1[ID])
        print(position, velocity)
        posconvert = str( format(int(mm_to_pulse(position)), '05x') )
        posconvert = posconvert.upper()
        velconvert = str( format(int(mmpersec_to_pulse(velocity)), '04x'))
        velconvert = velconvert.upper()
        command += velconvert + accelerator + waytotravel + posconvert
        command += '\x0D\x0A'
        print(command)
        ser_u1.write(command.encode())
        #ser_u1.flush()
        response = ser_u1.readline()
        print(response)
        
    if(a3==True):
        accelerator = '\x31\x31' 
        waytotravel = '\x31'
        command = '0MV'
        for j in range(4):
            id = 4*ID + j
            position = int(posdata_a3[id])
            velocity = int(veldata_a3[id])
            
            print(position, velocity)
            posconvert = str( format(int(mm_to_pulse(position)), '05x') )
            posconvert = posconvert.upper()
            velconvert = str( format(int(mmpersec_to_pulse(velocity)), '03x'))
            velconvert = velconvert.upper()
            command += velconvert + accelerator + waytotravel + posconvert
        command += '0\x0D\x0A'
        print(command)
        ser_a3.write(command.encode())
        ser_a3.flush()
        response = ser_a3.readline()
        print(response)        
        
def mm_to_pulse(position):
    pulse = position / 0.005
    return int(pulse)

def mmpersec_to_pulse(velocity):
    pulse = velocity
    return int(pulse)

def thread_test2(self, ser_a3, ser_u1, a3, u1):
    thread2 = threading.Thread(target=move_loop(self,ser_a3,ser_u1,a3,u1))
    thread2.start()    

def loop_status_monitor(self, ser_a3, ser_u1, a3, u1):

    self.root = tkinter.Tk()
    self.root.title("Peacock ---Loop Status Monitor---")
    self.root.geometry("800x800")

   # button_start = tkinter.Button(self.root, text='Start', height = 2, width = 20, bg = "yellow", fg = "black",
    #                              command=lambda:move_loop(self,self.ser_a3,self.ser_u1,a3,u1))
    button_start = tkinter.Button(self.root, text='Start', height = 2, width = 20, bg = "yellow", fg = "black",
                                  command=lambda:thread_test2(self, ser_a3, ser_u1, a3, u1))

    button_start.place(x=100, y=20)

    button_end = tkinter.Button(self.root, text='End', height = 2, width = 20, bg = "yellow", fg = "black",
                                command=lambda:end(self))
    button_end.place(x=300, y=20)

    self.button_pos_A = tkinter.Button(self.root, text='Pos A', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_A.place(x=100, y=100)

    self.button_pos_B = tkinter.Button(self.root, text='Pos B', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_B.place(x=100, y=300)

    self.button_pos_C = tkinter.Button(self.root, text='Pos C', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_C.place(x=100, y=500)

    self.button_pos_D = tkinter.Button(self.root, text='Pos D', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_D.place(x=300, y=100)

    self.button_pos_E = tkinter.Button(self.root, text='Pos E', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_E.place(x=300, y=300)

    self.button_pos_F = tkinter.Button(self.root, text='Pos F', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_F.place(x=300, y=500)

    self.button_pos_G = tkinter.Button(self.root, text='Pos G', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_G.place(x=500, y=100)

    self.button_pos_H = tkinter.Button(self.root, text='Pos H', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_H.place(x=500, y=300)

    self.button_pos_I = tkinter.Button(self.root, text='Pos I', height = 10, width = 20, bg = "blue", fg = "white")
    self.button_pos_I.place(x=500, y=500)

    self.root.mainloop()

def move_loop(self, ser_a3, ser_u1, a3, u1):

    for i in range(3):
        time.sleep(5)
        colur_update(self, i)
        self.root.update()
        
""""
    accelerator_u1 = '\x31' 
    waytotravel_u1 = '\x31'

    accelerator_a3 = '\x31\x31' 
    waytotravel_a3 = '\x31'
    datadir = "/home/nd280up/2020-11/mumon-emt-beam-test/automation/peacock/data"
    path_to_posdata_a3 = datadir + "/position.txt"
    path_to_veldata_a3 = datadir + "/velocity.txt"
    with open(path_to_posdata_a3) as f:
        posdata_a3 = f.read().split()
    with open(path_to_veldata_a3) as g:
        veldata_a3 = g.read().split()

    path_to_posdata_u1 = datadir + "/position-u1.txt"
    path_to_veldata_u1 = datadir + "/velocity-u1.txt"
    with open(path_to_posdata_u1) as f:
        posdata_u1 = f.read().split()
    with open(path_to_veldata_u1) as g:
        veldata_u1 = g.read().split()

    time.sleep(10) # wait for the controlers ready

    for icycle in range(9):
        yokogawa_power.output_on(self)
        matsusada_power.output_on(self)
        time.sleep(12)
        for jcycle in range(2):
            if(u1==True):
                command = '0MV'
                position = int(posdata_u1[icycle])
                velocity = int(veldata_u1[icycle])
                print(position, velocity)
                posconvert = str( format(int(mm_to_pulse(position)), '05x') )
                posconvert = posconvert.upper()
                velconvert = str( format(int(mmpersec_to_pulse(velocity)), '04x'))
                velconvert = velconvert.upper()
                command += velconvert + accelerator_u1 + waytotravel_u1 + posconvert
                command += '\x0D\x0A'
                print(command)
                ser_u1.write(command.encode())
                #ser_u1.flush()
                response = ser_u1.readline()
                print(response)

            if(a3==True):
                command = '0MV'
                for j in range(4):
                    id = 4*icycle + j
                    position = int(posdata_a3[id])
                    velocity = int(veldata_a3[id])
                    
                    print(position, velocity)
                    posconvert = str( format(int(mm_to_pulse(position)), '05x') )
                    posconvert = posconvert.upper()
                    velconvert = str( format(int(mmpersec_to_pulse(velocity)), '03x'))
                    velconvert = velconvert.upper()
                    command += velconvert + accelerator_a3 + waytotravel_a3 + posconvert
                command += '0\x0D\x0A'
                print(command)
                ser_a3.write(command.encode())
                ser_a3.flush()
                response = ser_a3.readline()
                print(response)

            if(jcycle==0):
                time.sleep(5)  
        time.sleep(20)
        measurement.get_current_position(self, ser_a3, ser_u1, a3, u1)

        colur_update(self, icycle)
        
        yokogawa_power.output_off(self)
        matsusada_power.output_off(self)
        time.sleep(5)
"""""

def colur_update(self, icycle):
    if(icycle==0):
        self.button_pos_I["bg"] = "blue"
        self.button_pos_A["bg"] = "red"
        
    if(icycle==1):
        self.button_pos_A["bg"] = "blue"
        self.button_pos_B["bg"] = "red"
                
    if(icycle==2):
        self.button_pos_B["bg"] = "blue"
        self.button_pos_C["bg"] = "red"    

    self.root.update()

    
def end(self):
    print("end")
    self.root.destroy()
    #self.root.quit()
