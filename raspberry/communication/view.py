#!/usr/bin/python3
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5 import QtWidgets
import config
import configDB,configFTP
import speech,exam,register
import numpy
import sys
import login
import random
import server
def transFilterWords(*args):#将All,True,False转换为能够嵌套到sql中的语句,将空字符串换位任意值来匹配正则表达式
	dic = {
		'All':' is not null',
		'True':'=true',
		'False':'=false',
		}	
	args = list(args)
	for aNo,arg in enumerate(args):
		if arg in dic:
			args[aNo]=dic[arg]
		else:
			args[aNo]=arg
	return tuple(args)
def getQueryLoginUser():
	filter = 'select id, rights from "user"'
	return filter
def getQueryLoginUserAdd(*args):
	filter = "select id, rights is_uploaded from user_add where to_char(rights,'9999999999')~'.*%s'"%args
	return filter
def getQueryRegisterStudent(*args):#stu_id, stu_name, stu_class, has_finger, has_face
	filter = "select id, name, class, finger, face, is_ic, is_uploaded \
	from register_student where to_char(id,'9999999999') ~'.*%s' and\
	name ~'.*%s' and to_char(class,'9999999999') ~'.*%s' and\
	bool(finger) %s and bool(face) %s "%transFilterWords(*args)
	return filter
def getQueryExamExamServer(exam_id,exam_name,location,teacher,exam_ids_local):
	if len(exam_ids_local) == 1:
		filter = "select id, name,location, teacher, id = %s as is_downloaded from exam where \
		to_char(id,'9999999999')~'%s' and name~'.*%s' and \
		location~'.*%s' and teacher ~'.*%s'"%transFilterWords(exam_ids_local[0],exam_id,exam_name,location,teacher)
	elif len(exam_ids_local) ==0:
		filter = "select id, name, location, teacher, false as is_downloaded from exam where \
		to_char(id,'9999999999')~'%s' and name~'.*%s' and \
		location~'.*%s' and teacher ~'.*%s'"%transFilterWords(exam_id,exam_name,location,teacher)
	else:
		filter = "select id, name,location, teacher, id in %s as is_downloaded from exam where \
		to_char(id,'9999999999')~'%s' and name~'.*%s'\
		and location~'.*%s' and teacher ~'.*%s'"%transFilterWords(exam_ids_local,exam_id,exam_name,location,teacher)
	return filter
def getKeysExamExamLocal():
	with configDB.configLocalDB() as cur:
		cur.execute("select id from exam")
		results = numpy.array(cur.fetchall())
		if len(results) == 0:
			return () 
		keys = results[:,0]
		return tuple(keys)
def getQueryExamExamLocal(*args):#exam_id, exam_name,location, teacher
	filter = "select id, name,location, teacher from exam where \
	to_char(id,'9999999999')~'%s' and name~'.*%s' and location~'.*%s' and teacher ~'.*%s'"%transFilterWords(*args)
	return filter
def getQueryExamRecord(*args):#exam_id, stu_id, stu_name, stu_class, has_finger,  has_face,is_ic,  is_matched, is_appended 
	filter = "select exam_id, stu_id, name, class,\
	exam_record.finger,exam_record.sim_finger,\
	exam_record.face,exam_record.sim_face,\
	exam_record.is_ic, exam_record.is_matched, exam_record.is_appended,\
	exam_record.is_uploaded from exam_record,exam_student \
	where exam_record.stu_id = exam_student.id and \
	to_char(exam_id,'9999999999')~'%s' and	to_char(stu_id, '9999999999')~'.*%s'  and \
	name ~'.*%s' and to_char(class,'9999999999')~'.*%s' and\
	bool(exam_record.finger) %s and bool(exam_record.face) %s and\
	is_ic %s and is_matched %s and is_appended %s"%transFilterWords(*args)
	return filter
def getQuerySpeechSpeech(*args):#spe_id, name, location, 
	filter = "select id,name, location, is_uploaded from speech where name~'.*%s'"%args
	return filter
def getQuerySpeechRecord(*args):#spe_id, stu_id	
	filter = "select spe_id, speech.name,  stu_id,signin_first, signin_second, speech_record.is_uploaded from speech_record,speech where to_char(spe_id,'9999999999')~'.*%s' and \
	to_char(stu_id,'9999999999')~'.*%s'"%args
	return filter

viewNames = (	"loginUserAdd","loginUser","registerStudent",\
				"examExamServer","examExamLocal", \
				"examRecord", "speechSpeech", "speechRecord")
getQuerys = (	getQueryLoginUserAdd, getQueryLoginUser, getQueryRegisterStudent,\
				getQueryExamExamServer, getQueryExamExamLocal,\
				getQueryExamRecord, getQuerySpeechSpeech, getQuerySpeechRecord)
keyColumns = (
				(0,),(0,),(0,),\
				(0,),(0,),
				(0,1),(0,),(0,1),
)
class View(QtWidgets.QTableView):
	def __init__(self,name, parent=None):
		QtWidgets.QTableView.__init__(self,parent)
		#设置所有表的基本信息
		getDBs = (self.getLocalDB,self.getLocalDB, self.getLocalDB\
					,self.getServerDB,self.getLocalDB,\
					self.getLocalDB,self.getLocalDB,self.getLocalDB)
		#建立基本结构
		self.viewId = viewNames.index(name)
		self.db = getDBs[self.viewId](name)
		self.model = QSqlTableModel(self, self.db)
		self.setModel(self.model)
		self.show()
		print(self.model.lastError().text())
		#添加属性
		self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
	def getKeys(self):
		indexs = self.selectedIndexes()
		rowCnt = int(len(indexs)/self.model.columnCount())
		indexs = numpy.array(indexs).reshape(rowCnt,self.model.columnCount())
		values = []
		values_temp = []
		for index in indexs:
			values_temp = []
			for keyColumn in keyColumns[self.viewId]:
				values_temp.append(self.model.data(index[keyColumn]))
			if len(keyColumns[self.viewId])==1:values.append(values_temp[0])
			else:values.append(tuple(values_temp))
		return tuple(values)
	def filter(self,*args):
		if self.viewId == 3:
			#如果是examExamServer的话,为了添加is_download,必须把本地exam的ids作为形参输入	
			keys = getKeysExamExamLocal()
			args = list(args)
			args.append(keys)
		self.query = QSqlQuery(getQuerys[self.viewId](*args),self.db)
		self.model.setQuery(self.query)
		print(self.model.lastError().text())
		self.update()
	def getLocalDB(self, dbName):
		db = QSqlDatabase.addDatabase("QPSQL",dbName+'%f'%random.random())
		#db = QSqlDatabase.addDatabase("QPSQL",dbName)
		db.setHostName(config.localDBHost)
		db.setPort(config.localDBPort)
		db.setDatabaseName(config.localDBName)
		db.setUserName(config.localDBUser)
		db.setPassword(config.localDBPasswd)
		if (db.open() == False):
			QtWidgets.QMessageBox.critical(None, "Database Error", db.lastError().text())
		return db
	def getServerDB(self, dbName):
		db = QSqlDatabase.addDatabase("QPSQL",dbName)
		db.setHostName(config.serverDBHost)
		db.setPort(config.serverDBPort)
		db.setDatabaseName(config.serverDBName)
		db.setUserName(config.serverDBUser)
		db.setPassword(config.serverDBPasswd)
		if (db.open() == False):
			QtWidgets.QMessageBox.critical(None, "Database Error", db.lastError().text())
		return db
class Window(QtWidgets.QWidget):
	def __init__(self,name):
		super(Window, self).__init__()
		self.view = View(name)
		self.btns = [QtWidgets.QPushButton(name) for name in ("Update","Print")]
		self.btnEvents = [self.btnEventUpload, self.btnEventPrint]
		layoutBtns = QtWidgets.QHBoxLayout()
		for i in range(len(self.btns)) :
			self.btns[i].clicked.connect(self.btnEvents[i])
			layoutBtns.addWidget(self.btns[i])
		layoutGlobal = QtWidgets.QVBoxLayout()
		layoutGlobal.addWidget(self.view)
		layoutGlobal.addLayout(layoutBtns)
		self.setLayout(layoutGlobal)
		self.show()
	def btnEventUpload(self):
		print("btnEventUpload")
		#self.view.setColumnHidden(1,True)
		self.view.update()
	def btnEventPrint(self):
		print("btnEventPrint")
		keys = self.view.getKeys()
		print(keys)
		#exam.examRecordUpload(*keys)
		#self.view.filter('','2015','','','All','All','All','All','All')
		login.loginUserDownload()
		self.view.filter()
		self.view.update()
		print('OK')
		

def main():
	app = QtWidgets.QApplication(sys.argv)
	#初始化,排除干扰
	#server.resetServerDB()
	#server.resetServerFiles()
	#configDB.resetLocalDB()
	#configFTP.resetLocalFiles()
	##预装数据
#	configFTP.registerStudentCreateFiles(2015210001,1,1)
#	register.registerStudentInsert(2015210001,'Student',2015211001,1,1,'True')
#	register.registerStudentUpload(2015210001)
#
#	server.examExamInsert(1,'Math','room','Jack')
#	server.examMemberInsert(1,2015210001)
#	exam.examExamDownload(1)
#	exam.examStudentDownload(1)
#	exam.examMemberDownload(1)
#
#	configFTP.examRecordCreateFiles(1,2015210001,1,2)
#	exam.examRecordInsert(1,2015210001,1,80,2,90,'True','False','True')
#用View类即可,初始化的时候里面记得写上模式名称,可用的模式名称如下就是实例中的这几个,有些可能用不上
#可用的函数有:
#	filter(*args):按照规定的顺序将关键字放进去,自动查询并且更新
#	update():数据刷新
#	getKeys():返回选中行的主键
#Note!!!:bool型的输入值只能为("All","True","False")中的值,
#		int类型可以输入int,也可以用字符串形式输入,func("123")和func(123)都是可以的
#		除了bool型,只要输入空字符串'',那么就代表该选项不作为筛选,可以查到所有值
#		对于spe_id和exam_id 输入"123"只可能查到"123",不可能查到"1234",既精确查询
#		对于stu_id和class 输入"2015"能够查到"201521101"等,既模糊查询
#	view = View("loginUser")
#	view.filter()
#	login.loginUserInsert('2','2','35')	
#	login.loginUserInsert('3','3','24')	
#	view = View("loginUserAdd")
#	view.filter(35)#查询权限为35的新增用户(user_add中的)
#	view = View("examExamServer")
#	view.filter('','','','')
#	view = View("examExamLocal")
#	view.filter('','','','')
#	view = View("examRecord")
#	view.filter('','.*2015','','','All','All','All','All','All')
#	view = View("registerStudent")
#	view.filter('','','','All','All')
#	view = View("speechSpeech")
#	view.filter('')
#	view = View("speechRecord")
#	view.filter('','')

#为了方便测试update()和getKeys()函数,可以用Window类进行测试
	window = Window("loginUser")
	window.view.filter()
#	window = Window("loginUserAdd")
#	window.view.filter(35)#查询权限为35的新增用户(user_add中的)
#	window = Window("examExamServer")
#	window.view.filter('','','','')
#	window = Window("examExamLocal")
#	window.view.filter('','','','')
#	window = Window("examRecord")
#	window.view.filter('','2015','','','All','All','All','All','All')
#	window = Window("registerStudent")
#	window.view.filter('','','','All','All')
#	window = Window("speechSpeech")
#	window.view.filter('')
#	window = Window("speechRecord")
#	window.view.filter('','')
#
#	window.view.filter(1,"2015","T","2015","True","True","True","False","False")
#	view = View("loginUserAdd")
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
