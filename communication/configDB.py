#!/usr/bin/python3
import config
import psycopg2
class configLocalDB():
	def __enter__(self):
		self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s "%(config.localDBName,config.localDBUser,config.localDBHost,config.localDBPasswd,))
		self.cur = self.conn.cursor()
		return self.cur
	def __exit__(self,type,value,traceback):
		self.cur.close()
		self.conn.commit()
		self.conn.close()
class configServerDB():
	def __enter__(self):
		self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s "%(config.serverDBName,config.serverDBUser,config.serverDBHost,config.serverDBPasswd,))
		self.cur = self.conn.cursor()
	#	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE,self.cur)
	#	psycopg2.extensions.set_client_encoding("UTF8")
	#	self.cur.execute("insert into test('好')")
		return self.cur
	def __exit__(self,type,value,traceback):
		self.cur.close()
		self.conn.commit()
		self.conn.close()
def setupLocalDB():
	with configLocalDB() as cur:
		print("setupLocalDB")
		cur.execute('''drop table if exists "user"''')
		cur.execute("drop table if exists user_add")
		cur.execute("drop table if exists register_student")
		cur.execute("drop table if exists speech")
		cur.execute("drop table if exists speech_record")
		cur.execute("drop table if exists exam")
		cur.execute("drop table if exists exam_member")
		cur.execute("drop table if exists exam_student")
		cur.execute("drop table if exists exam_record")


		cur.execute('''create table if not exists "user"(id int primary key, passwd varchar, rights int)''')
		cur.execute("create table if not exists user_add(id int primary key, passwd varchar, rights int, \
		is_uploaded bool default false)") 

		cur.execute("create table if not exists register_student(id int primary key, name varchar, class int, \
		finger int, face int, is_ic bool, is_uploaded bool)")

		cur.execute("create table if not exists exam(id int primary key, name varchar, location varchar, teacher varchar)")
		cur.execute("create table if not exists exam_student( id int primary key, name varchar, class int, \
		finger int, face int)")
		cur.execute("create table if not exists exam_record(exam_id int, stu_id int, finger int, sim_finger int, \
		face int, sim_face int, is_ic bool, is_appended bool default false,\
		is_matched bool default false, is_uploaded bool default false, \
		primary key(exam_id,stu_id) )")
		cur.execute("create table if not exists exam_member(exam_id int, stu_id int, \
		primary key(exam_id, stu_id))" )

		cur.execute("create table if not exists speech(id int  primary key, name varchar, location varchar, is_uploaded bool default false) ")
		cur.execute("create sequence seq_spe maxvalue 100 cycle owned by speech.id")
		cur.execute("create table if not exists speech_id_relation(id_local int, id_server int, primary key(id_local, id_server))")
		cur.execute("create table if not exists speech_record(spe_id int, stu_id int, \
		signin_first bool default false, signin_second bool default false, is_uploaded bool default false, \
		primary key(spe_id, stu_id))")
def setupServerDB():
	with configServerDB() as cur:
		print("setupServerDB")
		cur.execute('''drop table if exists "user"''')
		cur.execute("drop table if exists student")
		cur.execute("drop table if exists speech")
		cur.execute("drop table if exists speech_record")
		cur.execute("drop table if exists exam")
		cur.execute("drop table if exists exam_member")
		cur.execute("drop table if exists exam_record")
		#login
		cur.execute('''create table if not exists "user"(id int  primary key, passwd varchar, rights int)''')
		#student(register&exam&speech)
		cur.execute("create table if not exists student(id int primary key, name varchar, class int, \
		finger int, face int, is_ic bool, time char(16) default to_char(current_timestamp,'YYYY-MM-DD HH:MI'))")
		#exam
		cur.execute("create table if not exists exam(id int primary key, name varchar, location varchar, teacher varchar)")
		cur.execute("create table if not exists exam_record(exam_id int, stu_id int, \
		finger int, sim_finger int, face int, sim_face int,\
		is_ic bool, is_appended bool, is_matched bool,\
		time char(16) default to_char(current_timestamp,'YYYY-MM-DD HH:MI'),\
		primary key(exam_id, stu_id))")
		cur.execute("create table if not exists exam_member(exam_id int, stu_id int,\
		primary key(exam_id, stu_id))" )
		#speech
		cur.execute("create table if not exists speech(id int primary key, name varchar,\
		location varchar, time char(16) default to_char(current_timestamp,'YYYY-MM-DD HH:MI')) ")
		cur.execute("create sequence seq_spe maxvalue 10000 cycle owned by speech.id")
		cur.execute("create table if not exists speech_record(spe_id int, stu_id int, \
		primary key(spe_id, stu_id))")
def preloadServerDB():
	with configServerDB() as cur:
		print("preloadServerDB")
		cur.execute('''insert into  "user" values(2015211001,'raspberry',35)''')#新增User
		cur.execute('''insert into  "user" values(2015211002,'raspberry',24)''')#新增User
		cur.execute("insert into student values(2015211000,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")#新增Student
		cur.execute("insert into student values(2015211001,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")#新增Student
		cur.execute("insert into student values(2015211002,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into student values(2015211003,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into student values(2015211004,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into student values(2015211005,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into student values(2015211006,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into student values(2015211007,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into student values(2015211008,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into student values(2015211009,'Tesla',2015211001,3,3,true,'2017-01-01 15:30')")
		cur.execute("insert into exam values(1,'Game Theory', 'room3','Richard Dawkins')")#新增Exam
		cur.execute("insert into exam values(2,'Game Theory', 'room3','Richard Dawkins')")
		cur.execute("insert into exam values(3,'Game Theory', 'room3','Richard Dawkins')")
		cur.execute("insert into exam_member values(1,2015211000)")#新增 exam_member:每场exam有那些student参加
		cur.execute("insert into exam_member values(1,2015211001)")#新增 exam_member:每场exam有那些student参加
		cur.execute("insert into exam_member values(1,2015211002)")
		cur.execute("insert into exam_member values(1,2015211003)")
		cur.execute("insert into exam_member values(2,2015211004)")
		cur.execute("insert into exam_member values(2,2015211005)")
		cur.execute("insert into exam_member values(2,2015211006)")
		cur.execute("insert into exam_member values(3,2015211007)")
		cur.execute("insert into exam_member values(3,2015211008)")
		cur.execute("insert into exam_member values(3,2015211009)")
def clearLocalDB():
	print('clearLocalDB')
	with configLocalDB() as cur:
		cur.execute("truncate user_add,register_student,exam_student,exam_record,exam_member,exam,speech,\
		speech_record,speech_id_relation,speech")
def resetLocalDB():
	print('resetLocalDB')
	with configLocalDB() as cur:
		cur.execute('truncate "user",user_add,register_student,exam_student,exam_record,exam_member,exam,speech,\
		speech_record,speech_id_relation,speech')
		cur.execute('''insert into "user" values(1111111111,'111111',127)''')	
def main():
	#setupLocalDB()#建立LocalDatabase,清空
	setupServerDB()#建立ServerDatabase,清空
	preloadServerDB()#给Server预装数据
	#clearLocalDB()#清除除了user表中的所有数据
	#resetLocalDB()#清除所有表中的数据
if __name__ == "__main__":
	main()
		
