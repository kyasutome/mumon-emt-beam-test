import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time

    
def get_current_position(self,ser):
    command = '0RC\r\n'
    ser.write(command.encode())
    ser.flush()
    time.sleep(2)
    response = ser.readline()
    self.textbox_pos_act1.setText(str(response))
    self.textbox_pos_act2.setText(str(response))
    self.textbox_pos_act3.setText(str(response))
    self.textbox_pos_act4.setText(str(response))
