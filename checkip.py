#!/usr/bin/python
#coding:utf-8
#python 3
#tested in Win
#tested in Centos


import smtplib, configparser, os ,sys,subprocess
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

def getpubip():
    cmd = 'curl ifconfig.me'
    newip = subprocess.run(['curl','ifconfig.me','>',record])
    return newip

def sendmsg(newip,confile):
    config = configparser.ConfigParser()
    config.read(confile)
    mailsvr = config['mailsetting']['mailsvr']
    fromaddr = config['mailsetting']['fromaddr']
    toaddr = config['mailsetting']['toaddr']
    user = config['mailsetting']['user']
    passwd = config['mailsetting']['pass']
    body = newip
    # print(mailsvr)

    msg = MIMEText(body,'plain','utf-8')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Public IP Change'
 
    try:
        server = smtplib.SMTP()
        server.connect(mailsvr,25)
        # server = smtplib.SMTP_SSL(mailsvr)
        server.set_debuglevel(1)
        server.login(user,passwd)
        server.ehlo()
        # server.starttls()
        server.sendmail(fromaddr,toaddr,msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print('error',e)


def checkip():
    # compare IP
    with open(record,'r') as f:
        ip = f.readline().split()[0]
    newip = getpubip()
    if ip == newip :
        print('IP no change')
    else:
        with open(record,'w') as f:
            f.writelines(newip)
        sendmsg(newip,confile)

if __name__=='__main__':
    checkip()


