import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time
import serial.tools.list_ports

import movement
import measurement
import util
import yokogawa_power
import matsusada_power
 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):

        #Window Setting
        self.setGeometry(0, 0, 1200, 1000)
        self.setWindowTitle('Acutuator Automaton Peacock')      
        
        #Dropdown list        
        self.cb_type_preset = QComboBox(self)
        self.cb_type_preset.addItems(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
        self.cb_type_preset.setGeometry(1080, 615, 70, 50)

        #Serial Port
        a3 = False
        u1 = False
        gs = False
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if('FTRU3RQX' in str(p)):
                print(p)
                self.ser_a3 = serial.Serial(
                    port ='/dev/tty.usbserial-FTRU3RQX', 
                    baudrate = 38400,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS,
                    timeout = 2
                    )
                a3 = True

            if('FTRVIAFX' in str(p)):
                print(p)
                self.ser_u1 = serial.Serial(
                    port ='/dev/cu.usbserial-FTRVIAFX', 
                    baudrate = 9600,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS,
                    timeout = 4
                    )
                u1 = True

            if('AB0KED3C' in str(p)):
                print(p)
                self.ser_gs = serial.Serial(
                    port ='/dev/cu.usbserial-AB0KED3C', 
                    baudrate = 38400,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS,
                    timeout = 4
                    )
                gs = True

        if(a3 == False):
            self.ser_a3 = serial.Serial()
        if(u1 == False):
            self.ser_u1 = serial.Serial()
        if(gs == False):
            self.ser_gs = serial.Serial()

        layout_power_y = 100
        layout_alarm_y = 200
        layout_command_a3_y = 300
        layout_command_u1_y = 400
        layout_stop_y = 500
        layout_cycle_y = 600
        layout_loop_y = 700
        layout_current_pos_y = 800

        #Button Setting
        #Util
        self.button_connect = QPushButton('Device Info', self)
        self.button_connect.setGeometry(0, 0, 150, 80)
        self.button_connect.clicked.connect(lambda:util.connection(self, a3, u1)) 
        
        self.button_resetalarm = QPushButton('Alarm Reset', self)
        self.button_resetalarm.setGeometry(0, layout_alarm_y, 150, 80)
        self.button_resetalarm.clicked.connect(lambda:util.reset_alarm(self,a3,u1)) 

        self.button_manual_command_a3 = QPushButton('Command For A3', self)
        self.button_manual_command_a3.setGeometry(0, layout_command_a3_y, 150, 80)
        self.button_manual_command_a3.clicked.connect(lambda:util.manual_command(self,'a3'))

        self.button_manual_command_u1 = QPushButton('Command For U1', self)
        self.button_manual_command_u1.setGeometry(0, layout_command_u1_y, 150, 80)
        self.button_manual_command_u1.clicked.connect(lambda:util.manual_command(self,'u1'))

        self.button_emergency_a3 = QPushButton('Stop', self)
        self.button_emergency_a3.setGeometry(0, layout_stop_y, 150, 80)
        self.button_emergency_a3.clicked.connect(lambda:util.emergency_stop(self, a3, u1))

        #power
        self.button_power_yokogawa = QPushButton('Y Set', self)
        self.button_power_yokogawa.setGeometry(0, layout_power_y, 80, 80)
        self.button_power_yokogawa.clicked.connect(lambda:yokogawa_power.setting(self))

        self.button_power_yokogawa = QPushButton('Y ON', self)
        self.button_power_yokogawa.setGeometry(100, layout_power_y, 80, 80)
        self.button_power_yokogawa.clicked.connect(lambda:yokogawa_power.output_on(self))

        self.button_power_yokogawa = QPushButton('Y OFF', self)
        self.button_power_yokogawa.setGeometry(200, layout_power_y, 80, 80)
        self.button_power_yokogawa.clicked.connect(lambda:yokogawa_power.output_off(self))

        self.button_power_matsusada = QPushButton('M Set', self)
        self.button_power_matsusada.setGeometry(600, layout_power_y, 80, 80)
        self.button_power_matsusada.clicked.connect(lambda:matsusada_power.setting(self))

        self.button_power_matsusada = QPushButton('M ON', self)
        self.button_power_matsusada.setGeometry(700, layout_power_y, 80, 80)
        self.button_power_matsusada.clicked.connect(lambda:matsusada_power.output_on(self))

        self.button_power_matsusada = QPushButton('M OFF', self)
        self.button_power_matsusada.setGeometry(800, layout_power_y, 80, 80)
        self.button_power_matsusada.clicked.connect(lambda:matsusada_power.output_off(self))
            
        #Movement
        self.button_move_cycle = QPushButton('Move 1 cycle', self)
        self.button_move_cycle.setGeometry(0, layout_cycle_y, 150, 80)
        self.button_move_cycle.clicked.connect(lambda:movement.move_cycle(self,self.ser_a3,self.ser_u1,a3,u1))
        
        self.button_move_loop = QPushButton('Move 1 loop', self)
        self.button_move_loop.setGeometry(0, layout_loop_y, 150, 80)
        self.button_move_loop.clicked.connect(lambda:movement.move_loop(self, self.ser_a3, self.ser_u1,a3,u1)) 
            
        self.button_getpos = QPushButton('Current Position', self)
        self.button_getpos.setGeometry(0, layout_current_pos_y, 150, 80)
        self.button_getpos.clicked.connect(
            lambda:measurement.get_current_position(
            self,self.ser_a3,self.ser_u1,a3,u1)) 
        
        #TestBox setting
        self.textbox_connect_a3 = QLineEdit(self)
        self.textbox_connect_a3.move(200, 10)
        self.textbox_connect_a3.resize(200, 20)
        
        self.textbox_baudrate_a3 = QLineEdit(self)
        self.textbox_baudrate_a3.move(450, 10)
        self.textbox_baudrate_a3.resize(200, 20)
        
        self.textbox_parity_a3 = QLineEdit(self)
        self.textbox_parity_a3.move(700, 10)
        self.textbox_parity_a3.resize(200, 20)
        
        self.textbox_bytesize_a3 = QLineEdit(self)
        self.textbox_bytesize_a3.move(950, 10)
        self.textbox_bytesize_a3.resize(200, 20)
            
        self.textbox_connect_u1 = QLineEdit(self)
        self.textbox_connect_u1.move(200, 40)
        self.textbox_connect_u1.resize(200, 20)
            
        self.textbox_baudrate_u1 = QLineEdit(self)
        self.textbox_baudrate_u1.move(450, 40)
        self.textbox_baudrate_u1.resize(200, 20)
            
        self.textbox_parity_u1 = QLineEdit(self)
        self.textbox_parity_u1.move(700, 40)
        self.textbox_parity_u1.resize(200, 20)
            
        self.textbox_bytesize_u1 = QLineEdit(self)
        self.textbox_bytesize_u1.move(950, 40)
        self.textbox_bytesize_u1.resize(200, 20)
            
        self.textbox_target_pos1 = QLineEdit(self)
        self.textbox_target_pos1.move(250, layout_cycle_y+20)
        self.textbox_target_pos1.resize(100, 20)
        self.textbox_target_pos1.setText(str(0))
        
        self.textbox_target_vel1 = QLineEdit(self)
        self.textbox_target_vel1.move(250, layout_cycle_y+50)
        self.textbox_target_vel1.resize(100, 20)
        self.textbox_target_vel1.setText(str(1))
        
        self.textbox_target_pos2 = QLineEdit(self)
        self.textbox_target_pos2.move(450, layout_cycle_y+20)
        self.textbox_target_pos2.resize(100, 20)
        self.textbox_target_pos2.setText(str(0))
            
        self.textbox_target_vel2 = QLineEdit(self)
        self.textbox_target_vel2.move(450, layout_cycle_y+50)
        self.textbox_target_vel2.resize(100, 20)
        self.textbox_target_vel2.setText(str(1))
            
        self.textbox_target_pos3 = QLineEdit(self)
        self.textbox_target_pos3.move(650, layout_cycle_y+20)
        self.textbox_target_pos3.resize(100, 20)
        self.textbox_target_pos3.setText(str(0))
        
        self.textbox_target_vel3 = QLineEdit(self)
        self.textbox_target_vel3.move(650, layout_cycle_y+50)
        self.textbox_target_vel3.resize(100, 20)
        self.textbox_target_vel3.setText(str(1))
            
        self.textbox_target_pos4 = QLineEdit(self)
        self.textbox_target_pos4.move(850, layout_cycle_y+20)
        self.textbox_target_pos4.resize(100, 20)
        self.textbox_target_pos4.setText(str(0))
        
        self.textbox_target_vel4 = QLineEdit(self)
        self.textbox_target_vel4.move(850, layout_cycle_y+50)
        self.textbox_target_vel4.resize(100, 20)
        self.textbox_target_vel4.setText(str(1))
        
        self.textbox_pos_act1 = QLineEdit(self)
        self.textbox_pos_act1.move(200, layout_current_pos_y+25)
        self.textbox_pos_act1.resize(200, 20)
        
        self.textbox_pos_act2 = QLineEdit(self)
        self.textbox_pos_act2.move(450, layout_current_pos_y+25)
        self.textbox_pos_act2.resize(200, 20)
        
        self.textbox_pos_act3 = QLineEdit(self)
        self.textbox_pos_act3.move(700, layout_current_pos_y+25)
        self.textbox_pos_act3.resize(200, 20)
        
        self.textbox_pos_act4 = QLineEdit(self)
        self.textbox_pos_act4.move(950, layout_current_pos_y+25)
        self.textbox_pos_act4.resize(200, 20)
        
        self.textbox_manual_command_a3 = QLineEdit(self)
        self.textbox_manual_command_a3.move(200, layout_command_a3_y+25)
        self.textbox_manual_command_a3.resize(200, 20)

        self.textbox_manual_command_u1 = QLineEdit(self)
        self.textbox_manual_command_u1.move(200, layout_command_u1_y+25)
        self.textbox_manual_command_u1.resize(200, 20)

        self.textbox_yokogawa_power = QLineEdit(self)
        self.textbox_yokogawa_power.move(300, layout_power_y+25)
        self.textbox_yokogawa_power.resize(200, 20)

        self.textbox_matsusada_power = QLineEdit(self)
        self.textbox_matsusada_power.move(900, layout_power_y+25)
        self.textbox_matsusada_power.resize(200, 20)
        
        self.textbox_message_a3 = QLineEdit(self)
        self.textbox_message_a3.move(300, 900)
        self.textbox_message_a3.resize(700, 20)
        
        self.textbox_message_u1 = QLineEdit(self)
        self.textbox_message_u1.move(300, 930)
        self.textbox_message_u1.resize(700, 20)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
