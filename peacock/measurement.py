import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time
    
def get_current_position(self,ser_a3, ser_u1, a3, u1):
    print("Get Position")
    command = '0RC\r\n'
    if(a3==True):
        ser_a3.reset_input_buffer()
        ser_a3.write(command.encode())
        response = ser_a3.readline().decode()
        print("response", response)
        if(len(response)==25):
            pos_act1 = response[3:8]
            pos_act2 = response[8:13]
            pos_act3 = response[13:18]
            pos_act1 = int(pos_act1, 16)*0.005
            pos_act2 = int(pos_act2, 16)*0.005
            pos_act3 = int(pos_act3, 16)*0.005    
            print(pos_act1, pos_act2, pos_act3)        
            self.textbox_pos_act1.setText(str(pos_act1))
            self.textbox_pos_act2.setText(str(pos_act2))
            self.textbox_pos_act3.setText(str(pos_act3))
        if(len(response)!=25):
            self.textbox_pos_act1.setText("Error")
            self.textbox_pos_act2.setText("Error")
            self.textbox_pos_act3.setText("Error")
        
    if(u1==True):
        ser_u1.reset_input_buffer()
        ser_u1.write(command.encode())
        response = ser_u1.readline().decode()
        print("response", response)
        if(len(response)==10):
            pos_act = response[3:8]
            pos_act = int(pos_act, 16)*0.005
            print(pos_act)
            self.textbox_pos_act4.setText(str(pos_act))
        if(len(response)!=10):
            self.textbox_pos_act4.setText("Error")

