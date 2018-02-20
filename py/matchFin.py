#!/usr/bin/env python
# -*- coding: utf-8 -*
#################################修改########################3
#就是能不能把指纹录入剥离出来，就是录入和存储、匹配是独立的函数文件
import serial
import time
import re
import serial.tools.list_ports
import os
def getPort():
    port_list = serial.tools.list_ports.comports()
    port = 0
    for ports in port_list:
        if (re.match('/dev/cu.wchusbserial1420', ports.device)):
            port = ports.device
            return port


def matchFP(stu_id):
    port = getPort()

    if (port):
        ser = serial.Serial(port , 9600, timeout=5)
        while (ser.readline().decode('utf-8') != '0\r\n'):     #与下位机握手(串行通信均需双方握手)
            continue
        if ser.writable():      #选择工作模式
            ser.write(b'1')

        #####################文件路径######################
        pwd = os.getcwd()
        file_pwd = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
        file_pwd = file_pwd + '/files/examStudent'
        file_name = file_pwd + '/' + stu_id +'_0.txt'
        print("读文件：", file_name)
        if os.path.exists(file_name):
            fPrint_file = open(file_name, 'r')
        else:
            print("no file")
            return '0'

        for i in range(256):
            s = fPrint_file.readline()
            s = s.replace('0x', '', 1).strip('\n').encode()
            if ser.writable():
                ser.write(s)
        fPrint_file.close()

        #####################能不能在这里加个存储匹配时录入的指纹信息################


        #监听
        circut = True
        while circut:
            if (ser.readable()):
                status = ser.readline().decode('utf-8')
                status = status.strip('\r\n')
                if (re.match('conf', status)):
                    while (not ser.writable()):
                        continue
                    ser.write(b'0')     #退出信号握手
                    return status.replace('conf', '', 1)
                else:
                    if status != '':
                        return status
    else:
        return '3'

