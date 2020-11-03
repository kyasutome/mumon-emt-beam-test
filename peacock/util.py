import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time

def connection(self, a3, u1):
    if(a3==True):
        self.textbox_connect_a3.setText(self.ser_a3.name)
        self.textbox_baudrate_a3.setText(str(self.ser_a3.baudrate))
        self.textbox_parity_a3.setText(str(self.ser_a3.parity))
        self.textbox_bytesize_a3.setText(str(self.ser_a3.bytesize))

    if(u1==True):
        self.textbox_connect_u1.setText(self.ser_u1.name)
        self.textbox_baudrate_u1.setText(str(self.ser_u1.baudrate))
        self.textbox_parity_u1.setText(str(self.ser_u1.parity))
        self.textbox_bytesize_u1.setText(str(self.ser_u1.bytesize))    

def reset_alarm(self, a3, u1):
    resetcommand = '0AR\r\n'
    print("Reset Alarm")
    if(a3==True):
        self.ser_a3.write(resetcommand.encode())
        self.textbox_message_a3.setText('')

    if(u1==True):
        self.ser_u1.write(resetcommand.encode())
        self.textbox_message_u1.setText('')
        
def emergency_stop(self, a3, u1):
    stopcommand = '0SP\r\n'
    print("Emergency Stop")
    if(a3==True):
        self.ser_a3.write(stopcommand.encode())
        self.textbox_message_a3.setText('Emergency!!!')
    if(u1==True):
        self.ser_u1.write(stopcommand.encode())
        self.textbox_message_u1.setText('Emergency!!!')
    
def manual_command(self, type):
    if(type=='a3'):
        command = self.textbox_manual_command_a3.text()
        command = command + "\r\n"
        self.ser_a3.write(command.encode())
        self.ser_a3.flush()
        response = self.ser_a3.readline()
        self.textbox_message_a3.setText(str(response))
    if(type=='u1'):
        command = self.textbox_manual_command_u1.text()
        command = command + "\r\n"
        self.ser_u1.write(command.encode())
        self.ser_u1.flush()
        response = self.ser_u1.readline()
        self.textbox_message_u1.setText(str(response))
