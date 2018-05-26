import serial
import serial.tools.list_ports
import re
info = {}
info['D5 25 03 46'] = ('Robert', '201521112', '2015212310')  # admin
info['B3 6F 56 3E'] = ('Lily', '2015211102', '2015210012')  # student
info['B3 1A FB FE'] = ('Bob', '2015211123', '2015312201')  # register


def getPort():
    try:
        port_list = serial.tools.list_ports.comports()
    except:
        pass
        # print("IDNONE")
    port = None
    for ports in port_list:
        print(ports.device)
        if (re.match('/dev/ttyUSB1', ports.device)):
            port = ports.device
            break
    return port

def readID():
    port = getPort()
    print("id port:", port)
    if port == None:
        return None
    try:
        ser = serial.Serial(port, 9600, timeout=1)
    except:
        print("[1]id export error")
    idNum = ""
    while (len(idNum) == 0):
        try:
            # time.sleep(2)
            # 原始串口数据为bytes，需解码成str(utf-8)
            idNum = (ser.readline()).decode('utf-8')
        except:
            print("[2] id export error")

    print("idnum--[", str(idNum)[:-2], "]")
    if str(idNum)[:-2] in info.keys():
        return info[str(idNum)[:-2]]
    else:
        return ('UNKNOW', '000', '000')

def main():
    print(readID())

if __name__ == '__main__':
    main()
