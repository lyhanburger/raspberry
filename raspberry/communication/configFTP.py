#!/usr/bin/python3
import ftplib
import config,configDB
import os
import register,exam,server
import shutil
class configFTP():
	def __enter__(self):
		self.ftp = ftplib.FTP(config.serverFTPIP,config.serverFTPUser,config.serverFTPPasswd)
		return self.ftp
	def __exit__(self,type,value,traceback):
		self.ftp.close()
def resetLocalFiles():
	print('resetLocalFiles')
	shutil.rmtree(config.localRegisterStudentDir)
	shutil.rmtree(config.localExamStudentDir)
	shutil.rmtree(config.localExamRecordDir)
	os.mkdir(config.localRegisterStudentDir)
	os.mkdir(config.localExamStudentDir)
	os.mkdir(config.localExamRecordDir)
def registerStudentUploadFiles(*stu_ids):
	with configDB.configLocalDB() as cur:
		with configFTP() as ftp:
			print("registerStudentUploadFiles")
			for stu_id in stu_ids:
				cur.execute("select finger, face from register_student where id =%s",(stu_id,))
				fingerCnt, faceCnt = cur.fetchone()
				#上传stu_id学生的txt文件.该学生有fingerCnt个txt文件,local端目录是...,server端目录是...
				uploadGroupFiles(ftp,stu_id,".txt",fingerCnt,config.localRegisterStudentDir, config.serverStudentDir)
				#上传stu_id学生的jpg文件.该学生有fingerCnt个jpg文件,local端目录是...,server端目录是...
				uploadGroupFiles(ftp,stu_id,".jpg",faceCnt,config.localRegisterStudentDir, config.serverStudentDir)
def registerStudentCreateFiles(stu_id,fingerCnt,faceCnt):
	dir = config.localRegisterStudentDir
	if fingerCnt == 1:
		f = open(dir + '/{0}_0.txt'.format(stu_id),'wb')
		f.close()
	if faceCnt == 1:
		f = open(dir + '/{0}_0.jpg'.format(stu_id),'wb')
		f.close()
def examRecordCreateFiles(exam_id, stu_id,fingerCnt,faceCnt):
	dir = config.localExamRecordDir + '/{0}'.format(exam_id)
	if os.path.exists(dir) == False:
		os.mkdir(dir)
	for fingerNo in range(fingerCnt):
		f = open(dir + '/{0}_{1}.txt'.format(stu_id,fingerNo),'wb')
		f.close()
	for faceNo in range(faceCnt):
		f = open(dir + '/{0}_{1}.jpg'.format(stu_id,faceNo),'wb')
		f.close()
def examRecordUploadFiles(*id_groups):
	with configDB.configLocalDB() as cur:
		with configFTP() as ftp:
			print("examRecordUploadFiles")
			for exam_id,stu_id in id_groups:
				local_dir = config.localExamRecordDir + '/' + str(exam_id)
				server_dir = config.serverExamRecordDir + '/' +str(exam_id)
				if (server_dir in ftp.nlst(config.serverExamRecordDir)) == False :
					ftp.mkd(server_dir)
				cur.execute("select finger, face from exam_record where exam_id=%s and stu_id=%s",(exam_id, stu_id))
				fingerCnt, faceCnt = cur.fetchone()
				uploadGroupFiles(ftp, stu_id,".txt",fingerCnt,local_dir,server_dir)
				uploadGroupFiles(ftp, stu_id,".jpg",faceCnt,local_dir,server_dir)
def examStudentDownloadFiles(*exam_ids):
	with configDB.configServerDB() as cur:
		with configFTP() as ftp:
			print("examStudentDownloadFiles")
			for exam_id in exam_ids:
				cur.execute("select stu_id from exam_member where exam_id=%s"%(exam_id,))
				stu_ids = cur.fetchall()
				for stu_id in stu_ids:
					stu_id = stu_id[0]
					cur.execute("select finger, face from student where id=%s"%(stu_id,))
					fingerCnt, faceCnt = cur.fetchone()
					downloadGroupFiles(ftp, stu_id,".txt",fingerCnt,config.localExamStudentDir, config.serverStudentDir)
					downloadGroupFiles(ftp, stu_id,".jpg",faceCnt,config.localExamStudentDir, config.serverStudentDir)
def uploadGroupFiles(ftp, stu_id,fileType,fileCnt, localFileDir, serverFileDir):
	for fileNo in range(fileCnt):
			localFileName = localFileDir + "/" + str(stu_id) + "_" + str(fileNo) + fileType
			serverFileName = serverFileDir + "/" + str(stu_id) + "_" + str(fileNo) + fileType
			print("localFile:%s"%localFileName)
			print("serverFile:%s"%serverFileName)
			localFile = open(localFileName,"rb")
			ftp.storbinary("STOR "+serverFileName, localFile)
			localFile.close()
def downloadGroupFiles(ftp, stu_id,fileType,fileCnt, localFileDir, serverFileDir):
	for fileNo in range(fileCnt):
		localFileName = localFileDir + "/" + str(stu_id) + "_" + str(fileNo) + fileType
		serverFileName = serverFileDir + "/" + str(stu_id) + "_" + str(fileNo) + fileType
		print("localFile:%s"%localFileName)
		print("serverFile:%s"%serverFileName)
		localFile = open(localFileName,"wb")
		ftp.retrbinary("RETR "+serverFileName, localFile.write)
		localFile.close()
		for suffix in ("jpg","txt"):
			f = open("{0}/{1}_0.{2}".format(localFileDir,stu_id,suffix),"wb")
			f.close()
def main():
	#初始化local和server
	server.resetServerDB()
	server.resetServerFiles()
	configDB.resetLocalDB()
	resetLocalFiles()
#	#模拟注册
	registerStudentCreateFiles(2015210001,1,1)
	register.registerStudentInsert(2015210001,'Tesla',2015211001,1,1,'True')
#	#上传注册的文件信息和数据库信息
	register.registerStudentUpload(2015210001)
	register.registerStudentUpload(2015210001)
#
##	#模拟添加考试信息
#	server.examExamInsert(1,'Math','room3','Tom')	
#	server.examMemberInsert(1,2015210001)
##	#下载考试的数据库信息
#	exam.examExamDownload(1)
#	exam.examMemberDownload(1)
#	#下载考试对应的学生的文件信息和数据库信息
#	exam.examStudentDownload(1)
#	exam.examStudentDownload(1)
#
##	#模拟考试签到
#	examRecordCreateFiles(1,2015210001,2,2)
#	exam.examRecordInsert(1,2015210001,2,80,2,75,'True','False','True')
##	#上传考试记录的数文件信息和据库信息
#	exam.examRecordUpload((1,2015210001))
#	exam.examRecordUpload((1,2015210001))
#
if __name__ == '__main__':
	main()
		
