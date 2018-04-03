import serial
import serial.tools.list_ports
import re

def getPort():
    try:
        port_list = serial.tools.list_ports.comports()
    except:
        print("IDNONE")
    port = 0
    for ports in port_list:
        if (re.match('/dev/ttyUSB0', ports.device)):
            port = ports.device
            return port

def readID():
    port  = getPort()
    print("port----",port)
    try:
        ser = serial.Serial(port, 9600, timeout=1)
    except:
        print("IDNONE")
    idNum = ""
    while (len(idNum) == 0):
        try:
            idNum = (ser.readline()).decode('utf-8')  # 原始串口数据为bytes，需解码成str(utf-8)
        except:
            print("IDNONE")
    # print("idnum--",idNum)
    return idNum

def main():
    print(readID())
if __name__== '__main__':
    main()
