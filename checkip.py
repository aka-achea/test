#!/usr/bin/python3
#coding:utf-8
#tested in Win
#tested in Centos


import smtplib, configparser, os ,time,sys,subprocess
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# from email import encoders

if sys.platform == 'win32':
    record = r'e:\pubip'
    confile = r'C:\D\GitHub\test\mail.ini'
else:
    record = r'/job/pubip'
    confile = r'/job/mail.ini'


def sendmsg(newip,confile):
   # config = configparser.ConfigParser()
   # config.read(confile)
    mailsvr = 'smtp.163.com'
    sender = 'favoritebm@163.com'
    receiver = 'favoritebm@163.com'
    user = 'favoritebm@163.com'
    passwd = 'orz163'
    body = newip
    # print(mailsvr)
    #print(user)

    msg = MIMEText(body,'plain','utf-8')
    msg['from'] = sender
    msg['to'] = receiver
    msg['Subject'] = 'Public IP Change'

    try:
        #server = smtplib.SMTP(mailsvr,25)
        server = smtplib.SMTP_SSL(mailsvr,465)
        #server = smtplib.SMTP_SSL()
        #server.connect(mailsvr,465)
        server.set_debuglevel(1)
        server.login(user,passwd)
        #server.ehlo()
        server.sendmail(sender,receiver,msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print('error',e)


def checkip():
    # compare IP
    with open(record,'r') as f:
        ip = f.readline()
        print('old'+ip)
    cmd = 'curl -s ifconfig.me --max-time 7 -o '+record
    os.popen(cmd)
    time.sleep(5)
    with open(record,'r') as f:
        newip = f.readline()
        print('new'+newip)
    if ip == newip :
        print('IP no change')
    else:
        print('IP changed')
        sendmsg(newip,confile)

if __name__=='__main__':
    checkip()

