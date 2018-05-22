import time
#from getFP import *
#from matchFP import *
from idSerial import *
import login

from PyQt5.QtCore import *
from logc import printINFO, printTEST
###########载入指纹模块#########
from recordFP import *
from matchFin import *
##############################

class getstuid(QThread):
    getid = pyqtSignal(str)
    def __init__(self, parent = None):
        super(getstuid, self).__init__(parent)
        self.stuid=''

    def run(self):
        self.getid.emit(self.stuid)

    def setstuid(self,stuid):
        self.stuid=stuid
        self.start()

class finoperation(QThread):
    sinport = pyqtSignal(int,str)
    def __init__(self, parent = None):
        super(finoperation, self).__init__(parent)
        self.choice = -1
        self.stu_id = ''

    def run(self):
        while True:
            #print("choice:",self.choice)
            if self.choice==1:
                time.sleep(3)
                printINFO("Register")
                self.sinport.emit(1,lihaoGetFP())
            elif self.choice==2:
                printINFO("MatchFP")
                self.sinport.emit(2,matchFP())
            else:
                print("do nothing")
        time.sleep(7)

    def setvalue(self,choice,stu_id):
        self.choice = choice
        self.stu_id = stu_id
        self.start()

class idthread(QThread):
    idport = pyqtSignal(int,tuple)
    def __init__(self, parent = None):
        super(idthread, self).__init__(parent)
        self.choice = -1

    def run(self):
        while True:
            if self.choice == -1:
                break
            else:
                Idcard = readID()
                printTEST("idcard:"+str(Idcard))
                if Idcard != '':
                   self.idport.emit(self.choice, Idcard)
            time.sleep(2)

    def setvalue(self, choice):
        self.choice = choice
        self.start()

class upuserthread(QThread):
    def __init__(self, parent = None):
        super(upuserthread, self).__init__(parent)
    def run(self):
        login.loginUserDownload() 
