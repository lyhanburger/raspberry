import serial
from datetime import datetime

def getPort():
    port_list = serial.tools.list_ports.comports()
    port = 0
    for ports in port_list:
        if (re.match('/dev/cu.wchusbserial', ports.device)):
            port = ports.device
            return port

def readID():
    port = getPort()
    ser = serial.Serial(port, 9600, timeout=1)
    currTime = (datetime.now()).timestamp() #转换当前时间为stamp时间
    delayTime = currTime + 15
    idNum = "0"
    while currTime <= delayTime:
        if ser.readable():
            idNum = (ser.readline()).decode('utf-8')      #原始串口数据为bytes，需解码成str(utf-8)
            print(type(idNum))
            break
        currTime = (datetime.now()).timestamp()
    return idNum


