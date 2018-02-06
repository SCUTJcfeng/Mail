import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import sys
import os
import time
from smtplib import SMTPConnectError
from selenium import webdriver
import random
import pymysql
import re
import datetime
# 定义函数
def get_hitokoto_text():
    #读取数据库   
    db =pymysql.connect(host = 'localhost',user = 'root',password = 'root',database = 'hitokoto',charset = 'utf8')
    with db.cursor() as cursor:
        while True:
            i = random.randint(1,2841)
            sql = 'select dateline,content,note,translation,fenxiang_img from hitokoto.ciba where sid ='
            cursor.execute(sql + str(i))
            data = cursor.fetchone()
            if data != None:
                break
    dateline = data[0]
    content = data[1]
    note = data[2]
    translation = data[3]
    fenxiang_img = data[4]

    lt = [dateline,content,note,translation,fenxiang_img]
    return lt

def send_mail(to_list, sub):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = "".join(to_list)

    # 构造html
    html = """\
        <html>
          <body>
            <p>金山词霸每日一句:</p>
            <p>时间：""" + dateline.strftime('%Y-%m-%d')  + """</p>
            <p>每日一句：""" + content + """</p>
            <p>翻译：""" + note + """</p>
            <p>评论：""" + translation + """</p>
            <img src = '""" + fenxiang_img+ """'>
          </body>
        </html>
        """
    
    context = MIMEText(html, _subtype='html', _charset='utf-8')  # 定义发送的形式和编码格式，这里以html形式发送
    msg.attach(context)

    try:
        send_smtp = smtplib.SMTP_SSL(port = 463)
        send_smtp.connect(mail_host)
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(me, to_list, msg.as_string())
        send_smtp.close()
        return True
    except SMTPConnectError as e:
        print(e)
        return False

# 设置服务器名称、用户名、密码以及邮件后缀
# For QQ mail only
mail_host = 'smtp.qq.com'
mail_user = '123456789' # Your QQ
mail_pass = 'xxsadfd123546fsadfaff' # Get from QQ mail webpage... Find it yourself...
mail_postfix = "qq.com"
#mailto_lists = sys.argv[1]
#mailto_list = mailto_lists.split(',')   #发送多人
#sub= sys.argv[2]
mailto_list = ['xxxxx@xx.com,xxxxx@xxx.com']

sub= "金山词霸每日一句（历史随机）"
#send_mail(mailto_list, sub)

lt = get_hitokoto_text()#lt = [dateline,content,note,translation,fenxiang_img]
dateline = lt[0]
content =lt[1]
note =lt[2]
translation =lt[3]
fenxiang_img =lt[4]


'''
author =lt[1].replace('-「','')
author = author.replace('」','')
'''
if send_mail(mailto_list, sub):
        print ("Send mail succed!")
else:
        print ("Send mail failed!")


