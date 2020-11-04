import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time
    
def setting(self):
    remote_on(self)
    voltage_range_set(self)
    current_range_set(self)
    voltage_level_set(self)
    self.textbox_yokogawa_power.setText('Setting')
    
def remote_on(self):
    command = ':SYST:REM\r\n'
    self.ser_gs.write(command.encode())

    command = ':SYST:ERR?\r\n'
    self.ser_gs.write(command.encode())
    response = self.ser_gs.readline()
    print(response)

def voltage_range_set(self):
    command = 'SOUR:VOLT:RANG 30\r\n'
    self.ser_gs.write(command.encode())
    
    command = 'SOUR:VOLT:RANG?\r\n'
    self.ser_gs.write(command.encode())
    response = self.ser_gs.readline()

def current_range_set(self):
    command = ':SOUR:CURR:PROT:ULIM 2\r\n'
    self.ser_gs.write(command.encode())
    
    command = ':SOUR:CURR:PROT:ULIM?\r\n'
    self.ser_gs.write(command.encode())
    response = self.ser_gs.readline()
    print(response)

def voltage_level_set(self):
    command = ':SOUR:VOLT:LEV 24\r\n'
    self.ser_gs.write(command.encode())

    command = ':SOUR:VOLT:LEV?\r\n'
    self.ser_gs.write(command.encode())
    response = self.ser_gs.readline()
    print("function", response)

def output_on(self):
    command = ':OUTPut ON\r\n'
    self.ser_gs.write(command.encode())
    
    command = ':OUTP:STAT?\r\n'
    self.ser_gs.write(command.encode())
    response = self.ser_gs.readline()
    print("output", response)

    command = ':SOUR:VOLT:LEV?\r\n'
    self.ser_gs.write(command.encode())
    response = self.ser_gs.readline()

    self.textbox_yokogawa_power.setText('Power ON ' + response.decode())

def output_off(self):
    command = ':OUTP OFF\r\n'
    self.ser_gs.write(command.encode())

    command = ':OUTP:STAT?\r\n'
    self.ser_gs.write(command.encode())
    response = self.ser_gs .readline()
    print("output", response)
    self.textbox_yokogawa_power.setText('Setting')
