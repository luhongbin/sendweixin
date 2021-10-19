# coding=utf-8
from __future__ import unicode_literals
# import entapp.client as app
from entapp.message import *
import cx_Oracle
import datetime,time,re,os,string
from DINGDING2SQL import getDp, getUsers, getUserInfo, getAccess, save,getChatid,tonews
import pymssql
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

BUIN = 1111111  # 请填写企业总计号

AES_KEY = 'xxx='  # 请填写企业应用EncodingAesKey

APP_ID = 'xxx'  # 请填写企业应用AppId

ADDRESS = '192.168.0.???:7080'  # 请填写有度服务器地址

IMAGE_NAME = ''  # 请填写测试图片名称
IMAGE_PATH = ''  # 请填写测试图片路径

FILE_NAME = ''  # 请填写测试文件名称
FILE_PATH = ''  # 请填写测试文件路径

OUT_DIR = ''  # 请填写测试下载输出目录

TO_USER = 'XXX'  # 请填写测试接收消息的账号，使用'|'符号分割

# client = app.AppClient(BUIN, APP_ID, AES_KEY, ADDRESS)

# 在钉钉上创建应用后获取
AGENT_ID = 111111
APP_KEY = "xxx"
APP_SECRET = "xxx-xxx"

dd_domain = "https://oapi.dingtalk.com"


# class AppClientTestCase(unittest.TestCase):
#
#     def test_send_text_msg(self):
#         """
#         测试文字消息
#         """
#         body = TextBody('你好有度')
#         msg = Message(TO_USER, MESSAGE_TYPE_TEXT, body)
#         client.send_msg(msg)
#
#     def test_send_image_msg(self):
#         """
#         测试图片消息
#         """
#         media_id = client.upload_file(app.FILE_TYPE_IMAGE, IMAGE_NAME, IMAGE_PATH)
#         body = ImageBody(media_id)
#         msg = Message(TO_USER, MESSAGE_TYPE_IMAGE, body)
#         client.send_msg(msg)
#
#     def test_send_file_msg(self):
#         """
#         测试文件消息
#         """
#         media_id = client.upload_file(app.FILE_TYPE_FILE, FILE_NAME, FILE_PATH)
#         body = FileBody(media_id)
#         msg = Message(TO_USER, MESSAGE_TYPE_FILE, body)
#         client.send_msg(msg)
#
#     def test_send_mpnews_msg(self):
#         """
#         测试图文消息
#         """
#         media_id = client.upload_file(app.FILE_TYPE_IMAGE, IMAGE_NAME, IMAGE_PATH)
#         body = MpnewsBody([MpnewsBodyCell('你好有度', media_id, '有度', '工作需要张弛有度')])
#         msg = Message(TO_USER, MESSAGE_TYPE_MPNEWS, body)
#         client.send_msg(msg)
#
#     def test_send_exlink_msg(self):
#         """
#         测试外链消息
#         """
#         media_id = client.upload_file(app.FILE_TYPE_IMAGE, IMAGE_NAME, IMAGE_PATH)
#         body = ExlinkBody([ExlinkBodyCell('你好有度', 'https://youdu.im', '有度', media_id)])
#         msg = Message(TO_USER, MESSAGE_TYPE_EXLINK, body)
#         client.send_msg(msg)
#
#     def test_download_image(self):
#         """
#         测试下载图片
#         """
#         media_id = client.upload_file(app.FILE_TYPE_IMAGE, IMAGE_NAME, IMAGE_PATH)
#         client.download_file(media_id, OUT_DIR)
#
#     def test_download_file(self):
#         """
#         测试下载文件
#         """
#         media_id = client.upload_file(app.FILE_TYPE_FILE, FILE_NAME, FILE_PATH)
#         client.download_file(media_id, OUT_DIR)
#
#     def test_search_file(self):
#         """
#         测试搜索文件
#         """
#         media_id = client.upload_file(app.FILE_TYPE_FILE, FILE_NAME, FILE_PATH)
#         name, size = client.search_file(media_id)
#         print('name: {name}, size: {size}\n'.format(name=name, size=size))

# token
# token = 'f2046dac75c4312fb4670052bd1711f9'
token = ''
if token == '':
    token = getAccess()


def dingding2sql():
    db = pymssql.connect(host='192.168.0.2', user='sa', password='xxx', database='trade', charset='utf8')

    cur = db.cursor()  # 游标操作
    sql = "delete from dingdinguser"
    cur.execute(sql)
    db.commit()

    token = getAccess()
    dp = []
    if len(dp) == 0:
        dp = getDp(token)

    for d in dp:
        print("开始 部门:" + (d['name']) + '------>')
        if d['id'] == 1:
            # print('dept:' + d['name'] + ':' + + d['id'] )

            continue
        try:
            users = getUsers(d['id'])

            for u in users:
                username, id, jobnumber, mobile, orderInDepts, avatar = getUserInfo(token, u)
                print('userId:' + u + '  ' + username + ':' + jobnumber + ':' + mobile + ':' + d['name'] + ':' + avatar)
                save(u, username,jobnumber,mobile,orderInDepts,d['name'],avatar)
        except:
            print('dingding2sql error',token, d['id'])
def dingdingexist(value):
    db = pymssql.connect(host='192.168.0.2', user='sa', password='yh***microsoft***', database='trade', charset='utf8')
    cur = db.cursor()  # 游标操作
    sql = "select top 1 userid from dingdinguser where name='%s'" % (value)
    cur.execute(sql)
    resone = cur.fetchone()
    cur.close
    if resone == None:
        return 0
    else:
        return 1
def dingdingsend(r10,tosend,title):

    strcontent = len(r10.encode('utf-8'))
    if strcontent >=2000:
        boday=r10[0:2000]+'\n\n...'
    else:
        boday=r10
    if '1.' in boday:
        # chatid = getChatid(tosend)
        # print(tosend, boday,title)
        print(tonews(tosend, boday,title))

def getr10(r10,tosend,title):
    dingdingsend(r10,tosend,title)
    # print(r10,tosend,title)
    # tosend= '鲁红斌'
    # 下面是有度的发送代码
    # strcontent = len(r10.encode('utf-8'))
    # if strcontent <= 600:
    #     if '1.' in r10:
    #         boday = TextBody(r10)
    #         msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #         client.send_msg(msg)
    # elif strcontent <= 1200:
    #     boday = TextBody(r10[0:600])
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
    #     time.sleep(5)
    #     boday = TextBody(r10[601:1200])
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
    # elif strcontent <= 1800:
    #     boday = TextBody(r10[0:600])
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
    #     time.sleep(5)
    #     boday = TextBody(r10[600:1200])
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
    #     time.sleep(5)
    #     boday = TextBody(r10[1200:1800])
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
    # elif strcontent > 1800:
    #     boday = TextBody(r10[0:600])
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
    #     time.sleep(5)
    #     boday = TextBody(r10[600:1200])
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
    #     time.sleep(5)
    #     boday = TextBody(r10[1200:1750] + '\n\n太多了,自己去查...')
    #     msg = Message(tosend, MESSAGE_TYPE_TEXT, boday)
    #     client.send_msg(msg)
def get_t100z():
    conn2 = cx_Oracle.connect('dsdata/dsdata@192.168.0.5:1521/TOPPRD')
    cur = conn2.cursor()
    # # #####采购逾期通知
    # xxx = "select pmdldocno 采购单号,pmdnseq 采购项次,NVL(pmdnua002,'无') 订单号,pmdn001 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,((pmdo005-pmdo019+pmdo017) /pmdo008) 未交数量,pmdo012 应交日期,NVL(ooag011,'无') 采购员 from pmdn_t left join pmdl_t on pmdnent=pmdlent and pmdnsite=pmdlsite and pmdndocno=pmdldocno left join pmdo_t on pmdnent=pmdoent and pmdnsite=pmdosite and pmdndocno=pmdodocno and pmdnseq=pmdoseq left join imaal_t on pmdnent=imaalent and pmdn001=imaal001 and imaal002='zh_CN' left join ooag_t on pmdlent=ooagent and pmdl002=ooag001 where pmdnent='60' and pmdn045='1' and pmdlstus='Y' and ((pmdo005-pmdo019+pmdo017) /pmdo008)>0 and pmdo012<sysdate-1 order by ooag011,pmdldocno,pmdnseq "
    # cur.execute(xxx)
    # res = cur.fetchall()
    # xx = 0
    # r0 = ''
    # r3 = ''
    # cc = 0
    # r10=''
    # aa=0
    # for tao in res:
    #     r0 = '.采购单号：' + tao[0] + '-' + str(tao[1]) + ',订单号:' + tao[2] + ',料号：' + tao[3] + '[' + tao[4] + ',' + tao[5] + '],未交数量:'+ str(tao[6]) + ',应进日期:' + datetime.datetime.strftime(tao[7], "%Y-%m-%d")
    #     if cc == 0:
    #         r1 = tao[8]
    #     else:
    #         r3 = tao[8]
    #     if cc == 1:
    #         if r3 == r1:
    #             xx = xx + 1
    #             r10 = r10 + str(xx) + r0 + '\n'
    #             r1 = tao[8]
    #             aa=aa+tao[6]
    #         else:
    #             time.sleep(5)
    #             print(len(r10.encode('utf-8')))
    #             try:
    #                 r10 = '采购逾期通知(' + str(xx) + '项,未交数量共'+str(format(aa,","))+'件['+r1+']):\n' + r10
    #                 tosend = r1+'|周洪|施维君|鲁红斌'
    #                 getr10(r10,tosend)
    #             except:
    #                 r10 = '采购员已离职！' + r10
    #                 tosend = '周洪|施维君|鲁红斌'
    #                 getr10(r10,tosend)
    #             xx = 0
    #             # print(r10)
    #             r10 = ''
    #             cc=0
    #     else:
    #         cc=1
    #
    # #####未来1周交货通知
    # xxx = "select pmdldocno 采购单号,pmdnseq 采购项次,NVL(pmdnua002,'无') 订单号,pmdn001 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,((pmdo005-pmdo019+pmdo017) /pmdo008) 未交数量,pmdo012 应交日期,NVL(ooag011,'无') 采购员 from pmdn_t left join pmdl_t on pmdnent=pmdlent and pmdnsite=pmdlsite and pmdndocno=pmdldocno left join pmdo_t on pmdnent=pmdoent and pmdnsite=pmdosite and pmdndocno=pmdodocno and pmdnseq=pmdoseq left join imaal_t on pmdnent=imaalent and pmdn001=imaal001 and imaal002='zh_CN' left join ooag_t on pmdlent=ooagent and pmdl002=ooag001 where pmdnent='60' and pmdn045='1' and pmdlstus='Y' and ((pmdo005-pmdo019+pmdo017) /pmdo008)>0 and pmdo012>=sysdate-1 and pmdo012<sysdate+6  order by ooag011,pmdldocno,pmdnseq "
    # cur.execute(xxx)
    # res = cur.fetchall()
    # xx = 0
    # r0 = ''
    # r3 = ''
    # cc = 0
    # r10 = ''
    # aa=0
    # for tao in res:
    #     r0 = '.采购单号：' + tao[0] + '-' + str(tao[1]) + ',订单号:' + tao[2] + ',料号：' + tao[3] + '[' + tao[4] + ',' + tao[
    #         5] + '],未交数量:' + str(tao[6]) + ',应进日期:' + datetime.datetime.strftime(tao[7], "%Y-%m-%d")
    #     if cc == 0:
    #         r1 = tao[8]
    #     else:
    #         r3 = tao[8]
    #     if cc == 1:
    #         if r3 == r1:
    #             xx = xx + 1
    #             r10 = r10 + str(xx) + r0 + '\n'
    #             r1 = tao[8]
    #             aa=aa+tao[6]
    #
    #         else:
    #             time.sleep(5)
    #             print(len(r10.encode('utf-8')))
    #             try:
    #                 r10 = '未来1周交货通知(' + str(xx) + '项,未交数量共'+str(format(aa,","))+'件[' + r1 + ']):\n' + r10
    #                 tosend = r1 + '|周洪|施维君|鲁红斌'
    #                 getr10(r10, tosend)
    #             except:
    #                 r10 = '采购员已离职！' + r10
    #                 tosend = '周洪|施维君|鲁红斌'
    #                 getr10(r10, tosend)
    #             xx = 0
    #             # print(r10)
    #             r10 = ''
    #             cc = 0
    #     else:
    #         cc = 1


    # #####未来1周应付款到期
    # xxx = "select NVL(ooag011,'无') 采购员 from  apcc_t left join apca_t on apccent = apcaent and apccld = apcald and apccdocno = apcadocno left join pmaal_t on apcaent=pmaalent and apca005 = pmaal001 and pmaal002='zh_CN' left join ooag_t on apcaent = ooagent and apca014=ooag001 where apccent = '60' and apcc108<>apcc109 and apca001 in ('13','17') and apccld in ('Y1','Y3','Y4','YM') and apcc003<sysdate+7 group by ooag011 order by  ooag011"
    # cur.execute(xxx)
    # res = cur.fetchall()
    # for tao1 in res:
    #     yy=tao1[0]
    #     xx=0
    #     xxx = "select apca005||':'||pmaal004 供应商,apccdocno 应付账款单,apccseq 项次,apcc108-apcc109 原币待付,apca100 币种,apcc118-apcc119 本币待付,apcc003 应付款日,NVL(ooag011,'无')  采购员,apccld 账套 from  apcc_t left join apca_t on apccent = apcaent and apccld = apcald and apccdocno = apcadocno left join pmaal_t on apcaent=pmaalent and apca005 = pmaal001 and pmaal002='zh_CN' left join ooag_t on apcaent = ooagent and apca014=ooag001 where apccent = '60' and apcc108<>apcc109 and apca001 in ('13','17') and apccld in ('Y1','Y3','Y4','YM') and apcc003<sysdate+7 and ooag011='%s'" % (yy)
    #     cur.execute(xxx)
    #     res1 = cur.fetchall()
    #     r10 = ''
    #     bb = 0
    #     title = yy+':未来1周应付款到期'
    #
    #     for tao in res1:
    #         xx = xx + 1
    #         r0 = '.供应商：' + tao[0] + ',应付账款单:' + tao[1] + '-' + str(tao[2]) + ',应付原币：' + str(tao[3]) + tao[4] + ',应付本币:' + str(tao[5]) +  ',应付款日:' + datetime.datetime.strftime(tao[6], "%Y-%m-%d")
    #
    #         bb = bb + tao[5]
    #         r10 = r10 + str(xx) + r0 + '\n'
    #     try:
    #         bb = round(bb)
    #         r10 = '未来1周应付款到期(' + str(xx) + '项,应付本币共' + str(format(bb, ",")) + '元[' + yy + ']):\n' + r10
    #         tosend = yy + '|周洪|舒银萍|施维君|鲁红斌'
    #         getr10(r10, tosend,title)
    #     except:
    #         r10 = yy+'采购员已离职！' + r10
    #         tosend = '周洪|舒银萍|施维君|鲁红斌'
    #         getr10(r10, tosend,title)

     #  #####未来1周应收款到期
    #
    # xxx = "select NVL(ooag011,'无') 业务员 from  xrcc_t left join xrca_t on xrccent = xrcaent and xrccld = xrcald and xrccdocno = xrcadocno left join pmaal_t on xrcaent=pmaalent and xrca005 = pmaal001 and pmaal002='zh_CN' left join ooag_t on xrcaent = ooagent and xrca014=ooag001 where xrccent = '60' and xrcc108<>xrcc109 and xrca001 in ('12','17') and xrccld in ('Y1','Y3','Y4','YM') and xrcc003<sysdate+7 group by ooag011 order by  ooag011"
    # cur.execute(xxx)
    # res = cur.fetchall()
    #
    # for tao1 in res:
    #     yy=tao1[0]
    #     xx=0
    #     xxx = "select xrca005||':'||pmaal004 客户,xrccdocno 应收账款单,xrccseq 项次,xrcc108-xrcc109 原币待收,xrca100 币种,xrcc118-xrcc119 本币待收,xrcc003 应收款日,NVL(ooag011,'无') 业务员,xrccld 账套 from  xrcc_t left join xrca_t on xrccent = xrcaent and xrccld = xrcald and xrccdocno = xrcadocno left join pmaal_t on xrcaent=pmaalent and xrca005 = pmaal001 and pmaal002='zh_CN' left join ooag_t on xrcaent = ooagent and xrca014=ooag001 where xrccent = '60' and xrcc108<>xrcc109 and xrca001 in ('12','17') and xrccld in ('Y1','Y3','Y4','YM') and xrcc003<sysdate+7 and ooag011='%s'" % (yy)
    #     cur.execute(xxx)
    #     res1 = cur.fetchall()
    #     r10 = ''
    #     bb = 0
    #     title = yy+':未来1周应收款到期'
    #
    #     for tao in res1:
    #         xx = xx + 1
    #         r0 = '.客户：' + tao[0] + ',应收账款单:' + tao[1] + '-' + str(tao[2]) + ',应收原币：' + str(tao[3]) + tao[
    #             4] + ',应收本币:' + str(tao[5]) + ',应收款日:' + datetime.datetime.strftime(tao[6], "%Y-%m-%d")
    #         bb = bb + tao[5]
    #         r10 = r10 + str(xx) + r0 + '\n'
    #     try:
    #         bb = round(bb)
    #         r10 = '未来1周应收款到期(' + str(xx) + '项,应收本币共' + str(format(bb, ",")) + '元[' + yy + ']):\n' + r10
    #         tosend = yy + '|周洪|劳威芳|方苑茹|鲁红斌'
    #         getr10(r10, tosend,title)
    #     except:
    #         r10 = yy+'业务员已离职！' + r10
    #         tosend = '周洪|劳威芳|方苑茹|鲁红斌'
    #         getr10(r10, tosend,title)

    #####复检申请请处理

    xxx = "select qcbauc004 检验员 from qcbauc_t where qcbaucstus='N'  group by qcbauc004 order by qcbauc004"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy=tao1[0]
        if yy == None:
            yy = '没写检验员'
        xx=0
        xxx = "select qcbaucdocno 复检申请单号,qcbauc004 检验员 from qcbauc_t where qcbaucstus='N' and qcbauc004='%s'" % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy+':复检申请请处理'
        print(yy)
        yy = yy.replace(',', '|')
        for tao in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.单号：' + tao[0] + '已生成 请及时复检' + '\n'
        # try:
        r10 = '复检申请请处理(' + str(xx) + '项,[' + yy + ']):\n\n' + r10

        if yy == 'xxx':
            tosend = 'xxx|llll'
        else:
            tosend = yy + '|xxx|llll'
        getr10(r10, tosend,title)
        # except:
            # r10 = yy+':检验员已离职！' + r10
            # tosend = '周洪|鲁红斌'
            # tosend = yy + '|周洪|鲁红斌'
            # getr10(r10, tosend,title)


    #####检验不合格验退请处理
    xxx = "select NVL(a.ooag011,'无') 仓管员,NVL(b.ooag011,'无') 采购员 from qcba_t left join pmdt_t on qcbaent=pmdtent and qcbasite=pmdtsite and qcbadocno=pmdt081 left join pmds_t on pmdtent=pmdsent and pmdtsite=pmdssite and pmdtdocno=pmdsdocno left join pmdl_t on qcbaent=pmdlent and qcbasite=pmdlsite and qcba003=pmdldocno left join ooag_t a on qcbaent=a.ooagent and  qcba900=a.ooag001 left join ooag_t b on pmdlent=b.ooagent and  pmdlcrtid=b.ooag001 where qcba000='1' and qcba022='2' and qcbaent='60' and (pmdt081 is null or pmdt081 is not null and pmdsstus='N') group by b.ooag011,a.ooag011 order by b.ooag011,a.ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy=tao1[1]
        yy1=tao1[0]
        xx=0
        aa = 0
        xxx = "select NVL(qcbasite,'') 据点,NVL(qcbadocno,'') 检验单号,NVL(qcba027,0) 验退量,NVL(qcba001,'') 进货单号,NVL(qcba002,0) 进货项次,NVL(qcba003,'') 采购单号,NVL(pmdtdocno,'') 验退单号,NVL(qcba010,'') 料号,NVL(imaal003,'') 品名,NVL(imaal004,'') 规格,NVL(qcbaud001,'') 订单号 from qcba_t left join pmdt_t on qcbaent=pmdtent and qcbasite=pmdtsite and qcbadocno=pmdt081 left join pmds_t on pmdtent=pmdsent and pmdtsite=pmdssite and pmdtdocno=pmdsdocno left join pmdl_t on qcbaent=pmdlent and qcbasite=pmdlsite and qcba003=pmdldocno left join ooag_t a on qcbaent=a.ooagent and  qcba900=a.ooag001 left join ooag_t b on pmdlent=b.ooagent and  pmdlcrtid=b.ooag001 left join imaal_t on qcbaent=imaalent and qcba010=imaal001 and imaal002='zh_CN' where qcba000='1' and qcba022='2' and qcbaent='60' and (pmdt081 is null or pmdt081 is not null and pmdsstus='N') and b.ooag011='%s'  and a.ooag011='%s'" % (yy,yy1)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy+'/'+yy1+':检验不合格验退请处理'

        for tao in res1:
            xx = xx + 1
            print(str(xx) + '.' + tao[0] + ',检验单号:' + tao[1] + ',验退量：' + str(tao[2]) + ',进货单号:' + tao[3]+'-' + str(tao[4]))
            print(',采购单号:' + tao[5])
            try:
                print(', 验退单号:' + tao[6])
                tap6=tao[6]
            except:
                tap6=''
            try:
                print(', 验退单号:' +  tao[10])
                tap10= tao[10]
            except:
                tap10=''
            try:
                print('[' + tao[8] + ',' + tao[9] + '], 订单号:' + tap10)
                print(', 验退单号:' +  tao[8])
                tap8= tao[8]
            except:
                tap8=''
            try:
                print(', 验退单号:' +  tao[9])
                tap9= tao[9]
            except:
                tap9=''
            print(',产品:' + tao[7])
            r10 = r10 + str(xx) + '.' + tao[0] + ',检验单号:' + tao[1] + ',验退量：' + str(tao[2]) + ',进货单号:' + tao[3]+'-' + str(tao[4]) + ',采购单号:' + tao[5] + ', 验退单号:' + tap6+',产品:' + tao[7] + '[' + tap8 + ',' + tap9 + '], 订单号:' + tap10 + '\n'
            aa = aa + tao[2]
        try:
            r10 = '检验不合格验退请处理(' + str(xx) + '项, 验退量共' + str(format(aa, ","))+'件[' + yy + '/' + yy1 + ']),请及时处理验退信息:\n\n' + r10

            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend,title)
        except:
            tosend = 'xxx|llll'
            getr10(r10, tosend,title)

    ####供应商据点信息缺失
    xxx = "select NVL(ooag011,'无') 维护人员 from pmab_t inner join pmaa_t on pmabent = pmaaent and pmab001 = pmaa001  left join pmaal_t  on  pmabent = pmaalent and pmab001 = pmaal001 and pmaal002 = 'zh_CN'  left join ooag_t  on pmabent = ooagent and pmabcrtid = ooag001 where pmabent = '60' and pmabsite not in ('ALL', 'Y2', 'US', 'EU', 'Y3', 'SITE-01') and pmaa002 in ('1', '3') and pmaa083 <> '30' and  ( pmab031 is null or pmab059 is null or pmab033 is null or pmab034 is null or pmab053 is null or pmab054 is null or pmab056 is null or pmab057 is null or pmab058 is null or (pmab052 is null and pmab051='Y')) group by ooag011 order by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy=tao1[0]
        xx=0
        xxx = "select NVL(pmabsite,'无') 据点,pmab001||':'||pmaal004 供应商,NVL(ooag011,'无') 维护人员 from pmab_t inner join pmaa_t on pmabent = pmaaent and pmab001 = pmaa001  left join pmaal_t  on  pmabent = pmaalent and pmab001 = pmaal001 and pmaal002 = 'zh_CN'  left join ooag_t  on pmabent = ooagent and pmabcrtid = ooag001 where pmabent = '60' and pmabsite not in ('ALL', 'Y2', 'US', 'EU', 'Y3', 'SITE-01') and pmaa002 in ('1', '3') and pmaa083 <> '30' and  ( pmab031 is null or pmab059 is null or pmab033 is null or pmab034 is null or pmab053 is null or pmab054 is null or pmab056 is null or pmab057 is null or pmab058 is null or (pmab052 is null and pmab051='Y')) and ooag011='%s'" % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy+':供应商据点信息缺失'
        for tao in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao[0] + ',供应商:' + tao[1] + '\n'
        try:
            r10 = '供应商据点信息缺失，请补充完整(' + str(xx) + '项,[' + yy + ']):\n\n' + r10

            if yy == 'xxx':
                tosend = 'xxx|llll|yyyy'
            else:
                tosend = yy + '|xxx|llll|yyyy'
            getr10(r10, tosend,title)
        except:
            tosend = 'xxx|llll|yyyy'

            getr10(r10, tosend,title)

    # #####客户据点信息缺失
    title ='客户据点信息缺失'
    xxx = "select  NVL(pmabsite,'无') 据点,pmab001||':'||pmaal004 客户 from pmab_t inner join pmaa_t on pmabent=pmaaent and pmab001=pmaa001 left join pmaal_t on pmabent=pmaalent and pmab001=pmaal001 and pmaal002='zh_CN' where pmabent='60' and pmabsite not in ('ALL','Y2','US','EU','Y3','SITE-01') and pmaa002 in ('2','3') and (pmab081 is null or pmab109 is null or pmab083 is null or pmab084 is null or pmab103 is null or pmab104 is null or pmab106 is null  or pmab087 is null or pmab107 is null or pmab108 is null ) "
    cur.execute(xxx)
    res = cur.fetchall()
    xx = 0
    r10 = ''
    for tao in res:
        r0 = '.' + tao[0] + ',客户:' + tao[1]
        xx = xx + 1
        r10 = r10 + str(xx) + r0 + '\n'

    time.sleep(5)
    r10 = '客户据点信息缺失，请补充完整(' + str(xx) + '项):\n\n' + r10
    tosend = 'tttt|xxxxx'
    # getr10(r10, tosend, title)

    # #####料件生命周期不同
    xxx = "select NVL(ooag011,'无') 录入者 from imaf_t left join imaa_t on imafent=imaaent and imaf001=imaa001 left join ooag_t on imafent=ooagent and imafcrtid=ooag001 where imafent='60' and imaf016<>imaa010 and imafsite in ('ALL','Y1','Y4','YM') group by ooag011 order by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy=tao1[0]
        xx=0
        xxx = "select NVL(imafsite,'无') 据点,NVL(imaf001,'无') 料号,NVL(imaf016,'无') 据点生命周期,NVL(imaa010,'无') 料号生命周期,NVL(ooag011,'无') 录入者 from imaf_t left join imaa_t on imafent=imaaent and imaf001=imaa001 left join ooag_t on imafent=ooagent and imafcrtid=ooag001 where imafent='60' and imaf016<>imaa010 and imafsite in ('ALL','Y1','Y4','YM') and ooag011='%s'" % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy+':料件生命周期不同'
        for tao in res1:
            xx = xx + 1
            r10 = r10+str(xx)+'.' + tao[0] + ',料号:' + tao[1] + ',据点生命周期:' + tao[2] + ',料号生命周期:' + tao[3]+ '\n'
        try:
            r10 = '料件生命周期不同，请核改正确(' + str(xx) + '项,[' + yy + ']):\n\n' + r10

            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + 'xxx|llll'
            getr10(r10, tosend, title)
        except:
            r10 = yy+'录入员已离职！' + r10
            tosend = 'xxx|llll'
            getr10(r10, tosend, title)

    # #####采购员离职，提醒数据维护
    xxx = "select pmabsite 据点 from pmab_t inner join pmaa_t on pmabent=pmaaent and pmab001=pmaa001 left join pmaal_t on pmaaent=pmaalent and pmaa001=pmaal001 and pmaal002='zh_CN' left join ooag_t on pmabent=ooagent and pmab031=ooag001 where pmabent='60' and pmabsite in ('Y1','Y4','YM') and pmaa002 in ('1','3') and ooagstus='N' and pmaa083 in ('10','20') GROUP BY pmabsite"
    cur.execute(xxx)
    res = cur.fetchall()
    for tao1 in res:
        yy=tao1[0]
        xxx = "select pmabsite 据点,pmab001||':'||pmaal004 供应商,ooag011 采购员 from pmab_t inner join pmaa_t on pmabent=pmaaent and pmab001=pmaa001 left join pmaal_t on pmaaent=pmaalent and pmaa001=pmaal001 and pmaal002='zh_CN' left join ooag_t on pmabent=ooagent and pmab031=ooag001 where pmabent='60' and pmabsite in ('Y1','Y4','YM') and pmaa002 in ('1','3') and ooagstus='N' and pmaa083 in ('10','20') and pmabsite='%s'" % (yy)
        cur.execute(xxx)
        res = cur.fetchall()
        xx = 0
        r10 = ''
        aa = 0
        for tao in res:
            r0 = '.' + tao[0] + ',' + str(tao[1]) + '[' + str(tao[2]) + ']'
            aa = aa + 1
            xx = xx + 1
            r10 = r10 + str(xx) + r0 + ';'
        title ='采购员离职数据维护'
        try:
            r10 = '采购员离职请数据维护(' + str(xx) + '条):\n\n' + r10
            if tao[0] == 'YM':
                tosend = 'xxx|llll'
            else:
                tosend = 'xxx|llll'
            getr10(r10, tosend, title)
        except:
            r10 = '采购员已离职！请数据维护' + r10
            if tao[0] == 'YM':
                tosend = 'xxx|llll'
            else:
                tosend = 'xxx|llll'
            getr10(r10, tosend, title)


    # #####供应商据点付款条件缺失，提醒数据维护
    xxx = "select pmabsite 据点,pmab001||':'||pmaal004 供应商,ooag011 维护人员 from pmab_t inner join pmaa_t on pmabent=pmaaent and pmab001=pmaa001 left join pmaal_t on pmabent=pmaalent and pmab001=pmaal001 and pmaal002='zh_CN' left join ooag_t on pmabent=ooagent and pmabcrtid=ooag001 where pmabent='60' and pmabsite not in ('ALL','Y2','US','EU','Y3','SITE-01') and pmaa002 in ('1','3') and pmaa083<>'30' and pmab037 is null"
    cur.execute(xxx)
    res = cur.fetchall()
    xx = 0
    r10 = ''
    aa = 0
    for tao in res:
        r0 = '.' + tao[0] + ',' + str(tao[1]) + '[' + str(tao[2]) + ']'
        aa = aa + 1
        xx = xx + 1
        r10 = r10 + str(xx) + r0 + ';'
    title ='供应商据点付款条件缺失'
    try:
        r10 = '供应商据点 付款条件缺失,请数据维护(' + str(xx) + '条):\n\n' + r10
        tosend = 'xxx|llll'
        getr10(r10, tosend, title)
    except:
        print('供应商据点付款条件缺失')

    # #####厂内工单的工单工艺是委外工单的请变更
    xxx = "select ooag011 录入人员 from sfaa_t inner join sfcb_t on sfaaent=sfcbent and sfaasite=sfcbsite and sfaadocno=sfcbdocno left join ooag_t on sfaaent=ooagent and sfaacnfid=ooag001 where sfaastus='F' and sfcb012='Y' and sfaaent='60' and sfaasite='Y1' and sfaa057='1' and sfaa061='Y' group by ooag011 order by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy=tao1[0]
        xx=0
        xxx = "select sfaadocno 工单号,ooag011 录入人员 from sfaa_t inner join sfcb_t on sfaaent=sfcbent and sfaasite=sfcbsite and sfaadocno=sfcbdocno left join ooag_t on sfaaent=ooagent and sfaacnfid=ooag001 where sfaastus='F' and sfcb012='Y' and sfaaent='60' and sfaasite='Y1' and sfaa057='1' and sfaa061='Y' and ooag011='%s'" % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy+':厂内工单是委外请变更'
        for tao2 in res1:
            xx = xx + 1
            r10=str(xx)+'.'+tao2[0]+';'
        try:
            r10 = '厂内工单的工单工艺是委外工单的请变更(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            # r10 = yy+'录入员已离职！' + r10
            tosend = '周洪|鲁红斌'
            tosend = yy + '|周洪|鲁红斌'
            getr10(r10, tosend, title)

    # #####PI已经评审完成，请及时转正
    conn2 = cx_Oracle.connect('dsdata/dsdata@192.168.0.5:1521/TOPPRD')
    cur = conn2.cursor()
    xxx = "select ooag011 业务员 from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%2299%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdaua011>0 and to_date(sysdate)-xmdaua011<=3 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdaua011 d from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%%2299%%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdaua011>0 and to_date(sysdate)-xmdaua011<=3 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':PI已经评审完成'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(tao2[3]) + '天);\n'
        try:
            r10 = 'PI已经评审完成，请及时转正！七天内未转正，自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'
            getr10(r10, tosend, title)

    xxx = "select ooag011 业务员 from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%2299%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdadocdt>3 and to_date(sysdate)-xmdaua011<=5 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdaua011 d from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%%2299%%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdadocdt>3 and to_date(sysdate)-xmdaua011<=5 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':PI已经评审完成超4天'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(
                tao2[3]) + '天);\n'
        try:
            r10 = 'PI已经评审完成，请及时转正！七天内未转正，自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                if yy == 'xxx':
                    tosend = 'xxx|llll'
                else:
                    tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = yy + '|xxx|llll'

            getr10(r10, tosend, title)

    xxx = "select ooag011 业务员 from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%2299%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdadocdt>5 and to_date(sysdate)-xmdaua011<=6 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdaua011 d from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%%2299%%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdadocdt>5 and to_date(sysdate)-xmdaua011<=6 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':PI已经评审完成超5天'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(
                tao2[3]) + '天);\n'
        try:
            r10 = 'PI已经评审完成，请及时转正！七天内未转正，自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                if yy == 'xxx':
                    tosend = 'xxx|llll'
                else:
                    tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = yy + '|xxx|llll'

            getr10(r10, tosend, title)

    xxx = "select ooag011 业务员 from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%2299%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdaua011>6 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdaua011 业务员 from xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5'  AND xmdastus = 'Y' AND xmdaua011 is not null AND xmdadocno LIKE '%%2299%%' AND (xmdaua008 = '6' OR xmdaua008 = '7') and to_date(sysdate)-xmdaua011>6 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':PI已经评审完成超过6天'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(tao2[3]) + '天);\n'
        try:
            r10 = 'PI已经评审完成，请及时转正！七天内未转正，自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                if yy == 'xxx':
                    tosend = 'xxx|llll'
                else:
                    tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'

            getr10(r10, tosend, title)
    # #####订单请及时审核

    xxx = "SELECT ooag011 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%2299%' and to_date(sysdate)-xmdadocdt>0 and to_date(sysdate)-xmdadocdt<=3 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "SELECT xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdadocdt 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%%2299%%' and to_date(sysdate)-xmdadocdt>0 and to_date(sysdate)-xmdadocdt<=3 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':订单请及时审核'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(
                tao2[3]) + '天);\n'
        try:
            r10 = '订单请及时审核！七天内未审核自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'

            getr10(r10, tosend, title)

    xxx = "SELECT ooag011 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%2299%' and to_date(sysdate)-xmdadocdt>3 and to_date(sysdate)-xmdadocdt<=5 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "SELECT xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdadocdt 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%%2299%%' and to_date(sysdate)-xmdadocdt>3 and to_date(sysdate)-xmdadocdt<=5 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':订单超过4天 请及时审核'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(
                tao2[3]) + '天);\n'
        try:
            r10 = '订单请及时审核！七天内未审核自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = yy + '|xxx|llll'

            getr10(r10, tosend, title)

    xxx = "SELECT ooag011 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%2299%' and to_date(sysdate)-xmdadocdt>5 and to_date(sysdate)-xmdadocdt<=6 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "SELECT xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdadocdt 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%%2299%%' and to_date(sysdate)-xmdadocdt>5 and to_date(sysdate)-xmdadocdt<=6 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':订单超过5天 请及时审核'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(
                tao2[3]) + '天);\n'
        try:
            r10 = '订单请及时审核！七天内未审核自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = yy + '|xxx|llll'

            getr10(r10, tosend, title)

    xxx = "SELECT ooag011 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%2299%' and to_date(sysdate)-xmdadocdt>6 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "SELECT xmdasite 据点,xmdadocno PI号,xmdadocdt 录入日期,to_date(sysdate)-xmdadocdt 业务员 FROM xmda_t left join ooag_t on xmdaent=ooagent and xmda002=ooag001 WHERE xmdaent = '60' AND xmda006 <> '5' AND xmdastus = 'N' AND xmdadocno NOT LIKE '%%2299%%' and to_date(sysdate)-xmdadocdt>6 and ooag011='%s'" % (
            yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':订单超过6天 请及时审核'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.' + tao2[1] + '.' + datetime.datetime.strftime(tao2[2], "%Y-%m-%d") + '(超过' + str(
                tao2[3]) + '天);\n'
        try:
            r10 = '订单请及时审核！七天内未审核自动作废！(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'

            getr10(r10, tosend, title)

    # xxx = "select ooag011 采购员 from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142  when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 else 'Y00106' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 in ('1','3') and (substr(inag001,1,1) in ('0','1','2','3','4') or (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201'))) and to_date(sysdate)-inag015>0 and to_date(sysdate)-inag015<=5  and inag015>='12-7月-21'  group by ooag011"
    # xxx = "select ooag011 采购员 from inag_t left join (select inaj005,inaj007,inaj008,inaj009,inaj010,sum(inaj004*inaj011) inaj011 from inaj_t where inajent='60' and inajsite='Y1' and inaj008='98' and (substr(inaj005,1,1) in ('0','1','2','3','4') or (substr(inaj005,1,1) in ('5','6','7','8','9') and substr(inaj010,4,4) not in ('2200','2201')))  and inaj022>='12-7月-21'  group by inaj005,inaj007,inaj008,inaj009,inaj010 ) a2  on inag001=a2.inaj005 and inag003=a2.inaj007 and inag004=a2.inaj008 and inag005=a2.inaj009  and inag006=a2.inaj010  left join (select max(inaj022) inaj022,inaj005,inaj007,inaj008,inaj009,inaj010 from inaj_t where inajent='60' and inajsite='Y1' and inaj008='98' and (substr(inaj005,1,1) in ('0','1','2','3','4') or  (substr(inaj005,1,1) in ('5','6','7','8','9') and substr(inaj010,4,4) not in ('2200','2201')))  and inaj022>='12-7月-21' group by inaj005,inaj007,inaj008,inaj009,inaj010) a3 on inag001=a3.inaj005 and inag003=a3.inaj007 and inag004=a3.inaj008 and inag005=a3.inaj009 and inag006=a3.inaj010 left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001  left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142  when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 else 'Y00106' end) =ooag001 where inagent='60' and inagsite='Y1' and inag004='98' and inag008>0 and (substr(inag001,1,1) in ('0','1','2','3','4') or  (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201')))  and a2.inaj011>0  and imaf013 in ('1','3')   and to_date(sysdate)-a3.inaj022>0 and to_date(sysdate)-a3.inaj022<=5 group by ooag011"
    #xxx = "select ooag011 采购员,  inag001  料号, imaal003 品名, imaal004  规格, inag008 数量, a3.inaj022 日期, from inag_t left  join (select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group  by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when imaf013 in ('1', '3') then imaf142 when imaf013 = '2' and substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') then ooeg011 else 'Y00106' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 in ('1', '3') and to_date(sysdate) - a3.inaj022 > 0 and to_date(sysdate) - a3.inaj022 <= 5"
    xxx = "select ooag011 采购员 from inag_t left  join (select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group  by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when imaf013 in ('1', '3') then imaf142 when imaf013 = '2' and substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') then ooeg011 else 'Y00106' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 in ('1', '3') and to_date(sysdate) - a3.inaj022 > 0 and to_date(sysdate) - a3.inaj022 <= 5 group by ooag011"

    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无')  品名,NVL(imaal004,'无') 规格,inag008 数量,a3.inaj022 日期,to_date(sysdate)-a3.inaj022 rq from inag_t left  join (select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group  by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when imaf013 in ('1', '3') then imaf142 when imaf013 = '2' and substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') then ooeg011 else 'Y00106' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 in ('1', '3') and to_date(sysdate) - a3.inaj022 > 0 and to_date(sysdate) - a3.inaj022 <= 5 and ooag011='%s'" % (yy)
        # xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,inag008 数量,inag015 日期,to_date(sysdate)-inag015 rq from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142  when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 else 'Y00106' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 in ('1','3') and (substr(inag001,1,1) in ('0','1','2','3','4') or (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201'))) and to_date(sysdate)-inag015>0 and to_date(sysdate)-inag015<=5  and inag015>='12-7月-21' and ooag011='%s'" % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':待处理品库库存5天内 请及时处理'
        for tao2 in res1:
            xx = xx + 1
            r10 = r10 + str(xx) + '.[' + tao2[0] + ']' + tao2[1] + ':' + tao2[2] + '(数量:' + str(
                tao2[3]) + ').' + datetime.datetime.strftime(tao2[4], "%Y-%m-%d") + '(超' + str(tao2[5]) + '天);\n'
        try:
            r10 = '待处理品库库存5天内 请及时处理(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'

            getr10(r10, tosend, title)

    xxx = "select ooag011 采购员 from inag_t left  join (select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group  by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when imaf013 in ('1', '3') then imaf142 when imaf013 = '2' and substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') then ooeg011 else 'Y00106' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 in ('1', '3') and to_date(sysdate) - a3.inaj022 > 0 and to_date(sysdate) - a3.inaj022 > 5 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无')  品名,NVL(imaal004,'无') 规格,inag008 数量,a3.inaj022 日期,to_date(sysdate)-a3.inaj022 rq from inag_t left  join (select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group  by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when imaf013 in ('1', '3') then imaf142 when imaf013 = '2' and substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') then ooeg011 else 'Y00106' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 in ('1', '3') and to_date(sysdate) - a3.inaj022 > 0 and to_date(sysdate) - a3.inaj022 > 5 and ooag011='%s'" % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':待处理品库库存超过5天 请及时处理'
        for tao2 in res1:
            xx = xx + 1
            try:
                r10 = r10 + str(xx) + '.[' + tao2[0] + ']' + tao2[1] + ':' + tao2[2] + '(数量:' + str(
                    tao2[3]) + ').' + datetime.datetime.strftime(tao2[4], "%Y-%m-%d") + '(超' + str(tao2[5]) + '天);\n'
            except:
                print(tao2[0], tao2[1], tao2[2], tao2[3], tao2[4], tao2[5])
        try:
            r10 = '待处理品库库存超过5天 请及时处理(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'

            getr10(r10, tosend, title)

#    xxx = "select ooag011 人员 from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142 when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when xmda002 is not null then xmda002 else 'Y00039' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 = '2' and (substr(inag001,1,1) in ('0','1','2','3','4') or  (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201'))) and to_date(sysdate)-inag015>0  and inag015>='12-7月-21'  group by ooag011"
    xxx = "select  ooag011 人员 from inag_t left join(select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022)  inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join ooag_t on ooagent=60 and (case when substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,1,18)=xmdadocno then xmda002 else 'Y00039' end) =ooag001  where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 = '2' and to_date(sysdate) - inag015 > 0  group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        # xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,NVL(inag008,0) 数量,inag015 日期,to_date(sysdate)-inag015 rq,NVL(inag006,'无') 批号 from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142 when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when xmda002 is not null then xmda002 else 'Y00039' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 = '2' and (substr(inag001,1,1) in ('0','1','2','3','4') or  (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201'))) and to_date(sysdate)-inag015>0  and inag015>='12-7月-21' and ooag011='%s'" % ( yy)
        xxx = "select  NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,NVL(inag008,0) 数量, a3.inaj022  日期,to_date(sysdate)- a3.inaj022 rq, substr(inag006, 1, 18)  订单号 from inag_t left join(select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022)  inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join ooag_t on ooagent=60 and (case when substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,1,18)=xmdadocno then xmda002 else 'Y00039' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 = '2' and to_date(sysdate) - inag015 > 0 and ooag011='%s'" % (yy)

        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':自制待处理品库库存请及时处理'
        for tao2 in res1:
            xx = xx + 1
            try:
                r10 = r10 + str(xx) + '.[' + tao2[0] + ']' + tao2[1] + ':' + tao2[2] + '(数量:' + str(tao2[3]) + ')' \
                      + tao2[6] + '.' + datetime.datetime.strftime(tao2[4], "%Y-%m-%d") + '(超' + str(tao2[5]) + '天);\n'
            except:
                print(tao2[0], tao2[1], tao2[2], tao2[3], tao2[4], tao2[5], tao2[6])
        try:
            r10 = '自制待处理品库库存请及时处理(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'
            getr10(r10, tosend, title)


    #xxx = "select  ooag011 人员 from inag_t left join(select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022)  inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when imaf013 in ('1', '3') then imaf142 when imaf013 = '2' and substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') then ooeg011 else 'Y00039' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and a2.inaj011 > 0 and imaf013 = '2' and to_date(sysdate) - inag015 > 0"
    xxx = "select ooag011 仓管员 from pmds_t inner join pmdt_t on pmdsent = pmdtent and pmdssite = pmdtsite and pmdsdocno = pmdtdocno left join ooag_t on pmdsent = ooagent and pmdscrtid = ooag001  where pmdsent = '60' and pmdssite = 'Y1' and pmdsstus = 'Y' and pmdt026 = 'Y' and pmds000 in ('1', '8') and pmdt053 > 0 and pmdt054 = 0 group by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        # xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,NVL(inag008,0) 数量,inag015 日期,to_date(sysdate)-inag015 rq,NVL(inag006,'无') 批号 from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142 when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when xmda002 is not null then xmda002 else 'Y00039' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 = '2' and (substr(inag001,1,1) in ('0','1','2','3','4') or  (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201'))) and to_date(sysdate)-inag015>0  and inag015>='12-7月-21' and ooag011='%s'" % ( yy)
        xxx = "select pmdsdocno 单号 from pmds_t inner join pmdt_t on pmdsent = pmdtent and pmdssite = pmdtsite and pmdsdocno = pmdtdocno left join ooag_t on pmdsent = ooagent and pmdscrtid = ooag001  where pmdsent = '60' and pmdssite = 'Y1' and pmdsstus = 'Y' and pmdt026 = 'Y' and pmds000 in ('1', '8') and pmdt053 > 0 and pmdt054 = 0  and ooag011='%s' group by pmdsdocno" % ( yy)

        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':收货单已检验完成请及时入库'
        for tao2 in res1:
            xx = xx + 1
            try:
                r10 = r10 + str(xx) + '.' + tao2[0] + '\n'
            except:
                print(tao2[0])
        try:
            r10 = '收货单已检验完成请及时入库(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'
            getr10(r10, tosend, title)
    cur.close

    # if os.path.exists("qcbadocno.txt"):
    #     try:
    #         os.remove("qcbadocno.txt")
    #     except:
    #         f.closed
    #         os.remove("qcbadocno.txt")
    # cur.close
def get_kc():
    # #####PI已经评审完成，请及时转正
    conn2 = cx_Oracle.connect('dsdata/dsdata@192.168.0.5:1521/TOPPRD')
    cur = conn2.cursor()
    xxx = "select ooag011 采购员 from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142  when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 else 'Y00106' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 in ('1','3') and (substr(inag001,1,1) in ('0','1','2','3','4') or (substr(inag001,1,1) in ('5','6','7','8','9') and inag015<'12-7月-21' group by ooag011"
    xxx = "select  case when  ooag011 is null  then 'xxx' else ooag011 end 人员 from inag_t left join(select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010 ) a2 on inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201')))  and inaj004 = '1'  and inaj022 < '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when ooagstus='Y' then imaf052 else 'Y00026' end) = ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and (a2.inaj011 <= 0 or a2.inaj011 is null) and imaf013 in ('1', '3') group by  case when  ooag011 is null  then '杨海波' else ooag011 end"

    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,NVL(inag008,0) 数量,inag015 日期,to_date(sysdate)-inag015 rq from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142  when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 else 'Y00106' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 in ('1','3') and (substr(inag001,1,1) in ('0','1','2','3','4') or (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201')))  and inag015<'12-7月-21'  and ooag011='%s'" % (
            yy)
        xxx = "select  NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,NVL(inag008,0) 数量, a3.inaj022  日期,to_date(sysdate)-a3.inag015 rq from inag_t left join(select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201'))) and inaj022 >= '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010 ) a2 on inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98'  and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201')))  and inaj004 = '1'  and inaj022 < '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join ooag_t on ooagent = 60 and (case when ooagstus='Y' then imaf052 else 'Y00026' end) = ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and (a2.inaj011 <= 0 or a2.inaj011 is null) and imaf013 in ('1', '3') and ,  case when  ooag011 is null  then '杨海波' else ooag011 end 人员 ='%s'" % (yy)

        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':采购待处理品库超15天库存请及时处理！'
        for tao2 in res1:
            xx = xx + 1
            try:
                r10 = r10 + str(xx) + '.[' + tao2[0] + ']' + tao2[1] + ':' + tao2[2] + '(数量:' + str(
                    tao2[3]) + ').' + datetime.datetime.strftime(tao2[4], "%Y-%m-%d") + '(超' + str(tao2[5]) + '天);\n'
            except:
                print(tao2[0], tao2[1], tao2[2], tao2[3], tao2[4], tao2[5])
        try:
            r10 = '待处理品库库存超过15天 请及时处理(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'

            getr10(r10, tosend, title)

    xxx = "select ooag011 人员 from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142 when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when xmda002 is not null then xmda002 else 'Y00039' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 = '2' and (substr(inag001,1,1) in ('0','1','2','3','4') or  (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201')))  and inag015<'12-7月-21'  group by ooag011"
    xxx = "select ooag011 人员 from inag_t left join (select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group  by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t   where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201')))  and inaj004 = '1' and inaj022 < '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join ooag_t on ooagent=60 and (case when substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,1,18)=xmdadocno then xmda002 else 'Y00039' end) =ooag001  where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and (a2.inaj011 <= 0 or a2.inaj011 is null) and imaf013 = '2'  group by ooag011"

    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy = tao1[0]
        xx = 0
        xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,NVL(inag008,0) 数量,inag015 日期,to_date(sysdate)-inag015 rq,NVL(inag006,'无') 批号 from inag_t left join imaf_t on inagent=imafent and inagsite=imafsite and inag001=imaf001 left join imae_t on inagent=imaeent and inagsite=imaesite and inag001=imae001 left join ooeg_t on imaeent=ooegent and imae035=ooeg001 left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join imaal_t on inagent=imaalent and inag001=imaal001 and imaal002='zh_CN' left join ooag_t on ooagent=60 and (case when imaf013 in ('1','3') then imaf142 when imaf013 = '2' and substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when xmda002 is not null then xmda002 else 'Y00039' end) =ooag001 where inagent=60 and inagsite='Y1' and inag008>0 and inag004='98' and imaf013 = '2' and (substr(inag001,1,1) in ('0','1','2','3','4') or  (substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,4,4) not in ('2200','2201')))  and inag015<'12-7月-21'  and ooag011='%s'" % (
            yy)
        xxx = "select NVL(inag001,'无') 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格, inag008 数量, a3.inaj022 日期,to_date(sysdate)-a3.inaj022 rq,substr(inag006, 1, 18) 订单号 from inag_t left join (select inaj005, inaj007, inaj008, inaj009, inaj010, sum(inaj004 * inaj011) inaj011 from inaj_t  where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inaj005, 1, 1) in ( '5', '6', '7', '8', '9') and substr(inaj010, 4, 4) not in ( '2200', '2201'))) and inaj022 >= '12-7月-21'  group  by  inaj005, inaj007, inaj008, inaj009, inaj010 ) a2  on  inag001 = a2.inaj005 and inag003 = a2.inaj007 and inag004 = a2.inaj008 and inag005 = a2.inaj009 and inag006 = a2.inaj010 left join(select max(inaj022) inaj022, inaj005, inaj007, inaj008, inaj009, inaj010 from inaj_t   where inajent = '60' and inajsite = 'Y1' and inaj008 = '98' and (substr(inaj005, 1, 1) in ('0', '1', '2', '3', '4') or  (substr(inaj005, 1, 1) in ('5', '6', '7', '8', '9') and substr( inaj010, 4, 4) not in ('2200', '2201')))  and inaj004 = '1' and inaj022 < '12-7月-21' group by inaj005, inaj007, inaj008, inaj009, inaj010) a3 on inag001 = a3.inaj005 and inag003 = a3.inaj007 and inag004 = a3.inaj008 and inag005 = a3.inaj009 and inag006 = a3.inaj010 left join imaf_t on inagent = imafent and inagsite = imafsite and inag001 = imaf001 left join imae_t on inagent = imaeent and inagsite = imaesite and inag001 = imae001 left join ooeg_t on imaeent = ooegent and imae035 = ooeg001 left join imaal_t on inagent = imaalent and inag001 = imaal001 and imaal002 = 'zh_CN' left join xmda_t on inagent=xmdaent and inagsite=xmdasite and substr(inag006,1,18)=xmdadocno left join ooag_t on ooagent=60 and (case when substr(inag001,1,1) in ('0','1','2','3','4') then ooeg011 when substr(inag001,1,1) in ('5','6','7','8','9') and substr(inag006,1,18)=xmdadocno then xmda002 else 'Y00039' end) =ooag001 where inagent = '60' and inagsite = 'Y1' and inag004 = '98' and inag008 > 0 and (substr(inag001, 1, 1) in ('0', '1', '2', '3', '4') or (substr(inag001, 1, 1) in ('5', '6', '7', '8', '9') and substr(inag006, 4, 4) not in ('2200', '2201'))) and (a2.inaj011 <= 0 or a2.inaj011 is null) and imaf013 = '2' and ooag011='%s'" % (yy)

        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy + ':自制待处理品库历史库存请及时处理'
        for tao2 in res1:
            xx = xx + 1
            try:
                r10 = r10 + str(xx) + '.[' + tao2[0] + ']' + tao2[1] + ':' + tao2[2] + '(数量:' + str(tao2[3]) + ')' \
                      + tao2[6] + '.' + datetime.datetime.strftime(tao2[4], "%Y-%m-%d") + '(超' + str(tao2[5]) + '天);\n'
            except:
                print(tao2[0], tao2[1], tao2[2], tao2[3], tao2[4], tao2[5], tao2[6])
        try:
            r10 = '自制待处理品库历史库存请及时处理(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'
            getr10(r10, tosend, title)
    cur.close

def get_t100zfix():

    conn2 = cx_Oracle.connect('dsdata/dsdata@192.168.0.5:1521/TOPPRD')
    cur = conn2.cursor()
    # #####周计划更改采购交期
    xxx = "select ooag011 采购员 from sfahuc_t left join ooag_t on sfahucent=ooagent and sfahuc008=ooag001 left join pmaal_t on sfahucent=pmaalent and sfahuc009=pmaal001 and pmaal002='zh_CN' left join imaal_t on sfahucent=imaalent and sfahuc012=imaal001 and imaal002='zh_CN' where sfahuc006 in ('1','3') and to_number(to_char(sfahuc003,'yyyymmdd'))=to_number(to_char(sysdate,'yyyymmdd'))  group by ooag011 order by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()

    for tao1 in res:
        yy=tao1[0]
        xx=0
        xxx = "select sfahucsite 据点,sfahuc001 年份,sfahuc002 周次,sfahuc003 排产时间,sfahuc007 影响单号,ooag011 采购员,NVL(pmaal004,'无') 供应商,sfahuc010 订单号,sfahuc011 订单项次,sfahuc012 影响产品,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,sfahuc013 原交期,sfahuc014 新交期 from sfahuc_t left join ooag_t on sfahucent=ooagent and sfahuc008=ooag001 left join pmaal_t on sfahucent=pmaalent and sfahuc009=pmaal001 and pmaal002='zh_CN' left join imaal_t on sfahucent=imaalent and sfahuc012=imaal001 and imaal002='zh_CN' where sfahuc006 in ('1','3') and to_number(to_char(sfahuc003,'yyyymmdd'))=to_number(to_char(sysdate,'yyyymmdd')) and ooag011='%s'" % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        title = yy+':周计划更改采购交期'
        for tao in res1:
            xx = xx + 1
            r10 = '.：' + tao[0] + ',周次:' + str(tao[1]) + '.' + str(tao[2]) + ',排产时间:' + datetime.datetime.strftime(
                tao[3], "%Y-%m-%d") + ',影响单号:' + tao[4] + ',供应商:' + \
                 tao[6] + ',订单号:' + tao[7] + str(tao[8]) + ',影响产品:' + tao[9] + '[' + tao[10] + ',' + tao[
                     11] + ']' + ',原交期:' + datetime.datetime.strftime(tao[12],"%Y-%m-%d") + ',新交期:' + datetime.datetime.strftime(tao[13], "%Y-%m-%d")

        try:
            r10 = '周计划更改采购交期通知(' + str(xx) + '项[' + yy + ']):\n\n' + r10
            if yy == 'xxx':
                tosend = 'xxx|llll'
            else:
                tosend = yy + '|xxx|llll'
            getr10(r10, tosend, title)
        except:
            tosend = 'xxx|llll'

            getr10(r10, tosend, title)
    cur.close


def get_t10fz():
    # try:
    #     f = open("qcbadocno.txt", 'w+')
    # except IOError:
    #     f = open("qcbadocno.txt", 'a+')
    conn2 = cx_Oracle.connect('dsdata/dsdata@192.168.0.5:1521/TOPPRD')
    cur = conn2.cursor()
    title ='检验单已生成请及时检验'
    #####检验单已生成请及时检验
    xxx = "select qcbadocno 检验单号,qcba010 料号,NVL(imaal003,'无') 品名,NVL(imaal004,'无') 规格,qcba017 数量，NVL(ooag011,'无') 检验员 from qcba_t left join  ooag_t on qcbaent=ooagent and qcba024=ooag001 left join imaal_t on qcbaent=imaalent and qcba010=imaal001 and imaal002='zh_CN' where qcbaent='60' and qcbastus='N' order by ooag011,qcbadocno "
    cur.execute(xxx)
    res = cur.fetchall()
    xx = 0
    r0 = ''
    r3 = ''
    cc = 0
    r10=''
    tao0=''
    for tao in res:
        if cc == 0:
            r1 = tao[5]
        else:
            r3 = tao[5]
        r0 = '.检验单号：' + tao[0] + ',料号：' + tao[1] + '[' + tao[2] + ',' + tao[3] + '],数量:'+ str(tao[4])
        if cc == 1:
            if r3 == r1:
                lines=f.read()
                if tao[0] in lines:
                    print('wj:' + lines)
                else:
                    xx = xx + 1
                    r10 = r10 + str(xx) + r0 + '\n'
                    r1 = tao[5]
                    tao0 = tao[0] + '\n'
            else:
                time.sleep(5)
                try:
                    r10 = '检验单已生成请及时检验(' + str(xx) + '项,['+r1+']):\n\n' + r10
                    tosend = r1+'|xxx|llll'
                    getr10(r10, tosend, title)
                except:
                    r10 = '检验员已离职！' + r10
                    tosend = 'xxx|llll'
                    getr10(r10, tosend, title)
                xx = 0
                cc=0
                tao0=''
        else:
            cc=1

        f.closed
        f = open("qcbadocno.txt", 'a+')
        f.write(tao0)
        r10 = ''
        f.closed

    cur.close

def get_yxh():
    import pymssql  as pymssql
    conn = pymssql.connect(host='192.168.0.23', user='sa', password='1', database='HRMDB', charset='utf8')
    curhr = conn.cursor();
    hrx = "select a.cnname from Employee as a  left join [Job] as e on a.JobId=e.JobId where e.name='销售会计' and EmployeeStateId='EmployeeState2001'"
    curhr.execute(hrx)
    reshr = curhr.fetchone()
    if reshr == None:
        xskj = ''
    else:
        if dingdingexist(reshr[0]) == 1:
            xskj = '|'+reshr[0]
        else:
            xskj = ''

    hrx = "select a.cnname from Employee as a  left join [Job] as e on a.JobId=e.JobId where e.name='采购会计' and EmployeeStateId='EmployeeState2001'"
    curhr.execute(hrx)
    reshr = curhr.fetchone()
    if reshr == None:
        cgkl = ''
    else:
        if dingdingexist(reshr[0]) == 1:
            cgkl = '|'+reshr[0]
        else:
            cgkl = ''
    if not curhr:
        raise Exception('数据库连接失败！')

    conn2 = cx_Oracle.connect('dsdata/dsdata@192.168.0.5:1521/TOPPRD')
    cur = conn2.cursor()

   ##### 对于未结预付款进行有度触发跟踪
    xxx = "select ooag011 from  dsdata.apca_t b left join (select apccdocno a,sum(apcc109) b from  dsdata.apcc_t where apccent='60'  group by apccdocno) a on a.a=b.apcadocno  left join dsdata.apbb_t on apbbent='60' and apbbcomp=b.apcasite and b.apca018=apbbdocno left join dsdata.pmaal_t on b.apca004=pmaal001 and pmaalent=b.apcaent and pmaal002='zh_CN' left join dsdata.ooag_t on ooagent=b.apcaent and ooag001=b.apca014  left join dsdata.apca_t c on b.apcadocno=c.apca019 and b.apcaent=c.apcaent where b.apcaent='60'  and b.apcastus in('Y','A') and (b.apca108-nvl(a.b,0))<>0 and substr(b.apcadocno,4,3) in('751')   and floor(sysdate-b.apcadocdt)>30 group by ooag011 order by ooag011"
    cur.execute(xxx)
    res = cur.fetchall()
    for tao1 in res:
        yy=tao1[0]
        xx=0
        xxx = "select  floor(sysdate-b.apcadocdt) ts,(case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)) je, b.apcasite,to_char(b.apcadocdt,'yyyy-mm-dd')||'日请款，'||decode(b.apca004,'98000',apbb049,pmaal004)||'|'||b.apca100||to_char((case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)))||' ('||b.apcadocno||'|'||c.apcadocno||')已超'||to_char(floor(sysdate-b.apcadocdt))||'天未销账!备注:'||c.apca053||b.apca053 内容 from  dsdata.apca_t b left join (select apccdocno a,sum(apcc109) b from  dsdata.apcc_t where apccent='60'  group by apccdocno) a on a.a=b.apcadocno left join dsdata.apbb_t on apbbent='60' and apbbcomp=b.apcasite and b.apca018=apbbdocno left join dsdata.pmaal_t on b.apca004=pmaal001 and pmaalent=b.apcaent and pmaal002='zh_CN' left join dsdata.ooag_t on ooagent=b.apcaent and ooag001=b.apca014 left join dsdata.apca_t c on b.apcadocno=c.apca019 and b.apcaent=c.apcaent where b.apcaent='60'  and b.apcastus in('Y','A') and (b.apca108-nvl(a.b,0))<>0 and substr(b.apcadocno,4,3) in('751')   and floor(sysdate-b.apcadocdt)>30 and floor(sysdate-b.apcadocdt)<=60 and ooag011='%s' order by b.apcasite,ooag011,decode(b.apca004,'98000',apbb049,pmaal004),b.apcadocdt"  % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        if res1 != None:

            r10 = ''
            bb = 0
            title = yy+':未结预付款(31~60天)'

            for tao in res1:
                xx = xx + 1
                r0 = '.' + tao[2] + ',' + tao[3]

                bb = bb + tao[1]
                r10 = r10 + str(xx) + r0 + '\n'
            try:
                bb = round(bb)
                r10 = '(31~60天)未结预付款(' + str(xx) + '项,预付共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
                tosend = yy + '|xxx|llll'+cgkl
                getr10(r10, tosend,title)
            except:
                r10 = yy+'请款人已离职！' + r10
                tosend = 'xxx|llll'+cgkl
                getr10(r10, tosend,title)
        #61~90天########################################################
        xx=0
        zszgx=''

        xxx = "select  floor(sysdate-b.apcadocdt) ts,(case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)) je, b.apcasite,to_char(b.apcadocdt,'yyyy-mm-dd')||'日请款，'||decode(b.apca004,'98000',apbb049,pmaal004)||'|'||b.apca100||to_char((case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)))||' ('||b.apcadocno||'|'||c.apcadocno||')已超'||to_char(floor(sysdate-b.apcadocdt))||'天未销账!备注:'||c.apca053||b.apca053 内容 from  dsdata.apca_t b left join (select apccdocno a,sum(apcc109) b from  dsdata.apcc_t where apccent='60'  group by apccdocno) a on a.a=b.apcadocno left join dsdata.apbb_t on apbbent='60' and apbbcomp=b.apcasite and b.apca018=apbbdocno left join dsdata.pmaal_t on b.apca004=pmaal001 and pmaalent=b.apcaent and pmaal002='zh_CN' left join dsdata.ooag_t on ooagent=b.apcaent and ooag001=b.apca014 left join dsdata.apca_t c on b.apcadocno=c.apca019 and b.apcaent=c.apcaent where b.apcaent='60'  and b.apcastus in('Y','A') and (b.apca108-nvl(a.b,0))<>0 and substr(b.apcadocno,4,3) in('751')   and floor(sysdate-b.apcadocdt)>60 and floor(sysdate-b.apcadocdt)<=90 and ooag011='%s' order by b.apcasite,ooag011,decode(b.apca004,'98000',apbb049,pmaal004),b.apcadocdt"  % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        if res1 != None:

            r10 = ''
            bb = 0
            title = yy+':未结预付款(61~90天)'
            hrx = "select [Employee_Employee_DirectorId].[CnName] zsname from Employee  LEFT JOIN[Employee] AS [Employee_Employee_DirectorId] ON [Employee].[DirectorId] = [Employee_Employee_DirectorId].[EmployeeId] where Employee.CnName='%s'"  % (yy)
            curhr.execute(hrx)
            reshr = curhr.fetchone()
            if reshr == None:
                zszg = ''
            else:
                if dingdingexist(reshr[0]) == 1:
                    zszg = reshr[0]
                else:
                    zszg = ''
            if (zszg != '') & (zszg != '周洪') & (zszg != '舒银萍') & (zszg != '姚旭辉') & (zszg != '鲁红斌') & (zszg != '方毅') & (zszg != '诸越华'):
                zszgx = '|'+zszg

            for tao in res1:
                xx = xx + 1
                r0 = '.' + tao[2] + ',' + tao[3]

                bb = bb + tao[1]
                r10 = r10 + str(xx) + r0 + '\n'
            try:
                bb = round(bb)
                r10 = '(61~90天)未结预付款(' + str(xx) + '项,预付共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
                tosend = yy + '|xxx|llll'+zszgx+cgkl
                getr10(r10, tosend,title)
            except:
                r10 = yy+'请款人已离职！' + r10
                tosend = 'xxx|llll'+zszgx+cgkl
                getr10(r10, tosend,title)

        #91~180天########################################################
        xx=0
        xxx = "select  floor(sysdate-b.apcadocdt) ts,(case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)) je, b.apcasite,to_char(b.apcadocdt,'yyyy-mm-dd')||'日请款，'||decode(b.apca004,'98000',apbb049,pmaal004)||'|'||b.apca100||to_char((case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)))||' ('||b.apcadocno||'|'||c.apcadocno||')已超'||to_char(floor(sysdate-b.apcadocdt))||'天未销账!备注:'||c.apca053||b.apca053 内容 from  dsdata.apca_t b left join (select apccdocno a,sum(apcc109) b from  dsdata.apcc_t where apccent='60'  group by apccdocno) a on a.a=b.apcadocno left join dsdata.apbb_t on apbbent='60' and apbbcomp=b.apcasite and b.apca018=apbbdocno left join dsdata.pmaal_t on b.apca004=pmaal001 and pmaalent=b.apcaent and pmaal002='zh_CN' left join dsdata.ooag_t on ooagent=b.apcaent and ooag001=b.apca014 left join dsdata.apca_t c on b.apcadocno=c.apca019 and b.apcaent=c.apcaent where b.apcaent='60'  and b.apcastus in('Y','A') and (b.apca108-nvl(a.b,0))<>0 and substr(b.apcadocno,4,3) in('751')   and floor(sysdate-b.apcadocdt)>90 and floor(sysdate-b.apcadocdt)<=180 and ooag011='%s' order by b.apcasite,ooag011,decode(b.apca004,'98000',apbb049,pmaal004),b.apcadocdt"  % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        if res1 != None:

            r10 = ''
            bb = 0
            title = yy+':未结预付款(91~180天)'

            hrx = "select [Employee_Employee_DirectorId].[CnName] zsname from Employee  LEFT JOIN[Employee] AS [Employee_Employee_DirectorId] ON [Employee].[DirectorId] = [Employee_Employee_DirectorId].[EmployeeId] where Employee.CnName='%s'"  % (yy)
            curhr.execute(hrx)
            reshr = curhr.fetchone()
            if reshr == None:
                zszg = ''
            else:
                if dingdingexist(reshr[0]) == 1:
                    zszg = reshr[0]
                else:
                    zszg = ''

            if (zszg != '') & (zszg != 'xxx'):
                zszgx = '|' + zszg

            hrx = "select [Employee_Employee_DirectorId].[CnName] zsname from Employee  LEFT JOIN[Employee] AS [Employee_Employee_DirectorId] ON [Employee].[DirectorId] = [Employee_Employee_DirectorId].[EmployeeId] where Employee.CnName='%s'"  % (reshr[0])
            curhr.execute(hrx)
            reshr = curhr.fetchone()
            if reshr == None:
                zszg = ''
            else:
                if dingdingexist(reshr[0]) == 1:
                    zszg = reshr[0]
                else:
                    zszg = ''

            if (zszg != '') & (zszg != 'xxx'):
                zszgx1 = '|' + zszg
            else:
                zszgx1=''
            for tao in res1:
                xx = xx + 1
                r0 = '.' + tao[2] + ',' + tao[3]

                bb = bb + tao[1]
                r10 = r10 + str(xx) + r0 + '\n'
            try:
                bb = round(bb)
                r10 = '(91~180天)未结预付款(' + str(xx) + '项,预付共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
                tosend = yy + '|xxx|llll'+zszgx+zszgx1+cgkl
                getr10(r10, tosend,title)
            except:
                r10 = yy+'请款人已离职！' + r10
                tosend = 'xxx|llll'+zszgx+zszgx1+cgkl
                getr10(r10, tosend,title)

        # 91~180天########################################################
        xx = 0
        xxx = "select  floor(sysdate-b.apcadocdt) ts,(case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)) je, b.apcasite,to_char(b.apcadocdt,'yyyy-mm-dd')||'日请款，'||decode(b.apca004,'98000',apbb049,pmaal004)||'|'||b.apca100||to_char((case when substr(b.apcadocno,4,2) in('75') then 1 else -1 end)*(b.apca108-nvl(a.b,0)))||' ('||b.apcadocno||'|'||c.apcadocno||')已超'||to_char(floor(sysdate-b.apcadocdt))||'天未销账!备注:'||c.apca053||b.apca053 内容 from  dsdata.apca_t b left join (select apccdocno a,sum(apcc109) b from  dsdata.apcc_t where apccent='60'  group by apccdocno) a on a.a=b.apcadocno left join dsdata.apbb_t on apbbent='60' and apbbcomp=b.apcasite and b.apca018=apbbdocno left join dsdata.pmaal_t on b.apca004=pmaal001 and pmaalent=b.apcaent and pmaal002='zh_CN' left join dsdata.ooag_t on ooagent=b.apcaent and ooag001=b.apca014 left join dsdata.apca_t c on b.apcadocno=c.apca019 and b.apcaent=c.apcaent where b.apcaent='60'  and b.apcastus in('Y','A') and (b.apca108-nvl(a.b,0))<>0 and substr(b.apcadocno,4,3) in('751')   and floor(sysdate-b.apcadocdt)>180 and ooag011='%s' order by b.apcasite,ooag011,decode(b.apca004,'98000',apbb049,pmaal004),b.apcadocdt"  % (yy)

        cur.execute(xxx)
        res1 = cur.fetchall()
        if res1 != None:

            r10 = ''
            bb = 0
            title = yy + ':未结预付款(91~180天)'

            hrx = "select [Employee_Employee_DirectorId].[CnName] zsname from Employee  LEFT JOIN[Employee] AS [Employee_Employee_DirectorId] ON [Employee].[DirectorId] = [Employee_Employee_DirectorId].[EmployeeId] where Employee.CnName='%s'" % (
                yy)
            curhr.execute(hrx)
            reshr = curhr.fetchone()
            if reshr == None:
                zszg = ''
            else:
                if dingdingexist(reshr[0]) == 1:
                    zszg = reshr[0]
                else:
                    zszg = ''

            if (zszg != '') & (zszg != 'xxx'):
                zszgx = '|' + zszg

            hrx = "select [Employee_Employee_DirectorId].[CnName] zsname from Employee  LEFT JOIN[Employee] AS [Employee_Employee_DirectorId] ON [Employee].[DirectorId] = [Employee_Employee_DirectorId].[EmployeeId] where Employee.CnName='%s'" % (
                reshr[0])
            curhr.execute(hrx)
            reshr = curhr.fetchone()
            if reshr == None:
                zszg = ''
            else:
                if dingdingexist(reshr[0]) == 1:
                    zszg = reshr[0]
                else:
                    zszg = ''

            if (zszg != '') & (zszg != 'xxx'):
                zszgx1 = '|' + zszg

            for tao in res1:
                xx = xx + 1
                r0 = '.' + tao[2] + ',' + tao[3]

                bb = bb + tao[1]
                r10 = r10 + str(xx) + r0 + '\n'
            try:
                bb = round(bb)
                r10 = '(91~180天)未结预付款(' + str(xx) + '项,预付共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
                tosend = yy + '|XXX' + zszgx + zszgx1+cgkl
                if tosend.find('yyy') < 0:
                    tosend=tosend+'|yyy'
                getr10(r10, tosend, title)
            except:
                r10 = yy + '请款人已离职！' + r10
                tosend = 'XXX' + zszgx + zszgx1+cgkl
                if tosend.find('yyy') < 0:
                    tosend = tosend + '|yyy'
                getr10(r10, tosend, title)


    #####将到期和已到期的应收款
    xxx = "select a2.ooag011 from dsdata.xrca_t  left join dsdata.pmaa_t on xrca004=pmaa001 and pmaaent=xrcaent left join dsdata.pmaal_t on xrca004=pmaal001 and pmaalent=xrcaent and pmaal002='zh_CN' left join dsdata.xrcc_t on xrccent=xrcaent and xrcccomp=xrcacomp and xrccdocno=xrcadocno left join dsdata.ooag_t  a1 on a1.ooag001=xrca014 and a1.ooagent=xrcaent left join dsdata.isaf_t on isafdocno=xrca018 and isafent=xrcaent and xrcasite=xrcacomp left join dsdata.ooibl_t t2 on xrca008=t2.ooibl002 and t2.ooiblent=xrcaent  and t2.ooibl003='zh_CN' left join dsdata.pmab_t on xrca004=pmab001 and pmabent=xrcaent and pmabsite=xrcacomp left join dsdata.ooag_t a2 on pmab081=a2.ooag001 and a2.ooagent=xrcaent  where xrcaent='60'  and to_char(xrcadocdt,'yyyymmdd')>='20170801' and substr(xrcadocno,4,2) in('61','62','65')   and (xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1)<>0 and xrcastus in ('Y') and xrcacomp not in('US') and floor(sysdate-xrca009)>=-10 group by a2.ooag011 order by a2.ooag011"
    cur.execute(xxx)
    res = cur.fetchall()
    for tao1 in res:
        yy=tao1[0]
        xx=0
        xxx = "select a2.ooag011,floor(sysdate-xrca009) 天,(xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1) je,xrcacomp 公司别,pmaal004||nvl(nvl(xrca021,isafud001),xrca066)||'|'||xrca100||to_char((xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1))||' ('||xrcadocno||')于'||to_char(xrca009,'yyyy-mm-dd')||'到期,逾期'||to_char(floor(sysdate-xrca009))||'天!备注:'||xrcaua001||xrca053 内容 from dsdata.xrca_t  left join dsdata.pmaa_t on xrca004=pmaa001 and pmaaent=xrcaent left join dsdata.pmaal_t on xrca004=pmaal001 and pmaalent=xrcaent and pmaal002='zh_CN' left join dsdata.xrcc_t on xrccent=xrcaent and xrcccomp=xrcacomp and xrccdocno=xrcadocno left join dsdata.ooag_t  a1 on a1.ooag001=xrca014 and a1.ooagent=xrcaent left join dsdata.isaf_t on isafdocno=xrca018 and isafent=xrcaent and xrcasite=xrcacomp left join dsdata.ooibl_t t2 on xrca008=t2.ooibl002 and t2.ooiblent=xrcaent  and t2.ooibl003='zh_CN' left join dsdata.pmab_t on xrca004=pmab001 and pmabent=xrcaent and pmabsite=xrcacomp left join dsdata.ooag_t a2 on pmab081=a2.ooag001 and a2.ooagent=xrcaent  where xrcaent='60'  and to_char(xrcadocdt,'yyyymmdd')>='20170801' and substr(xrcadocno,4,2) in('61','62','65')   and (xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1)<>0 and xrcastus in ('Y') and xrcacomp not in('US') and floor(sysdate-xrca009)>=-10 and floor(sysdate-xrca009)<=21 and a2.ooag011='%s' order by xrcacomp,a2.ooag011,pmaal004,xrca009"  % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        bb = 0
        title = yy+':将到期和已到期的应收款(-10~21天)'

        for tao in res1:
            xx = xx + 1
            r0 = '.' + tao[3] + ',' + tao[4]

            bb = bb + tao[2]
            r10 = r10 + str(xx) + r0 + '\n'
        try:
            bb = round(bb)
            r10 = '(-10~21天)应收款(' + str(xx) + '项,应收共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
            tosend = yy + '|XXX'+xskj
            getr10(r10, tosend,title)
        except:
            r10 = yy+'销售员已离职！' + r10
            tosend = 'XXX'+xskj
            getr10(r10, tosend,title)

        xx=0
        xxx = "select a2.ooag011,floor(sysdate-xrca009) 天,(xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1) je,xrcacomp 公司别,pmaal004||nvl(nvl(xrca021,isafud001),xrca066)||'|'||xrca100||to_char((xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1))||' ('||xrcadocno||')于'||to_char(xrca009,'yyyy-mm-dd')||'到期,逾期'||to_char(floor(sysdate-xrca009))||'天,!备注:'||xrcaua001||xrca053 内容 from dsdata.xrca_t  left join dsdata.pmaa_t on xrca004=pmaa001 and pmaaent=xrcaent left join dsdata.pmaal_t on xrca004=pmaal001 and pmaalent=xrcaent and pmaal002='zh_CN' left join dsdata.xrcc_t on xrccent=xrcaent and xrcccomp=xrcacomp and xrccdocno=xrcadocno left join dsdata.ooag_t  a1 on a1.ooag001=xrca014 and a1.ooagent=xrcaent left join dsdata.isaf_t on isafdocno=xrca018 and isafent=xrcaent and xrcasite=xrcacomp left join dsdata.ooibl_t t2 on xrca008=t2.ooibl002 and t2.ooiblent=xrcaent  and t2.ooibl003='zh_CN' left join dsdata.pmab_t on xrca004=pmab001 and pmabent=xrcaent and pmabsite=xrcacomp left join dsdata.ooag_t a2 on pmab081=a2.ooag001 and a2.ooagent=xrcaent  where xrcaent='60'  and to_char(xrcadocdt,'yyyymmdd')>='20170801' and substr(xrcadocno,4,2) in('61','62','65')   and (xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1)<>0 and xrcastus in ('Y') and xrcacomp not in('US') and floor(sysdate-xrca009)>=22 and floor(sysdate-xrca009)<=60 and a2.ooag011='%s' order by xrcacomp,a2.ooag011,pmaal004,xrca009"  % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        bb = 0
        title = yy+':已到期应收款(22~60天)'

        for tao in res1:
            xx = xx + 1
            r0 = '.' + tao[3] + ',' + tao[4]

            bb = bb + tao[2]
            r10 = r10 + str(xx) + r0 + '\n'
        try:
            bb = round(bb)
            r10 = '(22~60天)应收款(' + str(xx) + '项,应收共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
            if yy == 'ZZZ':
                tosend = 'XXX|YYY' + xskj
            else:
                tosend = yy + 'XXX|YYY' + xskj

            getr10(r10, tosend,title)
        except:
            r10 = yy+'销售员已离职！' + r10
            tosend = 'XXX|YYY'+xskj
            getr10(r10, tosend,title)

        xx=0
        xxx = "select a2.ooag011,floor(sysdate-xrca009) 天,(xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1) je,xrcacomp 公司别,pmaal004||nvl(nvl(xrca021,isafud001),xrca066)||'|'||xrca100||to_char((xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1))||' ('||xrcadocno||')于'||to_char(xrca009,'yyyy-mm-dd')||'到期,逾期'||to_char(floor(sysdate-xrca009))||'天!备注:'||xrcaua001||xrca053 内容 from dsdata.xrca_t  left join dsdata.pmaa_t on xrca004=pmaa001 and pmaaent=xrcaent left join dsdata.pmaal_t on xrca004=pmaal001 and pmaalent=xrcaent and pmaal002='zh_CN' left join dsdata.xrcc_t on xrccent=xrcaent and xrcccomp=xrcacomp and xrccdocno=xrcadocno left join dsdata.ooag_t  a1 on a1.ooag001=xrca014 and a1.ooagent=xrcaent left join dsdata.isaf_t on isafdocno=xrca018 and isafent=xrcaent and xrcasite=xrcacomp left join dsdata.ooibl_t t2 on xrca008=t2.ooibl002 and t2.ooiblent=xrcaent  and t2.ooibl003='zh_CN' left join dsdata.pmab_t on xrca004=pmab001 and pmabent=xrcaent and pmabsite=xrcacomp left join dsdata.ooag_t a2 on pmab081=a2.ooag001 and a2.ooagent=xrcaent  where xrcaent='60'  and to_char(xrcadocdt,'yyyymmdd')>='20170801' and substr(xrcadocno,4,2) in('61','62','65')   and (xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1)<>0 and xrcastus in ('Y') and xrcacomp not in('US') and floor(sysdate-xrca009)>=61 and floor(sysdate-xrca009)<=90 and a2.ooag011='%s' order by xrcacomp,a2.ooag011,pmaal004,xrca009"  % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        bb = 0
        title = yy+':已到期应收款(61~90天)'

        for tao in res1:
            xx = xx + 1
            r0 = '.' + tao[3] +  tao[4]

            bb = bb + tao[2]
            r10 = r10 + str(xx) + r0 + '\n'
        try:
            bb = round(bb)
            r10 = '(61~90天)应收款(' + str(xx) + '项,应付共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
            if yy == 'YYY' or yy == 'XXX':
                tosend = 'XXX|YYY'+xskj
            else:
                tosend = yy + '|XXX|YYY'+xskj
            getr10(r10, tosend,title)
        except:
            r10 = yy+'销售员已离职！' + r10
            tosend = 'XXX|YYY'+xskj
            getr10(r10, tosend,title)

        xx=0
        xxx = "select a2.ooag011,floor(sysdate-xrca009) 天,(xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1) je,xrcacomp 公司别,pmaal004||nvl(nvl(xrca021,isafud001),xrca066)||'|'||xrca100||to_char((xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1))||' ('||xrcadocno||')于'||to_char(xrca009,'yyyy-mm-dd')||'到期,逾期'||to_char(floor(sysdate-xrca009))||'天!备注:'||xrcaua001||xrca053 内容 from dsdata.xrca_t  left join dsdata.pmaa_t on xrca004=pmaa001 and pmaaent=xrcaent left join dsdata.pmaal_t on xrca004=pmaal001 and pmaalent=xrcaent and pmaal002='zh_CN' left join dsdata.xrcc_t on xrccent=xrcaent and xrcccomp=xrcacomp and xrccdocno=xrcadocno left join dsdata.ooag_t  a1 on a1.ooag001=xrca014 and a1.ooagent=xrcaent left join dsdata.isaf_t on isafdocno=xrca018 and isafent=xrcaent and xrcasite=xrcacomp left join dsdata.ooibl_t t2 on xrca008=t2.ooibl002 and t2.ooiblent=xrcaent  and t2.ooibl003='zh_CN' left join dsdata.pmab_t on xrca004=pmab001 and pmabent=xrcaent and pmabsite=xrcacomp left join dsdata.ooag_t a2 on pmab081=a2.ooag001 and a2.ooagent=xrcaent  where xrcaent='60'  and to_char(xrcadocdt,'yyyymmdd')>='20170801' and substr(xrcadocno,4,2) in('61','62','65')   and (xrcc108-xrcc109)*decode(xrca001,'22',-1,'24',-1,1)<>0 and xrcastus in ('Y') and xrcacomp not in('US') and  floor(sysdate-xrca009)>90 and a2.ooag011='%s' order by xrcacomp,a2.ooag011,pmaal004,xrca009"  % (yy)
        cur.execute(xxx)
        res1 = cur.fetchall()
        r10 = ''
        bb = 0
        title = yy+':已到期的应收款(90天以上)'

        for tao in res1:
            xx = xx + 1
            r0 = '.' + tao[3] + tao[4]

            bb = bb + tao[2]
            r10 = r10 + str(xx) + r0 + '\n'
        try:
            bb = round(bb)
            r10 = '(90天以上)应收款(' + str(xx) + '项,应付共' + str(format(bb, ",")) + '元[' + yy + ']):\n\n' + r10
            if yy == 'YYY' or yy == 'XXX':
                tosend = 'XXX|YYY'+xskj
            else:
                tosend = yy + '|XXX|YYY'+xskj
            getr10(r10, tosend,title)
        except:
            r10 = yy+'销售员已离职！' + r10
            tosend = 'XXX|YYY'+xskj
            getr10(r10, tosend,title)
    curhr.close
    cur.close
