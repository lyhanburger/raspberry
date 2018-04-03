import serial
import time
import re
import serial.tools.list_ports
import os
FPtimes = 0
def getPort():
    port_list = serial.tools.list_ports.comports()
    port = 0
    for ports in port_list:
        if (re.match('/dev/cu.wchusbserial1420', ports.device)):
            port = ports.device
            return port

def lihaoGetFP():
    global FPtimes
    port = "/dev/ttyUSB0"
    print("getFPport：", port)
    if (port):
        try:
            ser = serial.Serial(port , 9600)
            print("registerXXX")
            time.sleep(2)
            ser.write(b'r')
#            ser.write(b'v')
            ser.write(b'1\n')
            print("lihaoregister") 
        except:
            print("FPNone")
   

       # with open("lihaoFPDict.txt","w")as lihaoFile:
       #     ser.write("\n")
       #     ser.write(str(int(FP_id)+1)+",")
       # with open("lihaoFPDict.txt","r")as lihaoFile:
       #     FP_id,stu_id = lihaoFile.readlines()[-1].strip().split(",")
       #     ser.write("\n")
       #     ser.write(str(int(FP_id)+1)+",") return "returnlihaoregister"
       return '1'
       
    else:
        return '3'
def getFP():

    global FPtimes
    port = getPort()
    print("getFPport：", port)
    if (port):
        ser = serial.Serial(port , 9600, timeout=5)
        while (ser.readline().decode('utf-8') != '0\r\n'):     #与下位机握手(串行通信均需双方握手)
            continue
        if ser.writable():      #选择工作模式
            ser.write(b'0')
        circuit = True  #是否循环读取
        finger = []     #指纹数据
        cnt = 0         #读取指纹数据用计数器
        while (circuit):
            if (ser.readable()):
                status = ser.readline().decode('utf-8')
                status = status.strip('\r\n')       #去尾
                if (status == '1'):
                    FPtimes+=1
                    pwd = os.getcwd()
                    file_pwd = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
                    file_pwd = file_pwd + '/files/registerStudent'
                    file_name =file_pwd + '/unnameFP_'+str(FPtimes)+'.txt'
                    circuit = False
                    cnt = 0
                    fPrint_file = open(file_name,'w')
                    for f in finger:
                        fPrint_file.write(f)
                        fPrint_file.write('\n')
                    fPrint_file.close()
                    while (not ser.writable()):
                        continue
                    ser.write(b'0')     #退出信号握手
                    return status
                elif (re.match('0x', status)):      #匹配字符
                    finger.append(status)
                    cnt += 1
                else:
                    if len(status) > 0:     #readline()即便是空行也会读取
                        return status
    else:
        return '3'

def main():
    print(getFP())
if __name__== '__main__':
    main()
