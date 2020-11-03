import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time

    
def get_current_position(self,ser):
    ser.reset_input_buffer()
    command = '0RC\r\n'
    ser.write(command.encode())
    #ser.flush()
    response = ser.readline().decode()
    print(response)

    pos_act1 = response[3:8]
    pos_act2 = response[8:13]
    pos_act3 = response[13:18]
    print(pos_act1, pos_act2, pos_act3)
    
    pos_act1 = int(pos_act1, 16)*0.005
    pos_act2 = int(pos_act2, 16)*0.005
    pos_act3 = int(pos_act3, 16)*0.005

    self.textbox_pos_act1.setText(str(pos_act1))
    self.textbox_pos_act2.setText(str(pos_act2))
    self.textbox_pos_act3.setText(str(pos_act3))
