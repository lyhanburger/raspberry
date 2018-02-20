#!/usr/bin/python3
#-*- coding:utf-8 -*-
import configDB
import configFTP
import server
def registerStudentInsert(*args):#stu_id, stu_name, stu_class, finger, face, is_ic
	with configDB.configLocalDB() as cur:#OK
		print("registerStudentInsert")
		cur.execute("insert into register_student(id, name, class, finger, face, is_ic, is_uploaded)\
		values(%s,'%s',%s,%s,%s,%s,false) \
		on conflict(id) do update set name=excluded.name, class=excluded.class,\
		finger=excluded.finger, face=excluded.face, is_ic=excluded.is_ic, \
		is_uploaded=excluded.is_uploaded"%args)
def registerStudentSelect(view,*args):#OK
	with configDB.configLocalDB() as cur:
		print("registerStudentSelect")
		cur.execute("select id from register_student where %s"%sql)
		return cur.fetchone()
def registerStudentDelete(*ids):#OK
	with configDB.configLocalDB() as cur:
		print("registerStudentDelete")
		if(ids == None ):
			print("empty input")
		for id in ids:
			cur.execute("delete from register_student where id=%s"%(id,))
def registerStudentUpload(*ids):
	with configDB.configLocalDB() as curLocal:
		with configDB.configServerDB() as curServer:
			print("registerStudentUpload")
			if(ids == None):
				print("empty input")
			for id  in ids:
				configFTP.registerStudentUploadFiles(id)
				curLocal.execute("select id, name, class, face, finger, is_ic   \
				from register_student where id=%s "%(id,))
				row = curLocal.fetchone()
				curServer.execute("insert into student values %s on conflict(id) do update set\
				name=excluded.name, class=excluded.class, face=excluded.face, \
				finger=excluded.finger, is_ic=excluded.is_ic,time=excluded.time" ,(row,))
				curLocal.execute("update register_student set is_uploaded=true where id=%s"%(id,))
def main():
	#初始化
	server.resetServerDB()
	server.resetServerFiles()
	configDB.resetLocalDB()
	configFTP.resetLocalFiles()
	#模拟生成照片和指纹(stu_id,fingerCnt,faceCnt)
	configFTP.registerStudentCreateFiles(2015211002,1,1)
	#新增记录(			stu_id,stu_name,stu_class,fingerCnt,faceCnt,is_ic)
	registerStudentInsert("2015211002","tesla","2015211101","1","1","True")
	##上传记录和文件
	registerStudentUpload("2015211002")
if __name__ == '__main__':
	main()
