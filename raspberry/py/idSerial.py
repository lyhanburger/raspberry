import serial
import serial.tools.list_ports
import re

def getPort():
    port_list = serial.tools.list_ports.comports()
    port = 0
    for ports in port_list:
        if (re.match('/dev/ttyUSB0', ports.device)):
            port = ports.device
            return port

def readID():
    port  = getPort()
    print("port----",port)
    ser = serial.Serial(port, 9600, timeout=1)
    idNum = ""
    while (len(idNum) == 0):
        idNum = (ser.readline()).decode('utf-8')  # 原始串口数据为bytes，需解码成str(utf-8)

    print("idnum--",idNum)
    return idNum

def main():
    print(readID())
if __name__== '__main__':
    main()
