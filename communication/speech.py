#!/usr/bin/python3
import configDB
import server
def speechSpeechInsert(*args):
	with configDB.configLocalDB() as cur:
		print("speechSpeechInsert")
		cur.execute("insert into speech values(nextval('seq_spe'), '%s','%s')"%args)
		cur.execute("select lastval() from speech")
		spe_id_local = cur.fetchone()[0]
	return spe_id_local
def speechSpeechDelete(*spe_id_locals):
	with configDB.configLocalDB() as cur:
		for spe_id_local in spe_id_locals:
			cur.execute("delete from speech where id =%s",(spe_id_local,))
def speechSpeechUpload(*spe_id_locals):
	with configDB.configLocalDB() as curLocal:
		with configDB.configServerDB() as curServer:
			print("speechSpeechUpload")
			for spe_id_local in spe_id_locals:
				curLocal.execute("select name,  location from speech where id=%s",(spe_id_local,))
				row = curLocal.fetchone()
				curServer.execute("insert into speech values \
				(nextval('seq_spe'),%s,%s,to_char(current_timestamp,'YYYY-MM-DD HH:MI'))",row)
				curServer.execute("select lastval() from speech")
				spe_id_server = curServer.fetchone()[0]
				curLocal.execute("insert into speech_id_relation values(%s,%s)\
				on conflict(id_local, id_server) do nothing"%(spe_id_local,spe_id_server))
				curLocal.execute("update speech set is_uploaded=true where id={0}".format(spe_id_local))
def speechRecordInsertFirst(*args):
	with configDB.configLocalDB() as cur:
		print("speechRecordInsertFirst")
		cur.execute("insert into speech_record(spe_id, stu_id, signin_first) values (%s,%s,true) on conflict(spe_id, stu_id) \
		do update set signin_first=excluded.signin_first"%args)
def speechRecordInsertSecond(*args):
	with configDB.configLocalDB() as cur:
		print("speechRecordInsertSecond")
		cur.execute("insert into speech_record (spe_id, stu_id, signin_second) values(%s,%s,true) \
		on conflict(spe_id,stu_id) do update \
		set  signin_second=excluded.signin_second"%args)
def speechRecordUpload(*spe_id_locals):
	with configDB.configLocalDB() as curLocal:
		with configDB.configServerDB() as curServer:
			print("speechRecordUpload")
			print(spe_id_locals)
			for spe_id_local in spe_id_locals:
				curLocal.execute("select id_server from speech_id_relation where id_local=%s"%(spe_id_local,))
				spe_id_server = curLocal.fetchone()[0]
				curLocal.execute("select stu_id from speech_record where signin_first=true and signin_second=true\
				and spe_id=%s"%(spe_id_local,))
				stu_ids = curLocal.fetchall()
				for stu_id in stu_ids:
					curServer.execute("insert into speech_record values(%s,%s) \
					on conflict(spe_id,stu_id) do nothing",(spe_id_server,stu_id[0]))
					curLocal.execute("update speech_record set is_uploaded=true where spe_id=%s and stu_id=%s"%(spe_id_local,stu_id[0]))
				curLocal.execute("update speech set  is_uploaded=true where id = %s"%(spe_id_local,))
def main():
	#初始化
	server.resetServerDB()
	configDB.resetLocalDB()
	#本地创建3个speech,并且获取本地编号
	spe_id_local_0 = speechSpeechInsert("how to sleep well","room3")
	#打印本地speech的本地编号
	print("spe_id_local:%s"%(spe_id_local_0))
	#上传部分speech,函数会自动获取server端的speechID 存储到本地speech_id_relation中
	#Note!!!上传SpeechRecord之前必须先上传SpeechSpeech
	speechSpeechUpload(spe_id_local_0)
	#插入记录
	speechRecordInsertFirst(spe_id_local_0,"2015210001")
	#批量上传,只上传两次都签到的,并且将is_uploaded属性设为true
	speechRecordUpload(spe_id_local_0)
if __name__ == '__main__':
	main()

	

	
	
	
