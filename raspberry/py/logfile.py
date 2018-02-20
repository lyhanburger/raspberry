# -*- coding: UTF-8 -*-
import datetime
import os
import re


def wlogfile(str):
    pwd = os.getcwd() #当前文件路径
    father_pwd = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    os.chdir(father_pwd)
    os.getcwd()
    fp = open('logfile.log','a')
    str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' -l ' + str +'\n'
    #print(str) #测试
    fp.write(str)
    fp.close()
    os.chdir(pwd)
    os.getcwd()

def rlogfile():
    pwd = os.getcwd()  # 当前文件路径
    father_pwd = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    os.chdir(father_pwd)
    os.getcwd()
    fp = open('logfile.log', 'r')
    str = fp.read()
    fp.close()
    os.chdir(pwd)
    os.getcwd()
    return str