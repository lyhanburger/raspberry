#!/usr/bin/python3
import config
import configDB
import configFTP
def loginUserInsert(id,passwd,rights):
	with configDB.configServerDB() as cur:
		print('server.loginUserInsert')
		cur.execute('''insert into "user"(id,passwd,rights) values({0},'{1}',{2}) \
		on conflict(id) do  update set\
		passwd = excluded.passwd, rights = excluded.rights'''.format(id,passwd,rights))
def examStudentInsert(id,name,class_,finger,face,is_ic):
	with configDB.configServerDB() as cur:
		print('server.examStudentInsert')
		cur.execute("insert into student(id,name,class,finger,face,is_ic) \
		values({0},'{1}',{2},{3},{4},{5})\
		on conflict(id) do update set\
		name = excluded.name, class = excluded.class, finger = excluded.finger,\
		face = excluded.face, is_ic = excluded.is_ic".format(id,name,class_,finger,face,is_ic))
def examExamInsert(id,name,location,teacher):
	with configDB.configServerDB() as cur:
		print('server.examExamInsert')
		cur.execute("insert into exam(id,name,location,teacher) values({0},'{1}','{2}','{3}')\
		on conflict(id) do update set\
		name = excluded.name, location = excluded.location, teacher = excluded.teacher".format(id,name,location,teacher))
def examMemberInsert(exam_id,stu_id):
	with configDB.configServerDB() as cur:
		print('server.examMemberInsert')
		cur.execute("insert into exam_member(exam_id,stu_id) values({0},{1})\
		on conflict(exam_id,stu_id) do nothing".format(exam_id,stu_id))
def resetServerDB():
	print('resetServerDB')
	with configDB.configServerDB() as cur:
		cur.execute('''truncate "user",student,exam,exam_member,exam_record,speech,speech_record''')
		cur.execute('''insert into "user" values(1111111111,'111111',127)''')
def resetServerFiles():
	print('resetServerFiles')
	with configFTP.configFTP() as ftp:
		dir_student = config.serverStudentDir
		for file in ftp.nlst(dir_student):
			print(file)
			ftp.delete(file)
		dir_examRecord = config.serverExamRecordDir
		for exam in ftp.nlst(dir_examRecord):
			for file in ftp.nlst(exam):
				ftp.delete(file)
			ftp.rmd(exam)

def main():
	resetServerFiles()
#	loginUserInsert(1111111111,'111111',127)	
#	loginUserInsert(2015211001,'raspberry',35)	
#	examStudentInsert(2015210001,'Tesla',2015211001,1,1,"True")
#	examExamInsert(1,"GameTheory","3-333","Tom")
#	examMemberInsert(1,2015210001)
if __name__ == '__main__':
	main()
