import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time

def connection(self):
    self.textbox_connect_a3.setText(self.ser_a3.name)
    self.textbox_baudrate_a3.setText(str(self.ser_a3.baudrate))
    self.textbox_parity_a3.setText(str(self.ser_a3.parity))
    self.textbox_bytesize_a3.setText(str(self.ser_a3.bytesize))

    self.textbox_connect_u1.setText(self.ser_u1.name)
    self.textbox_baudrate_u1.setText(str(self.ser_u1.baudrate))
    self.textbox_parity_u1.setText(str(self.ser_u1.parity))
    self.textbox_bytesize_u1.setText(str(self.ser_u1.bytesize))    

def reset_alarm(self):
    resetcommand = '0AR\r\n'
    print("Reset Alarm")
    self.ser_a3.write(resetcommand.encode())
    #self.ser_a3.flush()
    self.textbox_message_a3.setText('')

    self.ser_u1.write(resetcommand.encode())
    #self.ser_u1.flush()
    self.textbox_message_u1.setText('')
        
def emergency_stop(self, type):
    stopcommand = '0SP\r\n'
    print("Emergency Stop")
    if(type=='a3'):
        self.ser_a3.write(stopcommand.encode())
        self.textbox_message_a3.setText('Emergency!!!')
    if(type=='u1'):
        self.ser_u1.write(stopcommand.encode())
        self.textbox_message_u1.setText('Emergency!!!')
    
def manual_command(self):
    command = self.textbox_manual_command_a3.text()
    command = command + "\r\n"
    self.ser_a3.write(command.encode())
    self.ser_a3.flush()
    response = self.ser_a3.readline()
    self.textbox_message_a3.setText(str(response))
