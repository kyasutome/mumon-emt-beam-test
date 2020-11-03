import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time

import movement
import measurement
import util
 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #Window Setting
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('QCheckBox')      
  
        #Dropdown list

        self.cb_type_preset = QComboBox(self)
        self.cb_type_preset.addItems(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
        self.cb_type_preset.setGeometry(1080, 215, 70, 50)

        #Serial Port
        self.ser_a3 = serial.Serial(
            port ='/dev/tty.usbserial-FTRU3RQX', 
            baudrate = 38400,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 2
            )

        self.ser_u1 = serial.Serial(
            port ='/dev/tty.usbserial-FTRVIAFX', 
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 4
            )

        #Button Setting
        #Util
        self.button_connect = QPushButton('Device Info', self)
        self.button_connect.setGeometry(0, 0, 150, 80)
        self.button_connect.clicked.connect(lambda:util.connection(self)) 

        self.button_resetalarm = QPushButton('Alarm Reset', self)
        self.button_resetalarm.setGeometry(0, 0, 150, 80)
        self.button_resetalarm.clicked.connect(lambda:util.reset_alarm(self)) 
        self.button_resetalarm.move(0, 100)

        self.button_manual_command = QPushButton('Manual Command', self)
        self.button_manual_command.setGeometry(0, 0, 150, 80)
        self.button_manual_command.clicked.connect(lambda:util.manual_command(self))
        self.button_manual_command.move(0, 500)

        self.button_emergency_a3 = QPushButton('Emergency Stop Button For A3', self)
        self.button_emergency_a3.setGeometry(300, 725, 300, 50)
        self.button_emergency_a3.clicked.connect(lambda:util.emergency_stop(self, 'a3'))

        self.button_emergency_u1 = QPushButton('Emergency Stop Button For U1', self)
        self.button_emergency_u1.setGeometry(700, 725, 300, 50)
        self.button_emergency_u1.clicked.connect(lambda:util.emergency_stop(self, 'u1'))

        self.qbtn = QPushButton('Quit', self)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(0, 700)

        #Movement
        self.button_move_cycle = QPushButton('Move 1 cycle', self)
        self.button_move_cycle.setGeometry(0, 0, 150, 80)
        self.button_move_cycle.clicked.connect(lambda:movement.move_cycle(self,self.ser_a3,self.ser_u1))
        self.button_move_cycle.move(0, 200)

        self.button_move_loop = QPushButton('Move 1 loop', self)
        self.button_move_loop.setGeometry(0, 0, 150, 80)
        self.button_move_loop.clicked.connect(lambda:movement.move_loop(self.ser_a3, self.ser_u1)) 
        self.button_move_loop.move(0, 300)

        self.button_getpos = QPushButton('Current Position', self)
        self.button_getpos.setGeometry(0, 0, 150, 80)
        self.button_getpos.clicked.connect(lambda:measurement.get_current_position(self,self.ser_a3,'a3')) 
        self.button_getpos.clicked.connect(lambda:measurement.get_current_position(self,self.ser_u1,'u1')) 
        self.button_getpos.move(0, 400)

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
        self.textbox_target_pos1.move(250, 220)
        self.textbox_target_pos1.resize(100, 20)
        self.textbox_target_pos1.setText(str(0))

        self.textbox_target_vel1 = QLineEdit(self)
        self.textbox_target_vel1.move(250, 250)
        self.textbox_target_vel1.resize(100, 20)
        self.textbox_target_vel1.setText(str(1))

        self.textbox_target_pos2 = QLineEdit(self)
        self.textbox_target_pos2.move(450, 220)
        self.textbox_target_pos2.resize(100, 20)
        self.textbox_target_pos2.setText(str(0))

        self.textbox_target_vel2 = QLineEdit(self)
        self.textbox_target_vel2.move(450, 250)
        self.textbox_target_vel2.resize(100, 20)
        self.textbox_target_vel2.setText(str(1))

        self.textbox_target_pos3 = QLineEdit(self)
        self.textbox_target_pos3.move(650, 220)
        self.textbox_target_pos3.resize(100, 20)
        self.textbox_target_pos3.setText(str(0))

        self.textbox_target_vel3 = QLineEdit(self)
        self.textbox_target_vel3.move(650, 250)
        self.textbox_target_vel3.resize(100, 20)
        self.textbox_target_vel3.setText(str(1))

        self.textbox_target_pos4 = QLineEdit(self)
        self.textbox_target_pos4.move(850, 220)
        self.textbox_target_pos4.resize(100, 20)
        self.textbox_target_pos4.setText(str(0))

        self.textbox_target_vel4 = QLineEdit(self)
        self.textbox_target_vel4.move(850, 250)
        self.textbox_target_vel4.resize(100, 20)
        self.textbox_target_vel4.setText(str(1))

        self.textbox_pos_act1 = QLineEdit(self)
        self.textbox_pos_act1.move(200, 425)
        self.textbox_pos_act1.resize(200, 20)

        self.textbox_pos_act2 = QLineEdit(self)
        self.textbox_pos_act2.move(450, 425)
        self.textbox_pos_act2.resize(200, 20)

        self.textbox_pos_act3 = QLineEdit(self)
        self.textbox_pos_act3.move(700, 425)
        self.textbox_pos_act3.resize(200, 20)

        self.textbox_pos_act4 = QLineEdit(self)
        self.textbox_pos_act4.move(950, 425)
        self.textbox_pos_act4.resize(200, 20)

        self.textbox_manual_command_a3 = QLineEdit(self)
        self.textbox_manual_command_a3.move(200, 525)
        self.textbox_manual_command_a3.resize(200, 20)

        self.textbox_message_a3 = QLineEdit(self)
        self.textbox_message_a3.move(400, 625)
        self.textbox_message_a3.resize(500, 20)

        self.textbox_message_u1 = QLineEdit(self)
        self.textbox_message_u1.move(400, 675)
        self.textbox_message_u1.resize(500, 20)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
