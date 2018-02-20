#!/usr/bin/python3
import config
import configDB
import server
import configFTP
import register
import os
def examExamDownload(*exam_ids):
    with configDB.configLocalDB() as curLocal:
        with configDB.configServerDB() as curServer:
            print("examExamDownload")
            for exam_id in exam_ids:
                dir = config.localExamRecordDir + '/{0}'.format(exam_id)
                print(dir)
                if os.path.exists(dir) == False:
                    os.mkdir(dir)
                curServer.execute("select * from exam where id=%s"%(exam_id,))
                row = curServer.fetchone()
                curLocal.execute("insert into exam values %s on conflict(id) do update set \
                name=excluded.name, location=excluded.location, teacher=excluded.teacher"%(row,))
def examExamDelete(*exam_ids):
    with configDB.configLocalDB() as cur:
        print("examExamDelete")
        for exam_id in exam_ids:
            cur.execute("delete from exam where id=%s"%(exam_id,))
def examMemberDownload(*exam_ids):
    with configDB.configLocalDB() as curLocal:
        with configDB.configServerDB() as curServer:
            print("examMemberDownload")
            for exam_id in exam_ids:
                curServer.execute("select * from exam_member where exam_id=%s"%(exam_id,))
                rows = curServer.fetchall()
                for row in rows:
                    curLocal.execute("insert into exam_member values %s on conflict(exam_id, stu_id)\
                    do update set exam_id=excluded.exam_id, stu_id=excluded.stu_id",(row,))
                    curLocal.execute("insert into exam_record(exam_id,stu_id) values %s\
                    on conflict(exam_id,stu_id) do nothing",(row,))
def examMemberDelete(*exam_ids):
    with configDB.configLocalDB() as cur:
        print("examMemberDelete")
        for exam_id in exam_ids:
            cur.execute("delete from exam_member where exam_id=%s"%(exam_id,))
def examStudentDownload(*exam_ids):
    with configDB.configLocalDB() as curLocal:
        with configDB.configServerDB() as  curServer:
            print("examStudentDownload")
            for exam_id in exam_ids:
                configFTP.examStudentDownloadFiles(exam_id)
                curServer.execute("select id, name, class, finger, face \
                from student, exam_member \
                where id=stu_id \
                and exam_id =%s"%(exam_id,))
                rows = curServer.fetchall()
                for row in rows:
                    curLocal.execute("insert into exam_student values %s \
                    on conflict(id) do update set\
                    name=excluded.name, class=excluded.class,\
                    finger=excluded.finger, face=excluded.face",(row,))
def examRecordGetAttribute(exam_id,stu_id):
    with configDB.configLocalDB() as cur:
        cur.execute('select is_appended from exam_record where exam_id={0} and stu_id={1}'.format(exam_id,stu_id))
        result = cur.fetchone()
        if result == None:return "Empty"
        elif result[0] == True: return "Appended"
        else:return "Normal"
def examStudentAppend(stu_id,stu_name,stu_class):
    with configDB.configLocalDB() as cur:
        cur.execute("insert into exam_student (id,name,class) values({0},'{1}',{2})\
        on conflict (id) do update set id=excluded.id, \
        name=excluded.name, class=excluded.class".format(stu_id,stu_name,stu_class))
def examRecordInsert(exam_id,stu_id,finger,sim_finger,face,sim_face,is_ic,is_appended,is_matched):
    with configDB.configLocalDB() as cur:
        print("examRecordInsert")
        cur.execute("insert into exam_record(exam_id, stu_id,\
        finger, sim_finger, face, sim_face,\
        is_ic, is_appended,is_matched,\
        is_uploaded )\
        values( %s, %s, %s, %s, %s, %s,%s, %s, %s,false)\
        on conflict(exam_id, stu_id) do update set\
        finger=excluded.finger, sim_finger=excluded.sim_finger,\
        face=excluded.face, sim_face=excluded.sim_face,\
        is_ic=excluded.is_ic, is_appended=excluded.is_appended, \
        is_matched=excluded.is_matched,\
        is_uploaded=excluded.is_uploaded "%(exam_id,stu_id,finger,sim_finger,face,sim_face,is_ic,is_appended,is_matched))
def examRecordDelete(*ids):
    with configDB.configLocalDB() as cur:
        print("examRecordDelete")
        for exam_id, stu_id in ids:
            cur.execute("delete from exam_record where exam_id=%s and stu_id=%s"%(exam_id, stu_id))
def examRecordUpload(*ids):
    with configDB.configLocalDB() as curLocal:
        with configDB.configServerDB() as curServer:
            print("examRecordUpload")
            for exam_id, stu_id in ids:
                configFTP.examRecordUploadFiles((exam_id,stu_id),)
                curLocal.execute("select exam_id, stu_id, finger, sim_finger, face, sim_face,\
                is_ic, is_appended, is_matched \
                from exam_record\
                where exam_id=%s and stu_id=%s"%(exam_id,stu_id))
                rows = curLocal.fetchall()
                for row in rows:
                    curServer.execute("insert into exam_record(exam_id, stu_id,\
                    finger, sim_finger, face, sim_face, \
                    is_ic, is_appended, is_matched)\
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                    on conflict(exam_id, stu_id) do update set\
                    finger=excluded.finger, sim_finger=excluded.sim_finger,\
                    face=excluded.face, sim_face=excluded.sim_face,\
                    is_ic=excluded.is_ic, is_appended=excluded.is_appended,\
                    is_matched=excluded.is_matched,\
                    time=excluded.time"%row)
                    curLocal.execute("update exam_record set is_uploaded=true\
                    where exam_id=%s and stu_id=%s"%(exam_id, stu_id))
                curLocal.execute("select stu_id from exam_record where is_appended = true")
                ids = curLocal.fetchall()
                for id in ids:
                    print(id)
                    curLocal.execute("select name,class from exam_student where id = %s"%(id[0],))
                    stu_name,stu_class = curLocal.fetchone()
                    curServer.execute("insert into student (id,name,class) values(%s,'%s',%s)\
                    on conflict(id) do update set name=excluded.name,class=excluded.class"%(id[0],stu_name,stu_class))

def examExamShow():
    with configDB.configLocalDB() as curLocal:
        print("examMemberShow")
        curLocal.execute("select id from exam ")
        rows = curLocal.fetchall()
        return rows

def main():
    #初始化
    server.resetServerDB()
    server.resetServerFiles()
    configDB.resetLocalDB()
    configFTP.resetLocalFiles()

   #server端预装考试
    server.examExamInsert(1,'Math','room3','Tom')
    server.examExamInsert(2,'Math','room3','Tom')
    server.examMemberInsert(1,2015210001)

    #准备Student
    #模拟获得一个学生的文件(stu_id,fingerCnt,faceCnt)
    configFTP.registerStudentCreateFiles(2015210001,1,1)
    #注册一个学生(Stu_id,stu_name,stu_class,fingerCnt,faceCnt)//register下fingerCnt/faceCnt只能为0或1
    register.registerStudentInsert(2015210001,'Tesla',2015211001,1,1,'True')
    #上传学生的文件和数据库信息
    register.registerStudentUpload(2015210001)

    #下载考试相关信息
    #examExamDownload(1)
    #examMemberDownload(1)#下载好member后会自动将里面的记录作为主键在exam_record中生成空记录
    #examStudentDownload(1)#下载对应学生的文件和数据库信息

    #分别判断三个数据:已经存在与exam_record中的正常记录,不存在与表中,需要确认后append的记录,已经存在与表中且已经append的记录
    '''
    infos =((1,2015210001),(1,2015210002),(1,2015210002))
    for info in infos:
        attribute = examRecordGetAttribute(*info)
        print('Attribute of %s is %s'%(info,attribute))
        #模拟生成文件记录(exam_id,stu_id)
        configFTP.examRecordCreateFiles(*info,2,2)
        if attribute == 'Empty':
            #属性为"Empty"说明exam_record表中没有该记录,那么应该先弹窗提示,等待学生确认后再添加信息
            print("[这是一个弹窗]您不在当前考表中,如果确认考试信息无误,请继续...")
            #先记录这个需要append的学生的基本信息(id,name,class)并且添加到student表中
            #不用添加finger和face
            examStudentAppend(info[1],'Jerry',2015211001)
            #插入的时候要把sim_finger和sim_face设置为0,然后将is_appended设置为True,is_matched设置为False
            examRecordInsert(info[0],info[1],2,0,2,0,'False','True','False')
        elif attribute == 'Appended':
            #属性为"Appended"说明exam_record表中已经存在该记录而且is_appended属性为True
            #这种情况一般是appended的student想重新签到,可能是为了确认签到成功,也可能是为了更改信息,
            #比如前面忘带卡了,之后又找到卡了
            #插入的时候要把sim_finger和sim_face设置为0,然后将is_appended设置为True,is_matched设置为False
            examRecordInsert(info[0],info[1],2,0,2,0,'True','True','False')
        elif attribute == 'Normal':
            #属性为"Normal"说明exam_record表中有已存在该记录而且is_appended属性为False,
            #也就是说该学生与当前考试是存在与exam_member中的
            #这种情况即可能是正常的Student第一次签到,也可能不是第一次签到,但是没有什么区别,后面的签到记录会覆盖之前的
            #插入的时候要把is_appended设置为True,is_matched为实际匹配结果
            examRecordInsert(info[0],info[1],2,90,2,49,'True','False','False')
    #上传记录,不管是不是新增学生的记录
    examRecordUpload()
    examRecordUpload((1,2015210001),(1,2015210002))
    '''
if __name__ == '__main__':
    main()


