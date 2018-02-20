import sys
import os

pwd = os.getcwd()
rasp_pwd = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")

#localProjectDir = "/home/pi/raspberry"
#localProjectDir = "/Users/chenyao/Downloads/raspberry"
localProjectDir = rasp_pwd
localDBHost  = "127.0.0.1"
localDBUser = "pi"
localDBPort = 5432 
localDBName = "raspberry"
localDBPasswd = "raspberry"
#localExamStudentDir = "/home/pi/raspberry/files/examStudent"
#localExamRecordDir ="/home/pi/raspberry/files/examRecord"
#localRegisterStudentDir = "/home/pi/raspberry/files/registerStudent"
#localExamStudentDir = "/Users/chenyao/Downloads/raspberry/files/examStudent"
#localExamRecordDir ="/Users/chenyao/Downloads/raspberry/files/examRecord"
#localRegisterStudentDir = "/Users/chenyao/Downloads/raspberry/files/registerStudent"
localExamStudentDir = rasp_pwd + "/files/examStudent"
localExamRecordDir = rasp_pwd + "/files/examRecord"
localRegisterStudentDir =  rasp_pwd + "/files/registerStudent"
serverProjectDir = "/home/pi/DataEntry"
serverDBHost = "23.105.194.46"
serverDBUser = "pi"
serverDBPasswd = "raspberry"
serverDBPort = 5432
serverDBName = "raspberry"
serverFTPIP = "23.105.194.46"
serverFTPUser = "pi"
serverFTPPasswd = "raspberry"
serverStudentDir = "/home/pi/raspberry/files/student"
serverExamRecordDir = "/home/pi/raspberry/files/examRecord"

sys.path.append(localProjectDir+"/communication")
