import time
import login
from PyQt5.QtCore import *
from logc import printINFO, printTEST
# 载入指纹模块 
from finger_modle import enroll, match
# 载入磁卡
from idSerial import *

class getstuid(QThread):
    getid = pyqtSignal(str)
    def __init__(self, parent = None):
        super(getstuid, self).__init__(parent)
        self.stuid=''

    def run(self):
        self.getid.emit(self.stuid)

    def set_stuid(self, stuid):
        self.stuid=stuid

class finoperation(QThread):
    fp_recoder_signal = pyqtSignal(str,bool)
    fp_match_signal = pyqtSignal(tuple)

    def __init__(self, parent = None):
        super(finoperation, self).__init__(parent)
        self.mod = 1
        self.num = '1'

    def run(self):
        while True:
            if self.mod == 1:
                '''record'''
                num = bytes(self.num+'\n', encoding = "utf8")
                print('cur_fp_num:', num)
                result = enroll(num)
                self.fp_recoder_signal.emit(self.num, result)
            else: 
                result = match()
                if result:
                    self.fp_match_signal.emit(result)
                else:
                    self.fp_match_signal.emit((None, None))
            time.sleep(6)

    def setvalue(self, mod = 1, num = '1'):
        self.mod = mod
        self.num = num

class idthread(QThread):
    idport = pyqtSignal(int,tuple)
    def __init__(self, parent = None):
        super(idthread, self).__init__(parent)
        self.choice = -1
        self.is_stop = True

    def run(self):
        while True:
            if self.is_stop:
                print('stop ID thread')
                break
            else:
                Idcard = readID()
                print(Idcard)
                if Idcard != None:
                   self.idport.emit(self.choice, Idcard)
            time.sleep(2)

    def stop(self):
        self.is_stop = True
    def begin(self):
        self.is_stop = False
        self.start()
    def setvalue(self, val):
        self.choice = val


class upuserthread(QThread):
    def __init__(self, parent = None):
        super(upuserthread, self).__init__(parent)
    def run(self):
        login.loginUserDownload() 
