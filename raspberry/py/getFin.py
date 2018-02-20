#!/usr/bin/env python
# -*- coding: utf-8 -*
import serial
import time
import re
import serial.tools.list_ports

def getPort():
    port_list = serial.tools.list_ports.comports()
    port = 0
    for ports in port_list:
        if (re.match('/dev/cu.wchusbserial1420', ports.device)):
            port = ports.device
            return port
