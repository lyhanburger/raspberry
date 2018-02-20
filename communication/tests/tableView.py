#!/usr/bin/python3
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PyQt5.uic import *
import config
import view 
app = QApplication(sys.argv)

if __name__ == '__main__':
	window = view.Window("examRecord")
	window.view.filter('','','','','All','All','All','All','All')
	window.view.hideColumn(0)
	sys.exit(app.exec_())
	
