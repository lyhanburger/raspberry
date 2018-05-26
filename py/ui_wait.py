# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wait.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5. QtWidgets import *

class Ui_WAIT(QDialog):
    def __init__(self, parent=None):
        super(Ui_WAIT, self).__init__(parent)
        self.setupUi(self)
    def setupUi(self, WAIT):
        WAIT.setObjectName("WAIT")
        WAIT.resize(312, 236)
        WAIT.setStyleSheet("QWidget{\n"
"background-color: rgb(209, 220, 230);\n"
"color: rgb(102, 124, 149);\n"
"}")
        self.label = QtWidgets.QLabel(WAIT)
        self.label.setGeometry(QtCore.QRect(90, 80, 131, 21))
        self.label.setStyleSheet("font-size: 16px;\n"
"")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-6)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(WAIT)
        self.progressBar.setGeometry(QtCore.QRect(100, 130, 118, 23))
        self.progressBar.setStyleSheet("QProgressBar{\n"
"        border: none;\n"
"        color: white;\n"
"        text-align: center;\n"
"        background-color: rgb(100, 112, 130);\n"
"}\n"
"QProgressBar::chunk {\n"
"        border: none;\n"
"        background: rgb(179, 204, 250);\n"
"}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        
        self.retranslateUi(WAIT)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏标签栏
        self.timer = QTimer()
        self.timer.timeout.connect(self.process)
        self.timer.start(25)
        QtCore.QMetaObject.connectSlotsByName(WAIT)


    def retranslateUi(self, WAIT):
        _translate = QtCore.QCoreApplication.translate
        WAIT.setWindowTitle(_translate("WAIT", "Dialog"))
        self.label.setText(_translate("WAIT", "设备准备中"))

    def process(self):
        val = self.progressBar.value()
        self.progressBar.setValue(val+1)
        if val+ 1 == 100:
            self.accept()
