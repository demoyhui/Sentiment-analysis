# -*- coding:utf-8 -*-
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from django.http import HttpResponseRedirect
from django.shortcuts import render,render_to_response
import MySQLdb
from webserver.svm import SVM_Model

#正常用户分析
model=None
def score():
    global model
    if model==None:
        model = SVM_Model()


    scorelist=[]
    a=['2016-09','2016-10','2016-11','2016-12','2017-01','2017-02','2017-03']
    for ctime in a:
        relist=selectdb('顺丰控股',ctime)
        re=[]
        ll=len(relist)
        for row in relist:
            ct=row[0]
            #print ct
            re.append(ct)
        #print re
        result=model.predict(re)
        #print result
        scorelist.append(sum(result)/ll)
    print scorelist
    #将scorelist写入到一个文件中
    f=open('score.txt','w')
    for i in scorelist:
        f.write(str("%.4f"%i))
        f.write('\n')
    f.close()

#成熟用户分析

model1=None
def scoreold():
    global model1
    if model1==None:
        model1 = SVM_Model()


    scorelist=[]
    a=['2016-09','2016-10','2016-11','2016-12','2017-01','2017-02','2017-03']
    for ctime in a:
        relist=selectdbold('顺丰控股',ctime)
        re=[]
        ll=len(relist)
        for row in relist:
            ct=row[0]
            #print ct
            re.append(ct)
        #print re
        result=model1.predict(re)
        #print result
        scorelist.append(sum(result)/ll)
    print scorelist
    #将scorelist写入到一个文件中
    f=open('scoreold.txt','w')
    for i in scorelist:
        f.write(str("%.4f"%i))
        f.write('\n')
    f.close()

#非成熟用户分析
model2=None
def scorenew():
    global model2
    if model2==None:
        model2 = SVM_Model()


    scorelist=[]
    a=['2016-09','2016-10','2016-11','2016-12','2017-01','2017-02','2017-03']
    for ctime in a:
        relist=selectdbnew('顺丰控股',ctime)
        re=[]
        ll=len(relist)
        for row in relist:
            ct=row[0]
            #print ct
            re.append(ct)
        #print re
        result=model2.predict(re)
        #print result
        scorelist.append(sum(result)/ll)
    print scorelist
    #将scorelist写入到一个文件中
    f=open('scorenew.txt','w')
    for i in scorelist:
        f.write(str("%.4f"%i))
        f.write('\n')
    f.close()

#数据库链接操作
def conndb():
    #连接数据库
    conn=MySQLdb.connect(host="localhost",user="root",passwd="123",db="django",charset="utf8")
    return conn


#正常用户评论查询
def selectdb(sharename,ctime):
    db = conndb()
    cursor=db.cursor()
    ctime_str = "%"+ctime+"%"
    sql="select comment from sharecomment where sharename=%s and ctime like %s  "
    param=(sharename,ctime_str)
    cursor.execute(sql,param)
    relist=cursor.fetchall()
    cursor.close()
    db.commit()
    return relist

#成熟用户查询
def selectdbold(sharename,ctime):
    db = conndb()
    cursor=db.cursor()
    ctime_str = "%"+ctime+"%"
    sql="select comment from sharecomment where sharename=%s and ctime like %s and uinflu > 5 "
    param=(sharename,ctime_str)
    cursor.execute(sql,param)
    relist=cursor.fetchall()
    cursor.close()
    db.commit()
    return relist

#非成熟用户查询
def selectdbnew(sharename,ctime):
    db = conndb()
    cursor=db.cursor()
    ctime_str = "%"+ctime+"%"
    sql="select comment from sharecomment where sharename=%s and ctime like %s and uinflu <= 5 "
    param=(sharename,ctime_str)
    cursor.execute(sql,param)
    relist=cursor.fetchall()
    cursor.close()
    db.commit()
    return relist
if __name__ == "__main__":
    #根据需要查询用户的成熟和非成熟须手动切换
    scoreold()