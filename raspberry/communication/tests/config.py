import sys
localProjectDir = "/home/pi/raspberry"
localDBHost  = "127.0.0.1"
localDBUser = "pi"
localDBPort = 5432 
localDBName = "raspberry"
localDBPasswd = "raspberry"
localExamStudentDir = "/home/pi/raspberry/files/examStudent"
localExamRecordDir ="/home/pi/raspberry/files/examRecord" 
localRegisterStudentDir = "/home/pi/raspberry/files/registerStudent"
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
