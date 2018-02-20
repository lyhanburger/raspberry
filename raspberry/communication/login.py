#!/usr/bin/python3
import configDB
import server
def loginUserDownload():#OK
	with configDB.configLocalDB() as curLocal:
		with configDB.configServerDB() as curServer:
			print("loginUserDownload")
			curServer.execute('''select * from "user" ''')
			rows = curServer.fetchall()
			curLocal.execute('''delete  from  "user"''')
			for row in rows:
				curLocal.execute('''insert into "user" values %s ''',(row,))
def loginUserLogin(*args):#OK
	with configDB.configLocalDB() as cur:
		print("loginUserLogin")
		cur.execute('''select rights from "user" where id=%s and passwd ='%s' '''%args )
		result = cur.fetchone()
		if result == None:
			return 0
		else:
			return result[0]
def loginUserInsert(*args):#OK
	with configDB.configLocalDB() as cur:
		print("loginUserAdd")
		cur.execute("insert into user_add values('%s','%s',%s,false) on conflict(id) do \
		update set passwd=excluded.passwd, rights=excluded.rights, is_uploaded=excluded.is_uploaded"%args)
def loginUserSelect(view,filter):#OK
	with configDB.configLocalDB() as cur:
		print("loginUserSelect")
		cur.execute("select id from user_add where %s"%filter)
		return cur.fetchone()
def loginUserDelete(*names):#OK
	with configDB.configLocalDB() as cur:
		print("loginUserDelete")
		if(names == None ):
			print("empty input")
		for name in names:
			cur.execute("delete from user_add where id = %s ",(name,))
def loginUserUpload(*user_ids):#OK
	with configDB.configLocalDB() as curLocal:
		with configDB.configServerDB() as curServer:
			print("loginUserUpload")
			if(user_ids == None):
				print("empty input")
			for user_id in user_ids:
				curLocal.execute("select id, passwd, rights from user_add where id = %s",(user_id,))
				row = curLocal.fetchone()
				print(row)
				curServer.execute('''insert into "user" values %s on conflict(id)\
				do update set passwd=excluded.passwd ,rights=excluded.rights ''',(row,))
				curLocal.execute("update user_add set is_uploaded=true where id=%s"%(user_id,))

def loginUserShow():
	with configDB.configLocalDB() as curLocal:
		print("loginUserShow")
		curLocal.execute('''select * from "user" ''')
		rows = curLocal.fetchall()
		return rows

def main():
	#初始化local和server
	server.resetServerDB()
	configDB.resetLocalDB()
	#从Server下载所有的user
	#loginUserDownload()
	#登录并获取该user的rights
	#rights = loginUserLogin("2015211001","raspberry")
	#print("rights = %s"%rights)
	#新增用户(user_id,user_password,user_rights)
	#loginUserInsert("2015211001","raspberry","24")
	#上传用户
	#loginUserUpload(2015211001)
if __name__ == '__main__':
	main()
