# -*- coding: utf-8 -*-

from PyQt5 import uic

from PyQt5 import QtWidgets
from PyQt5.Qt import Qt


from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import QApplication

import constantValues as cv

import debugPrinter as dp

from PyQt5.QtCore import QSettings, QPoint, QSize

from PyQt5.QtWidgets import QInputDialog, QLineEdit


# class MplCanvas(FigureCanvas):
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)

qt_creator_file = "mi_app/mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # update_data = pyqtSignal(float,float)
    evt_win = pyqtSignal(str,str)
    # evt_win_data = pyqtSignal(str,int,str)

    

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_flash_led.triggered.connect(self.flash_led_triggered)

        # self.btn_flash_led.clicked.connect(self.flash_led_btn_click)
        self.btn_open_com.clicked.connect(self.open_com_btn_click)
        self.btn_close_com.clicked.connect(self.close_com_btn_click)
        self.btn_con_dev.clicked.connect(self.con_dev_btn_click)
        self.btn_stop_disconnect.clicked.connect(self.stop_disconnect_btn_click)

        # self.mac_to_connect = "00:00:00:00:00:00"

        # self.btn_open_close.setCheckable(True)

        self.btn_mi_train.clicked.connect(self.mi_train_btn_click)
        self.btn_mi_test.clicked.connect(self.mi_test_btn_click)
        self.btn_eye_open_close.clicked.connect(self.eye_open_close_btn_click)
        self.btn_generate_model.clicked.connect(self.btn_generate_model_btn_click)
        self.btn_curctrl_train.clicked.connect(self.curctrl_train_btn_click)
        self.btn_curctrl_task.clicked.connect(self.curctrl_task_btn_click)
        self.btn_generate_curctrl_model.clicked.connect(self.btn_generate_curctrl_model_btn_click)

        self.c=None

        self.settings = QSettings('./uiSetting.ini', QSettings.IniFormat)     
        # Initial window size/pos last saved. Use default values for first time
        self.resize(self.settings.value("size", QSize(270, 225)))
        if (self.settings.value("pos") is not None) and (self.settings.value("size") is not None):
            screenRect = QApplication.desktop().screenGeometry()
            self.height = screenRect.height()
            if self.settings.value("pos").x()<(screenRect.width()-100) and \
                self.settings.value("pos").y()<(screenRect.height()-100):
                self.move(self.settings.value("pos", QPoint(50, 50)))            

        self.comboBox_serialPort.addItem(cv.SERIAL_SIMULATOR)

        dp.dpt("mainwindow construction")

    # def process_finished(self):
    #     self.p = None
    #     print('del process')
    def flash_led_triggered(self):
        dp.dpt('flash_led_triggered - - -')
        self.evt_win.emit(cv.SERIAL_CMD_FALSH_LED,cv.DUMMY_STR)

    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Q:
            self.close()
            

    def stop_disconnect_btn_click(self):
        # self.evt_win_data.emit(cv.EVT_WIN_CMD_TO_BLE,cv.DUMMY_INT,cv.SERIAL_CMD_STOP_DISCONNECT)
        self.evt_win.emit(cv.SERIAL_CMD_STOP_DISCONNECT,cv.DUMMY_STR)
        self.log_info('disconnecting ... ')

    def con_dev_btn_click(self):
        # self.mac_to_connect = 
        # dp.dpt(self.comboBox_macs.currentText())
        self.evt_win.emit(cv.EVT_WIN_CMD_CON_DEV, self.comboBox_macs.currentText())
        self.log_info('connecting ... ')

    def curctrl_task_btn_click(self):
        self.evt_win.emit(cv.EVT_WIN_CURCTRL,cv.DUMMY_STR)

    def curctrl_train_btn_click(self):
        self.evt_win.emit(cv.EVT_WIN_CURCTRL_TRAIN,cv.DUMMY_STR)

    def mi_train_btn_click(self):
        self.evt_win.emit(cv.EVT_WIN_MI_TRAIN,cv.DUMMY_STR)        

    def mi_test_btn_click(self):
        self.evt_win.emit(cv.EVT_WIN_MI_TEST,cv.DUMMY_STR)        
       

    def eye_open_close_btn_click(self):
        self.evt_win.emit(cv.EVT_WIN_EYE_OC,cv.DUMMY_STR)        

    def btn_generate_model_btn_click(self):
        self.evt_win.emit(cv.EVT_WIN_GENERATW_MODEL,cv.DUMMY_STR)        
    def btn_generate_curctrl_model_btn_click(self):
        self.evt_win.emit(cv.EVT_WIN_GENERATW_CURCTRL_MODEL,cv.DUMMY_STR)        



    def open_com_btn_click(self,flag):
        if self.comboBox_serialPort.count() > 0:
            self.evt_win.emit(cv.EVT_WIN_CMD_OPEN_COM,self.comboBox_serialPort.currentText())

    def close_com_btn_click(self):
        # print('-----')
        self.evt_win.emit(cv.EVT_WIN_CMD_CLOSE_COM,cv.DUMMY_STR)

    def exit_app(self):
        self.close()


    def closeEvent(self, event):
        # do stuff
        r = QMessageBox.question(self,"Window Close","Are you sure to close?",
            QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if r == QMessageBox.Yes:
            self.evt_win.emit(cv.EVT_WIN_QUIT,cv.DUMMY_STR)        
            event.accept()

            self.settings.setValue("size", self.size())
            self.settings.setValue("pos", self.pos())

            QApplication.quit()

        else:
            event.ignore()
        
    def show_error(self,s):
        QMessageBox.warning(self, "error", s)


    def get_input_fileName(self,hint):
        text, ok = QInputDialog().getText(self, "File Name For Saving",
                                 "(you can use Subject Name or Session name):", QLineEdit.Normal,hint)
        return text,ok
        # if ok and text:
        #     c = a[:a.rfind('/')+1] + text
        #     print(c)
        #     if (self.fs.make_path(c)):
        #         QMessageBox.warning(self, "error", "this file has been exist!")
        #         return 'f'
        #     else:
        #         self.fs.setup(c,text)
        #         return 's'
        
 
    def add_serial_port_to_combox(self,li):
        for l in li:
            self.comboBox_serialPort.addItem(l.portName())

        # if self.comboBox_serialPort.count() > 0:
        #     self.evt_win_data.emit(cv.EVT_WIN_BTN_CLICK_OPEN_CLOSE, \
        #                              cv.WIN_CMD_SERIAL_OPEN,\
        #                              self.comboBox_serialPort.currentText())
    def set_combox_item(self,s):
        self.comboBox_serialPort.setCurrentText(s)

    def log_info(self,s):
        if(s!=cv.LOG_INFO_INGNORE):
            self.textBrowser_evt_log.append(s)

    def new_mac(self,s):
        # dp.dpt(s)
        if (self.comboBox_macs.findText(s)==-1):
            self.comboBox_macs.addItem(s)

    # def get_mac_to_connect(self):
    #     return self.mac_to_connect

    def serial_cmd(self,cmd):
        if cmd == cv.EVT_SERIAL_OPEN_SUC:
            self.btn_open_com.setEnabled(False)
            self.btn_close_com.setEnabled(True)
        elif cmd == cv.EVT_SERIAL_OPEN_FAILED:
            self.log_info('serial opend faild, check the device manager')
        elif cmd == cv.EVT_SERIAL_CLOSE_SUC:
            self.btn_open_com.setEnabled(True)
            self.btn_close_com.setEnabled(False)

    def dev_evt(self,s):
        self.log_info(s)
        # if s == cv.EVT_DEV_CON_SETUP_DONE:
        #     self.btn_stop_disconnect.setEnabled(True)
        #     self.btn_con_dev.setEnabled(False)
        # elif s == cv.EVT_DEV_DISCONNECT:
        #     self.btn_stop_disconnect.setEnabled(False)
        #     self.btn_con_dev.setEnabled(True)