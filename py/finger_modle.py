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
        print('FP prots.device', ports.device)
        if (re.match('/dev/ttyUSB0', ports.device)):
            port = ports.device
            return port

class FP:
    def __init__(self):
        self.port = getPort()
        print("fingerpoint", self.port)
        try:
            self.ser = serial.Serial(self.port, 9600, timeout=None)
        except:
            print('ERROR PORT')

    def enroll(self, type):

        # self.port = getPort()
        # print("fingerpoint", self.port)
        # try:
        #     self.ser = serial.Serial(self.port, 9600, timeout=1)
        # except:
        #     print('ERROR PORT')
        try:
            time.sleep(1)
            self.ser.write(b'1\n')
            time.sleep(1)
            self.ser.write(type)
        except:
            print("[2]finger export error")
        res = ""
        while True:
            res = (self.ser.readline()).decode('utf-8')
            print(res)
            # time.sleep(2)
            # if res.find(".")!=-1:
            #     break
            if res.find("Stored!") != -1:
                # self.ser.close()
                return True
            elif res.find("[py]") != -1:
                return False
            # elif res.find("Fingerprints did not match") != -1:
            #     self.ser.write(b'1\n')
            #     self.ser.write(type)
        return False

    def match(self):
        # self.port = getPort()
        # print("fingerpoint", self.port)
        # # if self.ser.isOpen():
        # #     self.ser.close()
        # try:
        #     self.ser = serial.Serial(self.port, 9600, timeout=1)
        # except:
        #     print('ERROR PORT') 
        time.sleep(1)
        self.ser.write(b'2\n')
        res = ""
        while True:
            try:
                res = (self.ser.readline()).decode('utf-8')
            except:
                pass
            print(res)
            # time.sleep(2)
            # if len(res)==0:
            #     break
            if res.find("Found ID #") != -1:
                a = res.find("with")
                b = res.find("of")
                ID = res[10:a - 1]
                confidence = res[b + 2:-2]
                result = (ID, confidence)
                print(result)
                # self.ser.close()
                return result
            elif res.find("Not match") != -1:
                return  None, None
        return None, None


