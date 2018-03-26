# -*- coding: utf-8 -*-
import sys
sys.path.append("/home/pi/raspberry/communication")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Setdevice import *
import loginImg_rc
import config
import psycopg2

class Ui_login(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.idcardthread=idthread()
        self.idcardthread.idport.connect(self.receiveid)
        self.idcardthread.setvalue(1)
        self.setObjectName("login")
        self.resize(400, 300)
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 401, 301))
        #qss样式
        self.stackedWidget.setStyleSheet("QWidget{\n"
"background-color: rgb(236,240,245);\n"

"color:rgb(98, 99, 99);\n"
"}\n"
"\n"
"QMessageBox{\n"
"background-color: rgb(236,240,245);\n"
"color:rgb(98, 99, 99);\n"
"}\n"
"QPushButton#login_buttn,\n"
"QPushButton#back_buttn,\n"
"QPushButton#NoCard_buttn\n"
"{\n"
"    color:white;\n"
"    background-color:rgb(14 , 150 , 254);\n"
"    border-radius:4px;\n"
"    min-width: 90px;\n"
"    max-width: 90px;\n"
"    min-height: 25px;\n"
"    max-height: 25px;\n"
"}\n"
"QPushButton#mini_buttn,\n"
"QPushButton#close_buttn,\n"
"QPushButton#close_buttn1,\n"
"QPushButton#mini_buttn1\n"
"{\n"
"    background-color:rgb(200, 200, 200,40);\n"
"    border:none;\n"
"    min-width: 21px;\n"
"    max-width: 21px;\n"
"    min-height: 21px;\n"
"    max-height: 21px;\n"
"}\n"
"QPushButton#mini_buttn,\n"
"QPushButton#mini_buttn1\n"
"{\n"
"    background-image:url(./img/mini.png);\n"
"}\n"
"QPushButton#close_buttn,\n"
"QPushButton#close_buttn1\n"
"{\n"
"    background-image:url(./img/close.png);\n"
"}\n"
"QPushButton#mini_buttn:hover,\n"
"QPushButton#mini_buttn1:hover\n"
"{\n"
"    background-color:rgb(236,240,245);\n"
"}\n"
"QPushButton#close_buttn:hover,\n"
"QPushButton#close_buttn1:hover\n"
"{\n"
"    background-color:rgb(255,0,0,70);\n"
"}\n"
"QPushButton#login_buttn:hover,\n"
"QPushButton#back_buttn:hover,\n"
"QPushButton#NoCard_buttn:hover\n"
"{\n"
"    color:white;\n"
"    background-color:rgb(44 , 137 , 255);\n"
"    border:0px;\n"
"}\n"
"\n"
"QPushButton:selected\n"
"{\n"
"    color:white;\n"
"    background-color:rgb(14 , 135 , 228);\n"
"    padding-left:3px;\n"
"    padding-top:3px;\n"
"}\n"
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
"}"

)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.NoCard_buttn = QtWidgets.QPushButton(self.page_2)
        self.NoCard_buttn.setGeometry(QtCore.QRect(260, 250, 90, 25))
        self.NoCard_buttn.setObjectName("NoCard_buttn")
        self.Card_label = QtWidgets.QLabel(self.page_2)
        self.Card_label.setGeometry(QtCore.QRect(60, 50, 281, 181))
        self.Card_label.setTextFormat(QtCore.Qt.AutoText)
        self.Card_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Card_label.setObjectName("Card_label")
        self.close_buttn1 = QtWidgets.QPushButton(self.page_2)
        self.close_buttn1.setGeometry(QtCore.QRect(3, 3, 23, 23))
        self.close_buttn1.setObjectName("close_buttn1")
        self.mini_buttn1 = QtWidgets.QPushButton(self.page_2)
        self.mini_buttn1.setGeometry(QtCore.QRect(24, 3, 23, 23))
        self.mini_buttn1.setObjectName("mini_buttn1")
        self.stackedWidget.addWidget(self.page_2)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayoutWidget = QtWidgets.QWidget(self.page)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 251))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(11)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.user_name = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.user_name.setFont(font)
        self.user_name.setAlignment(QtCore.Qt.AlignCenter)
        self.user_name.setObjectName("user_name")
        self.gridLayout.addWidget(self.user_name, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.uname_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.uname_edit.setObjectName("uname_edit")
        self.gridLayout.addWidget(self.uname_edit, 2, 2, 1, 1)
        self.user_passwd = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.user_passwd.setFont(font)
        self.user_passwd.setObjectName("user_passwd")
        self.gridLayout.addWidget(self.user_passwd, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 3, 1, 1)
        self.upasswd_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.upasswd_edit.setInputMethodHints(
            QtCore.Qt.ImhHiddenText | QtCore.Qt.ImhNoAutoUppercase | QtCore.Qt.ImhNoPredictiveText | QtCore.Qt.ImhSensitiveData)
        self.upasswd_edit.setText("")
        self.upasswd_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.upasswd_edit.setObjectName("upasswd_edit")
        self.gridLayout.addWidget(self.upasswd_edit, 3, 2, 1, 1)
        self.frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.title = QtWidgets.QLabel(self.frame)
        self.title.setGeometry(QtCore.QRect(0, 0, 399, 185))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.close_buttn = QtWidgets.QPushButton(self.frame)
        self.close_buttn.setGeometry(QtCore.QRect(3, 3, 23, 23))
        self.close_buttn.setObjectName("close_buttn")
        self.mini_buttn = QtWidgets.QPushButton(self.frame)
        self.mini_buttn.setGeometry(QtCore.QRect(24, 3, 23, 23))
        self.mini_buttn.setObjectName("mini_buttn")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 4)
        self.gridLayout.setRowStretch(0, 5)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.page)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 260, 301, 40))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.back_buttn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.back_buttn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.back_buttn.setObjectName("back_buttn")
        self.horizontalLayout.addWidget(self.back_buttn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.login_buttn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.login_buttn.setFont(font)
        self.login_buttn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.login_buttn.setObjectName("login_buttn")
        self.horizontalLayout.addWidget(self.login_buttn)
        self.stackedWidget.addWidget(self.page)

        ####################################################
        self.setWindowFlags(Qt.FramelessWindowHint)#消除边框#
        ####################################################

        self.retranslateUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.Card_label.setPixmap(QPixmap("./img/login_card.png"))
        self.NoCard_buttn.clicked.connect(self.input_loginshow)
        self.back_buttn.clicked.connect(self.card_loginshow)
        self.login_buttn.clicked.connect(self.startlogin)
        self.mini_buttn.clicked.connect(self.minimize)
        self.mini_buttn1.clicked.connect(self.minimize)
        self.close_buttn.clicked.connect(self.close)
        self.close_buttn1.clicked.connect(self.close)
        self.login_buttn.setShortcut(Qt.Key_Return)# 将字母区回车键与登录按钮绑定在一起

        self.uname_edit.setPlaceholderText("请输入您的教职工号")
        self.upasswd_edit.setPlaceholderText("请输入您的密码")
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "Dialog"))
        self.NoCard_buttn.setText(_translate("login", "无职工卡"))
        self.Card_label.setText(_translate("login", "请刷卡"))
        self.user_name.setText(_translate("login", "用户名"))
        self.user_passwd.setText(_translate("login", "密    码"))
        self.title.setText(_translate("login", "用户登陆"))
        self.back_buttn.setText(_translate("login", "返回刷卡"))
        self.login_buttn.setText(_translate("login", "确认登陆"))

    def receiveid(self):
        self.idcardthread.setvalue(0)
        self.mode = setdevice(127)
        self.mode.setVisible(1)
        self.mode.setWindowTitle("欢迎使用")

        self.close()

    def card_loginshow(self):
        self.stackedWidget.setCurrentIndex(0)

    def input_loginshow(self):
        self.stackedWidget.setCurrentIndex(1)
        print("ts et")
        login_gif=QMovie("./img/login.gif")
        self.title.setMovie(login_gif)
        login_gif.start()

    def minimize(self):
        self.setWindowState(Qt.WindowMinimized)

    #############################无标签栏下的拖动窗口##################################
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()


    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


    def startlogin(self):
        self.mode = setdevice(127)
        self.mode.setVisible(1)
        self.mode.setWindowTitle("欢迎使用")
        self.close()
        '''
        if not self.uname_edit.text():
            QMessageBox.information(self, "错误", '请输入用户名', QMessageBox.Ok)
        else:
            if not self.upasswd_edit.text():
                QMessageBox.critical(self, "错误", '请输入密码', QMessageBox.Ok)
            else:
                ##########测试###########
                #############连接数据库##############
                #                                 #
                #                                 #
                ###################################
                id = self.uname_edit.text()
                if not id.isdigit():
                    QMessageBox.critical(self.login_buttn, "错误", '错误的用户名')
                else:
                    db = psycopg2.connect("dbname=%s user=%s host=%s password=%s " % (
                        config.localDBName, config.localDBUser, config.localDBHost, config.localDBPasswd))
                    # set_client_encoding("UTF8")
                    self.cursor = db.cursor()
                    id = self.uname_edit.text()
                    passwd = self.upasswd_edit.text()
                    if not id.isdigit():
                        QMessageBox.critical(self.login_buttn, "错误", '错误的用户名')
                    else:
                        ##########
                        result = self.cursor.rowcount
                        # print(result)
                        if (result == 1):
                            rights = (self.cursor.fetchone())[0]  # 从数据库中获取权限
                            ########日志文件写入########
                            userstr = 'user:' + id + ' password:' + passwd + ' rights:' + str(rights)
                            wlogfile(userstr)

                            self.mode = setdevice(rights)
                            self.mode.setVisible(1)
                            self.mode.setWindowTitle("欢迎使用")
                            self.close()

                        else:
                            QMessageBox.critical(self.login_buttn, "错误", '用户名或密码错误')

'''
#self.cursor.execute('''select rights from "user" where id=%s and passwd='%s' ''' % (id, passwd))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    login = Ui_login()
    login.show()
    login.setWindowTitle("登录")
    sys.exit(app.exec_())
