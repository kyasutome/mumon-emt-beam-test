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

    pos_act = response[2:7]
    print(pos_act)    
    pos_act = int(pos_act, 16)*0.005
    self.textbox_pos_act.setText(str(pos_act))
