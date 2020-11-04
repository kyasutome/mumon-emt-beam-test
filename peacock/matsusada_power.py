import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import os
import subprocess
import time
    
def setting(self):
    script_path = os.path.dirname(os.path.abspath(__file__))
    path_sh = os.path.join(script_path, 'matsusada_power/power_set.sh')
    subprocess.run(['sh', path_sh])
    self.textbox_matsusada_power.setText('Setting')

def output_on(self):
    script_path = os.path.dirname(os.path.abspath(__file__))
    path_sh = os.path.join(script_path, 'matsusada_power/power_on.sh')
    subprocess.run(['sh', path_sh])
    self.textbox_matsusada_power.setText('Power ON')

def output_off(self):
    script_path = os.path.dirname(os.path.abspath(__file__))
    path_sh = os.path.join(script_path, 'matsusada_power/power_off.sh')
    subprocess.run(['sh', path_sh])
    self.textbox_matsusada_power.setText('Setting')
