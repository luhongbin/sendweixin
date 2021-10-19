# coding=utf-8
from __future__ import unicode_literals
from wxpy import *
import requests,urllib
from apscheduler.schedulers.background import BlockingScheduler
import datetime,time,re
import urllib.request
import time,os,datetime
import pymssql  as pymssql
from utility import maxinterid,copyuser,get_t100,spider_tao,mini2weixin,get_msg,setImage,get_iciba,huangli,WeatherHtmlParser,days,get_chibahuangli,SentQQRooms,week
from youduim import get_t100zfix,get_t100z,dingding2sql,get_t10fz,get_yxh,get_kc
import xlrd
from SinaWeibo import Weibo

import requests
import json

import time

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

DBNAME = 'active'
DBHOST = '???.247.???.134'
DBUSER = 'lutec'
DBPASS = 'fw@fsd'
DBPORT = 25252

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}

bot = Bot()
#bot = Bot(console_qr=True, cache_path=True)#启用缓存，来保存自己的登录状态

def auto_reply(text):# 调用图灵机器人API，发送消息并获得机器人的回复
     url = "http://www.tuling123.com/openapi/api"
     api_key=""
     payload = {
     "key": api_key,
     "info": text,
     "userid": "lutec"
     }
     r = requests.post(url, data=json.dumps(payload))
     result = json.loads(r.content)
     return result["text"]


def holidaysend1():
    try:
        my_friends = bot.friends(update=True)  # 获取微信好友列表，如果设置update=True将从服务器刷新列表，去除列表第一个元素（自己）
        print(my_friends)
        friendnum = len(my_friends) - 1
        print(friendnum)
        for i in range(friendnum):# 查看自己好友数
            try:
                friend = my_friends[i]
                #print('元旦快乐，Happy New Year to you,不用回复')
                friend.send('前路浩浩荡荡，万事尽可期待，新的一年，共同祝愿，所念之人健康平安，所想之事顺心如意！')
                time.sleep(2)  # 隔3s发送一条消息
            except:
                print('error happy', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    except:
        print('holidaysend',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
def holidaysend():
    try:
        my_friends = bot.friends(update=True)  # 获取微信好友列表，如果设置update=True将从服务器刷新列表，去除列表第一个元素（自己）
        print(my_friends)
        friendnum = len(my_friends) - 1
        print(friendnum)
        for i in range(friendnum) :# 查看自己好友数
            try:
                friend = my_friends[i]
                #print('元旦快乐，Happy New Year to you,不用回复')
                friend.send('不删不聊不打扰，愿你前路浩浩荡荡，万事尽可期待，新的一年，愿你所想之事顺心如意！')
                time.sleep(2)  # 隔3s发送一条消息
            except:
                print('error happy', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    except:
        print('holidaysend',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
def SentChatRoomsMsg(sendname, context):
    try:
        today = datetime.date.today()
        today = today.strftime('%Y-%m-%d')
        workbook = xlrd.open_workbook("D:\everydayweixin.xlsx")
        sheet = workbook.sheet_by_name('Sheet1')
        textList = sheet.row_values( days(today, '2018-11-07'))
        name = textList[0]
        try:
            conn1 = pymssql.connect(host='192.168.0.2', user='sa', password='xxx', database='trade',
                                    charset='GBK')
            cur1 = conn1.cursor()
            date_order = datetime.datetime.now().strftime("%Y%m%d")
            cur1.execute("SELECT id,[CHIBA],[HUANGLI] FROM [W_chiba] where id='%s'" % (date_order))
            resone = cur1.fetchone()

            if resone == None:
                get_iciba1 = huangli() + ':\n\n' + get_iciba()
                get_C=get_iciba()+ ':'
                print(sendname + '失败', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), get_iciba1)
            else:
                get_iciba1 = resone[2] + '\n\n' + resone[1]
                get_C=resone[1]+ ':'
            if context == 'MY':
                sendconten = name
            if context == 'YuYao':
                sendconten = WeatherHtmlParser('101210404')
            elif context == 'ShenYang':
                sendconten = WeatherHtmlParser('101070101')
            elif context == 'DaLian':
                sendconten = WeatherHtmlParser('101070201')
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), sendname, sendconten)
            elif context == 'GuiXi':
                sendconten = WeatherHtmlParser('101241103')
            elif context == 'ShenZhen':
                sendconten = WeatherHtmlParser('101280601')
            elif context == 'HaiDian':
                sendconten = WeatherHtmlParser('101010100')
            elif context == 'ZhengZhou':
                sendconten = WeatherHtmlParser('101180101')
            elif context == 'JiuZaiGou':
                sendconten = WeatherHtmlParser('10127190601A')
            elif context == 'ChengDu':
                sendconten = WeatherHtmlParser('101270101')
            sendcontent = sendconten + get_iciba1 + '\n\n' + name
            sendcoweio = sendconten + get_C + '\n\n' + name
            sendcontenx = sendconten + get_iciba1 + '\n\n' + '美好的一天，开始了！'

        except:
            print(sendname+'失败', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),sendcontent)
        print(sendcontent)
        if sendname=='xxx' or sendname=='yyy': # 你朋友的微信名称，不是备注，也不是微信帐号。
            my_friend = bot.friends().search(sendname)[0]
            get_chibahuangli()
        else:
            my_friend = bot.groups().search(sendname)[0]
        if sendname == '公司运营周报':
            if os.path.exists('D:\data.png'):
                print('data.png 文件存在')
                try:
                    my_friend.send_image("D:\data.png")
                except:
                    print('send_image png file error')
                time.sleep(16)
            else:
                print('data.png 不存在文件存在')
                time.sleep(5)
                week()
                time.sleep(90)
                if os.path.exists('D:\data.png'):
                    print('data.png 第二次文件存在')
                    my_friend.send_image("D:\data.png")
                    time.sleep(16)
                else:
                    print('no png file')
            # week1 = time.strftime('%W')
            # week2=("D:\Lutec's " + week1 + "nd weekly report.xlsx")
            # my_friend.send_file(week2)
        else:
            if len(sendcontent) < 5000:
                if sendname == '西藏嗨逛群':
                    my_friend.send(sendcontenx)
                else:
                    my_friend.send(sendcontent)
            elif len(sendcontent) < 10000:
                if sendname == '西藏嗨逛群':
                    my_friend.send(sendcontenx)

                else:
                    my_friend.send(sendcontent[0:5000])
                    time.sleep(5)
                    my_friend.send(sendcontent[5001:])
            elif len(sendcontent) < 15000:
                my_friend.send(sendcontent[0:5000])
                time.sleep(5)
                my_friend.send(sendcontent[5001:10000])
                time.sleep(5)
                my_friend.send(sendcontent[10000:])

    except:
        try:
            my_friend1 = bot.friends().search('简单')[0]
            my_friend1.send(sendname)
            my_friend1.send(sendcontent)
        except:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    # week()
    # dingding2sql()
    # get_t100z()
    # get_yxh()
    try:
        # print(huangli())
        # print(get_iciba())
        # print(mini2weixin())
        #copyuser()
        #get_t100()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        scheduler = BlockingScheduler()
        #scheduler.add_job(SentChatRoomsMsg, 'cron', day_of_week='0-6', hour=14, minute=32, second=20, kwargs={"sendname": '简单', "context":'YuYao' })
        scheduler.add_job(SentChatRoomsMsg, 'cron', day_of_week='0-6', hour=0, minute=12, second=2, kwargs={"sendname": '肥哥', "context": 'ShenYang'})
        scheduler.add_job(SentChatRoomsMsg, 'cron', day_of_week='0-6', hour=0, minute=20, second=2, kwargs={"sendname": '西藏嗨逛群', "context": 'HaiDian'})
        # scheduler.add_job(week, 'cron', day_of_week='fri-fri', hour=16, minute=28, kwargs={}) #周一是0开始
        scheduler.add_job(SentChatRoomsMsg, 'cron', day_of_week='fri-fri', hour=16, minute=30, second=2, kwargs={"sendname": '公司运营周报', "context": 'YuYao'})
        # scheduler.add_job(SentChatRoomsMsg, 'cron', day_of_week='0-6', hour=0, minute=20, second=10, kwargs={"sendname": '冶金学院计算机86级', "context": 'ShenZhen'})
        scheduler.add_job(holidaysend, 'cron', year=2021, month=2, day=12, hour=0, minute=0, second=2)#节假日群发用的
        #scheduler.add_job(SentChatRoomsMsg, 'cron', year=2019, month=12, day=7, hour=17, minute=43, second=2, kwargs={"sendname": '冶金学院计算机86级', "context": 'MY'})#
        # 节假日群发用的
        # scheduler.add_job(mini2weixin, 'cron', day_of_week='0-6', hour=4, minute=0, kwargs={})()
        # scheduler.add_job(spider_tao, 'cron', day_of_week='0-6', hour=11, minute=30, kwargs={})
        # scheduler.add_job(mini2weixin, 'cron', day_of_week='0-6', hour='2-23', minute='0-59',kwargs={})
        # scheduler.add_job(SentQQRooms, 'cron', day_of_week='0-6', hour=5, minute=30, second=10,kwargs={"sendname": '☽.', "context": 'ChongQing'})

        scheduler.add_job(SentQQRooms, 'cron', day_of_week='0-6', hour=7, minute=13, second=10, kwargs={"sendname": 'SUPERMAN', "context": 'ShenZhen'})
        #scheduler.add_job(get_t100, 'cron', day_of_week='0-6', hour='8-20', kwargs={})
        scheduler.add_job(get_yxh, 'cron', day_of_week='mon-mon', hour=7, minute=0, kwargs={}) #周一是0开始
        scheduler.add_job(week, 'cron', day_of_week='fri-fri', hour=16, minute=25, kwargs={}) #周一是0开始
        scheduler.add_job(get_kc, 'cron', day=15, hour=6, minute=30, second=2, kwargs={})
        scheduler.add_job(get_kc, 'cron',  day=1, hour=6, minute=30, second=2, kwargs={})

        scheduler.add_job(get_t100z, 'cron', day_of_week='0-5', hour=6, minute=50, kwargs={})
        scheduler.add_job(get_t100zfix, 'cron', day_of_week='0-5', hour=22, minute=30, kwargs={})
        scheduler.add_job(dingding2sql, 'cron', day_of_week='0-6', hour=4,minute=10, kwargs={})
    #     scheduler.add_job(get_t10fz, 'interval',   minutes =10,   kwargs={})
    #     get_t100z()
        scheduler.start()
    except:
        print('程序中断:',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))