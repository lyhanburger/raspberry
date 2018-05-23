import serial
import serial.tools.list_ports
import re
import time
def getPort():
    try:
        port_list = serial.tools.list_ports.comports()
    except:
        pass
        # print("IDNONE")
    port = 0
    for ports in port_list:
        if (re.match('/dev/ttyUSB1', ports.device)):
            port = ports.device
            return port

def enroll(type):
    port = getPort()
    print("fingerpoint", port)
    try:
        ser = serial.Serial(port, 9600, timeout=None)
    except:
        print("[1]finger export error")
        return False
    try:
        time.sleep(2)
        ser.write(b'1\n')
        time.sleep(1)
        ser.write(type)
    except:
        print("[2]finger export error")
        return False
    res = ""
    while True:
        res = (ser.readline()).decode('utf-8')
        print(res)
        if res.find("Stored!") != -1:
            return True
        elif res.find("Fingerprints did not match") != -1:
            ser.write(b'1\n')
            ser.write(type)




def match():
    port = getPort()
    print("enroll fingerpoint", port)
    try:
        ser = serial.Serial(port, 9600, timeout=None)
    except:
        print("[1]finger export error")
    # try:
    time.sleep(2)
    ser.write(b'2\n')
    # except:
    # print("[2]finger export error")
    res = ""
    while True:
        res = (ser.readline()).decode('utf-8')
        print(res)
        if res.find("Found ID #") != -1:
            a = res.find("with")
            b = res.find("of")
            ID = res[10:a - 1]
            confidence = res[b + 2:-2]
            result = (ID, confidence)
            print(result)
            return result
        else:
            return None


def main():
    match()
    # enroll(b'5\n')

