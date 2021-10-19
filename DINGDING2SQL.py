# coding=utf-8
from __future__ import unicode_literals
import os

import requests
import json
import pymssql
import pymysql

corp_id = 'XXX'
app_secret = 'XX-XX-XX'
agent_id = "XX"
app_key = 'XX'

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def getAccess():
    url = "https://oapi.dingtalk.com/gettoken?appkey={0}&appsecret={1}".format(app_key, app_secret)
    jo = json.loads(requests.get(url).text)
    return jo['access_token']


def getDp(token):
    url = "https://oapi.dingtalk.com/department/list?access_token=" + token
    print(url)
    dp = json.loads(requests.get(url).text)
    print(dp)
    return dp['department']


def getUsers(deptId):
    token = getAccess()
    url = "https://oapi.dingtalk.com/user/getDeptMember?access_token={0}&deptId={1}".format(token, deptId)
    users = json.loads(requests.get(url).text)
    return users['userIds']


def getUserInfo(token, userId):
    url = "https://oapi.dingtalk.com/user/get?access_token={0}&userid={1}".format(token, userId)
    info = json.loads(requests.get(url).text)
    print(info)
    try:
        job=info['jobnumber']
    except:
        job=''
    return info['name'], info['userid'], job, info['mobile'], info['orderInDepts'], info['avatar']

import cx_Oracle
def save(id, name,jobnumber,mobile,orderInDepts,dept,avatar):
    print(id, name,jobnumber,mobile,orderInDepts,dept,avatar)
    sql1 = "update dingdinguser set name = '%s',jobnumber = '%s',mobile = '%s',orderInDepts = '%s',dept = '%s'  where userid ='%s'" % (name,jobnumber,mobile,orderInDepts,dept,id)
    sql = "insert into dingdinguser (userid,name) values ('%s','%s')" % (id, name)
    sqlmy1 = "update litemall_user set password='$2a$10$Dgi78dZc8kvpSKY8W4.v/.drMqa4Wjf/QarTtMFr.5tPamCOjHBtC',nickname = '%s',weixin_openid = '%s',mobile = '%s',session_key = '%s',avatar = '%s'  where username ='%s'" % (name,jobnumber,mobile,dept,avatar,id)
    sqlmy = "insert into litemall_user (username, nickname) values ('%s','%s')" % (id, name)
    sqlmy2 = "insert into litemall_admin (username, avatar,password,role_ids) values ('%s','%s','$2a$10$Dgi78dZc8kvpSKY8W4.v/.drMqa4Wjf/QarTtMFr.5tPamCOjHBtC','[2]')" % (id, avatar) #密码APZHSBfBjC5Ybf2p
    sqlmy3 = "update litemall_admin set jobNumber = '%s',nickname = '%s',dept = '%s',mobile = '%s'  where username ='%s'" % (jobnumber,name,dept,mobile,id)
    sqlmy4 = "update litemall_admin set role_ids = '[1]'  where mobile ='13958356141'"
    db = pymssql.connect(host='192.168.0.2', user='sa', password='yh***microsoft***', database='trade', charset='utf8')
    dbmysql = pymysql.connect(host="localhost", user="root", password="123456", database="packageapp", charset='utf8')
    cur = db.cursor()  # 游标操作
    curmy = dbmysql.cursor()  # 游标操作
    try:
        try:
            cur.execute(sql)
            cur.execute(sql1)
            db.commit()
            print("db success")
        except:
            cur.execute(sql1)
            db.commit()
            print("db 有了")
        try:
            curmy.execute(sqlmy)
            curmy.execute(sqlmy1)
            print("db1 success")
        except:
            curmy.execute(sqlmy1)
            print("db1 有了")
        dbmysql.commit()

        try:
            curmy.execute(sqlmy2)
            curmy.execute(sqlmy3)
            dbmysql.commit()
            print("db2 success")
        except Exception as e:
            if mobile == '13958356141':
                curmy.execute(sqlmy4)
            else:
                curmy.execute(sqlmy3)
            dbmysql.commit()
            print(e)

    except Exception as e:
        cur.execute(sql1)
        db.commit()
        curmy.execute(sqlmy1)
        # curmy.execute(sqlmy2)
        dbmysql.commit()
        print("DB Exception:=>")
        print(e)
    finally:
        db.close
        curmy.close

# token
# token = 'f2046dac75c4312fb4670052bd1711f9'
# token = ''
# if token == '':
#     token = getAccess()
# #
# dp = []
# if len(dp) == 0:
#     dp = getDp(token)
#
# for d in dp:
#     print("开始 部门:" + (d['name']) + '------>')
#     if d['id'] == 1:
#         continue;
#     users = getUsers(d['id'])
#     for u in users:
#         username, id, jobnumber, mobile, orderInDepts, avatar = getUserInfo(token, u)
#         # print('userId:' + u + '  ' + username + ':' + jobnumber + ':' + mobile + ':' + orderInDepts)
#         save(u, username,jobnumber,mobile,orderInDepts,d['name'], avatar)

#默认情况下第一次创建群组 并获取群组id chatid并写入文件里

def getChatid(useridlist,title):
    sql = "select top 1 chatid,title from dingdingchat where title='%s'" % (title)
    db = pymssql.connect(host='192.168.0.2', user='sa', password='yh***microsoft***', database='trade', charset='utf8')
    cur = db.cursor()  # 游标操作
    cur.execute(sql)
    resone1 = cur.fetchone()

    useridlist1 = useridlist
    useridlist1 = useridlist1.replace('|', ',')
    name = useridlist
    strlist = name.split('|')  # 用逗号分割str字符串，并保存到列表

    print('strlistsdfgsdfg:',strlist)

    for value in strlist:  # 循环输出列表值
        sql = "select top 1 userid from dingdinguser where name='%s'" % (value)
        cur.execute(sql)
        resone = cur.fetchone()
        if resone == None:
            useridlist1 = useridlist1.replace(value, '')
            useridlist1 = useridlist1.replace("'',", '')
            useridlist1 = useridlist1.replace(",,", ',')
            # useridlist1 = useridlist1[1:]
        else:
            useridlist1 = useridlist1.replace(value, resone[0])
    if useridlist1[0] == ',':
        useridlist1 = useridlist1[1:]
    print('useridlist1',useridlist1)
    if resone1 == None:
        file_name = "/tmp/.chatid"
        #判断群组id文件是否存在
        if not os.path.exists(file_name) or 1 == 1:
            token = getAccess()

            url = 'https://oapi.dingtalk.com/chat/create?access_token=%s' % token
            data = {
                "name": title, #name : 群组名字
                "owner": "32035136051207483998", # 群主userid
                "useridlist": useridlist1.split(',') #群成员userId列表 也可以写群主userid
            }
            # print(data)

            data = json.dumps(data)
            req = requests.post(url, data)
            print(req.text)
            chatid = json.loads(req.text)['chatid']
            # with open(file_name, 'w') as fd:
            #     fd.write(chatid)
        else:
            with open(file_name) as fd:
                chatid = fd.read()
        sql = "insert into dingdingchat (chatid,member_id,member_name,title) values ('%s','%s','%s','%s')" % (chatid, useridlist1,useridlist,title)
        cur.execute(sql)
        db.commit()
    else:
        chatid=resone1[0]
        print('chatid',useridlist1, useridlist,title, chatid)

        sql = "update dingdingchat set member_id='%s',member_name='%s',title='%s' where chatid='%s'" % (useridlist1, useridlist,title, chatid)
        cur.execute(sql)
        db.commit()
        token = getAccess()
        url = 'https://oapi.dingtalk.com/chat/get?access_token=%s&chatid=%s' % (token, chatid)
        req = requests.get(url)
        print(req.text)
        try:
            useridlistnow = json.loads(req.text)['chat_info']['useridlist']
        except:
            useridlistnow = []
        deldata=useridlistnow.copy()
        equl1=deldata.copy()
        equl1=equl1.sort()
        useridlist11=useridlist1.split(',')
        equl2=useridlist11.copy()
        equl2=equl2.sort()
        print('useruseridlist1idlist1',useridlist11,equl1,equl2)
        sqluserlistadd = useridlist11.copy()
        sqluserlist = useridlist11.copy()
        adddata=useridlist11.copy()

        for useridlistold in range(len(useridlistnow)):
            a=useridlistnow[useridlistold]
            t = 1
            for useridnew in range(len(sqluserlistadd)):
                b=sqluserlistadd[useridnew]
                if a == b:
                    deldata.remove(a)

                # adddata.remove(useridlistold)
        # #
        print('useridlist11',deldata,adddata,useridlist11)
        for useridnew in range(len(sqluserlist)):
            t = 1
            a=sqluserlist[useridnew]
            for useridlistold in useridlistnow:
                if useridlistold == a:
                    t = 0
            if t == 0:
               adddata.remove(a)
        try:
            adddata.remove('')
        except:
            print('adddata no')

        #
        print('adddata:',adddata,deldata,useridlistnow,useridlist11,sqluserlist)
        url = 'https://oapi.dingtalk.com/chat/update?access_token=%s' % token
        # or equl1 == equl2
        if (len(deldata)==0 and len(adddata)==0):
            xxx=1
        else:
            xxx=0
        if len(deldata)==0:
            data = {
                "chatid": chatid,  # 群主userid
                "add_useridlist": adddata  # 群成员userId列表 也可以写群主userid
            }
        elif len(adddata)==0:
            data = {
                "chatid": chatid,  # 群主userid
                "del_useridlist": deldata  # 群成员userId列表 也可以写群主userid
            }
        else:
            data = {
                "chatid": chatid,  # 群主userid
                "del_useridlist": deldata,  # 群成员userId列表 也可以写群主userid
                "add_useridlist": adddata  # 群成员userId列表 也可以写群主userid
            }
        if xxx==0:
            print(data)
            data = json.dumps(data)
            req = requests.post(url, data)

            errmsg = json.loads(req.text)['errmsg']
            if errmsg == 'ok':
                print("ok")
            else:
                print("fail: %s" % req.text)
    return chatid

#access_token 访问令牌 chatid 群组id content 发送的内容
def tonews(chatname, content,title):
    token = getAccess()

    chatid = getChatid(chatname,title)
    url = "https://oapi.dingtalk.com/chat/send?access_token=%s" % token
    msgtype = 'text'
    values = {"chatid": chatid, "msgtype": msgtype, msgtype: {"content": content} }
    values = json.dumps(values)
    print('chatid:',chatid,chatname, content,title,values)
    data = requests.post(url, values)
    errmsg = json.loads(data.text)['errmsg']
    if errmsg == 'ok':
        return "ok"
    return "fail: %s" % data.text

# chatid = getChatid(token)
# content = '测试'
# print(tonews(token, chatid, content))