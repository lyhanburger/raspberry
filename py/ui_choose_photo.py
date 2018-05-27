# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_photo.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import face_recognition
from PIL import Image
from PIL.ImageQt import ImageQt
class Ui_CHOOSE_PHOTO(QDialog):
    def __init__(self, parent=None, photos = [], image = None):
        super(Ui_CHOOSE_PHOTO, self).__init__()
        self.photos = photos
        self.image = image
        self.setupUi(self)
    def setupUi(self, CHOOSE_PHOTO):
        self.setWindowFlags(Qt.FramelessWindowHint)
        CHOOSE_PHOTO.setObjectName("CHOOSE_PHOTO")
        CHOOSE_PHOTO.resize(400, 300)
        CHOOSE_PHOTO.setStyleSheet("QWidget{\n"
"background-color:rgb(216, 213, 227);\n"
"color: rgb(110, 105, 138);\n"
"}")
        self.stackedWidget = QtWidgets.QStackedWidget(CHOOSE_PHOTO)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.stackedWidget.setStyleSheet("QPushButton{\n"
"border: 0px solid rgb(173, 177, 189);\n"
"border-radius: 4px;\n"
"color: white;\n"
"background-color:rgb(211, 157, 162);\n"
"}\n"
"QPushButton:hover{\n"
"border: 0px solid rgb(173, 177, 189);\n"
"border-radius: 4px;\n"
"color: white;\n"
"background-color:rgb(240, 187, 187);\n"
"}")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label = QtWidgets.QLabel(self.page)
        self.label.setGeometry(QtCore.QRect(100, 40, 211, 31))
        self.label.setStyleSheet("font-size:17px;")
        self.label.setObjectName("label")
        self.photo = QtWidgets.QLabel(self.page)
        self.photo.setGeometry(QtCore.QRect(140, 80, 141, 161))
        self.photo.setObjectName("photo")
        self.next_pushButton = QtWidgets.QPushButton(self.page)
        self.next_pushButton.setGeometry(QtCore.QRect(60, 260, 113, 32))
        self.next_pushButton.setObjectName("next_pushButton")
        self.accept_pushButton = QtWidgets.QPushButton(self.page)
        self.accept_pushButton.setGeometry(QtCore.QRect(250, 260, 113, 32))
        self.accept_pushButton.setObjectName("accept_pushButton")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(90, 110, 231, 51))
        self.label_2.setStyleSheet("font-size:18px;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.reject_pushButton = QtWidgets.QPushButton(self.page_2)
        self.reject_pushButton.setGeometry(QtCore.QRect(250, 250, 113, 32))
        self.reject_pushButton.setObjectName("reject_pushButton")
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(CHOOSE_PHOTO)
        self.stackedWidget.setCurrentIndex(0)
        self.cur_index = 0
        self.show_photo()
        self.accept_pushButton.clicked.connect(self._accept)
        self.reject_pushButton.clicked.connect(self._reject)
        self.next_pushButton.clicked.connect(self._next)

        QtCore.QMetaObject.connectSlotsByName(CHOOSE_PHOTO)

    def retranslateUi(self, CHOOSE_PHOTO):
        _translate = QtCore.QCoreApplication.translate
        CHOOSE_PHOTO.setWindowTitle(_translate("CHOOSE_PHOTO", "Form"))
        self.label.setText(_translate("CHOOSE_PHOTO", "HI 亲爱的小伙伴 这是你吗？"))
        self.photo.setText(_translate("CHOOSE_PHOTO", "诶，照片不见了"))
        self.next_pushButton.setText(_translate("CHOOSE_PHOTO", "不是我"))
        self.accept_pushButton.setText(_translate("CHOOSE_PHOTO", "是我呀！"))
        self.label_2.setText(_translate("CHOOSE_PHOTO", "很抱歉没有捕捉到你的面孔\n"
" 请再来一次"))
        self.reject_pushButton.setText(_translate("CHOOSE_PHOTO", "我委屈"))

    def show_photo(self):
        top, right, bottom, left = self.photos[self.cur_index]
        face_image = self.image[top-30:bottom+30, left-10:right+10]
        face_image = Image.fromarray(face_image)
        qImg = ImageQt(face_image)
        qpix = QPixmap.fromImage(qImg)
        newpix = QPixmap(qpix.scaled(self.photo.width(),
                                     self.photo.height(),
                                     Qt.KeepAspectRatio))
        self.photo.setPixmap(newpix)  # 显示图片
    def _next(self):
        self.cur_index += 1
        if self.cur_index < len(self.photos):
            self.show_photo()
        else:
            self.stackedWidget.setCurrentIndex(1)
    def _accept(self):
        return self.accept()
    def _reject(self):
        return self.reject()