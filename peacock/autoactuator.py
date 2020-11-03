import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import serial
import time

import movement
import measurement
 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #Window Setting
        self.setGeometry(0, 0, 1300, 1300)
        self.setWindowTitle('QCheckBox')      
  
        #Dropdown list

        self.cb_type_preset = QComboBox(self)
        self.cb_type_preset.addItems(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
        self.cb_type_preset.setGeometry(900, 75, 240, 340)

        #Serial Port
        self.ser = serial.Serial(
            port ='/dev/tty.usbserial-FTRU3RQX', 
            baudrate = 38400,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 2
            )

        #Button Setting
        self.button_connect = QPushButton('Device Info', self)
        self.button_connect.setGeometry(0, 0, 150, 80)
        self.button_connect.clicked.connect(self.connection) 

        self.button_resetalarm = QPushButton('Alarm Reset', self)
        self.button_resetalarm.setGeometry(0, 0, 150, 80)
        self.button_resetalarm.clicked.connect(self.reset_alarm) 
        self.button_resetalarm.move(0, 100)

        self.button_move_cycle = QPushButton('Move 1 cycle', self)
        self.button_move_cycle.setGeometry(0, 0, 150, 80)
        self.button_move_cycle.clicked.connect(lambda:movement.move_cycle(self,self.ser)) 
        self.button_move_cycle.move(0, 200)

        self.button_move_loop = QPushButton('Move 1 loop', self)
        self.button_move_loop.setGeometry(0, 0, 150, 80)
        self.button_move_loop.clicked.connect(lambda:movement.move_loop(self.ser)) 
        self.button_move_loop.move(0, 300)

        self.button_getpos = QPushButton('Current Position', self)
        self.button_getpos.setGeometry(0, 0, 150, 80)
        self.button_getpos.clicked.connect(lambda:measurement.get_current_position(self,self.ser)) 
        self.button_getpos.move(0, 400)

        self.button_makeerror = QPushButton('Error Code', self)
        self.button_makeerror.setGeometry(0, 0, 150, 80)
        self.button_makeerror.clicked.connect(self.make_error) 
        self.button_makeerror.move(0, 500)

        self.button_manual_command = QPushButton('Manual Command', self)
        self.button_manual_command.setGeometry(0, 0, 150, 80)
        self.button_manual_command.clicked.connect(self.manual_command)
        self.button_manual_command.move(0, 600)

        self.button_emergency = QPushButton('Emergency Stop Button', self)
        self.button_emergency.setGeometry(550, 800, 300, 50)
        self.button_emergency.clicked.connect(self.emergency_stop)

        self.qbtn = QPushButton('Quit', self)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(0, 800)

        #TestBox setting
        self.textbox_connect = QLineEdit(self)
        self.textbox_connect.move(200, 35)
        self.textbox_connect.resize(200, 20)

        self.textbox_baudrate = QLineEdit(self)
        self.textbox_baudrate.move(450, 35)
        self.textbox_baudrate.resize(200, 20)

        self.textbox_parity = QLineEdit(self)
        self.textbox_parity.move(700, 35)
        self.textbox_parity.resize(200, 20)

        self.textbox_bytesize = QLineEdit(self)
        self.textbox_bytesize.move(950, 35)
        self.textbox_bytesize.resize(200, 20)

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

        self.textbox_pos_act1 = QLineEdit(self)
        self.textbox_pos_act1.move(200, 425)
        self.textbox_pos_act1.resize(200, 20)

        self.textbox_pos_act2 = QLineEdit(self)
        self.textbox_pos_act2.move(450, 425)
        self.textbox_pos_act2.resize(200, 20)

        self.textbox_pos_act3 = QLineEdit(self)
        self.textbox_pos_act3.move(700, 425)
        self.textbox_pos_act3.resize(200, 20)

        self.textbox_error_info = QLineEdit(self)
        self.textbox_error_info.move(200, 525)
        self.textbox_error_info.resize(200, 20)

        self.textbox_manual_command = QLineEdit(self)
        self.textbox_manual_command.move(200, 625)
        self.textbox_manual_command.resize(200, 20)

        self.textbox_manual_command_result = QLineEdit(self)
        self.textbox_manual_command_result.move(450, 625)
        self.textbox_manual_command_result.resize(400, 20)
    
    def connection(self):
        self.textbox_connect.setText(self.ser.name)
        self.textbox_baudrate.setText(str(self.ser.baudrate))
        self.textbox_parity.setText(str(self.ser.parity))
        self.textbox_bytesize.setText(str(self.ser.bytesize))

    def make_error(self):
        self.ser.reset_input_buffer()
        errorcommand = '0AB\x0D\x0A'
        self.ser.write(errorcommand.encode())
        time.sleep(2)
        response = self.ser.readline()
        self.textbox_error_info.setText(str(response))

    def reset_alarm(self):
        resetcommand = '0AR\r\n'
        print("Reset Alarm")
        self.ser.write(resetcommand.encode())
        self.ser.flush()
        self.textbox_error_info.setText('')

    def emergency_stop(self):
        stopcommand = '0SP\r\n'
        print("Emergency Stop")
        self.ser.write(stopcommand.encode())
        self.textbox_error_info.setText('Emergency!!!')

    def manual_command(self):
        command = self.textbox_manual_command.text()
        command = command + "\r\n"
        self.ser.write(command.encode())
        self.ser.flush()
        response = self.ser.readline()
        self.textbox_manual_command_result.setText(str(response))
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
