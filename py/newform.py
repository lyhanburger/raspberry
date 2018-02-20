# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newform.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class Ui_Newform(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(241, 328)
        self.setStyleSheet("QWidget{\n"
"background-color:rgb(210,210,210);\n"
"}\n"
"\n"
                           "QLineEdit\n"
                           "{\n"
                           "    background:white;\n"
                           "    padding-left:5px ;\n"
                           "    padding-top:1px ;\n"
                           "    border-radius:3px;\n"
                           "    border: 1px solid rgb(209 , 209 , 209);\n"
                           "}\n"
                           "QLineEdit:hover\n"
                           "{\n"
                           "    padding-top:0px ;\n"
                           "    border: 1px solid rgb(21 , 131 , 221);\n"
                           "}\n"
                           "\n"
                           "QWidget{\n"
                           "color:rgb(33,33,33);\n"
                           "}\n"
                           "QPushButton{\n"
                           "color:white;\n"
                           "background-color: rgb(0, 75, 141);\n"
                           "border:0px;\n"
                           "border-radius:4px;\n"
                           "}\n"
                           "QPushButton:hover{\n"
                           "color:white;\n"
                           "background-color:rgb(108, 156, 224);\n"
                           "border:0px;\n"
                           "border-radius:4px;\n"
                           "}\n"
                           )
        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 181, 251))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.name_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.name_label.setObjectName("name_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.name_label)
        self.name_lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.name_lineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.id_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.id_label.setObjectName("id_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.id_label)
        self.id_lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.id_lineEdit.setObjectName("id_lineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.id_lineEdit)
        self.class_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.class_label.setObjectName("class_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.class_label)
        self.class_lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.class_lineEdit.setObjectName("class_lineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.class_lineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(7, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.LabelRole, spacerItem3)
        self.finish_buttn = QtWidgets.QPushButton(self)
        self.finish_buttn.setGeometry(QtCore.QRect(130, 290, 81, 32))
        self.finish_buttn.setObjectName("finish_buttn")
        self.cancel_buttn=QtWidgets.QPushButton(self)
        self.cancel_buttn.setGeometry(30, 290, 81, 32)
        self.cancel_buttn.setObjectName("cancel_buttn")

        self.retranslateUi(self)
        self.finish_buttn.clicked.connect(self.finish)
        self.cancel_buttn.clicked.connect(self.cancel)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏标签栏

    def retranslateUi(self, Newform):
        _translate = QtCore.QCoreApplication.translate
        Newform.setWindowTitle(_translate("Newform", "Dialog"))
        self.name_label.setText(_translate("Newform", "姓名"))
        self.id_label.setText(_translate("Newform", "学号"))
        self.class_label.setText(_translate("Newform", "班级"))
        self.finish_buttn.setText(_translate("Newform", "完成"))
        self.cancel_buttn.setText(_translate("Newform", "取消"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
    def get_name(self):
        return self.name_lineEdit.text()
    def get_class(self):
        return self.class_lineEdit.text()
    def get_id(self):
        return self.id_lineEdit.text()

    def finish(self):
        if self.checkempty():
            return self.accept()
        else:
            return
    def cancel(self):
        return self.reject()

    def checkempty(self):
        is_empty=True
        count_id = len(self.id_lineEdit.text())
        count_class = len(self.class_lineEdit.text())
        if count_id>10:
            QMessageBox.information(self, "未完成录入", "学号位数错误", QMessageBox.Ok)
            is_empty = False
            return is_empty
        if count_class>10:
            QMessageBox.information(self, "未完成录入", "班级位数错误", QMessageBox.Ok)
            is_empty = False
            return is_empty
        if not self.name_lineEdit.text():
            QMessageBox.information(self, "未完成录入", "姓名未键入", QMessageBox.Ok)
            is_empty=False
            return is_empty

        if not self.id_lineEdit.text():
            QMessageBox.information(self, "未完成录入", "学号未键入", QMessageBox.Ok)
            is_empty = False
            return is_empty

        if not self.class_lineEdit.text():
            QMessageBox.information(self, "未完成录入", "班级未键入", QMessageBox.Ok)
            is_empty = False
            return is_empty

        return is_empty