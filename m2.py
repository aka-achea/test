import requests
# from requests.cookies import RequestsCookieJar

userAgent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36"

header = {
    "Referer": "https://passport.mafengwo.cn/",
    'User-Agent': userAgent
}


lg = "https://passport.mafengwo.cn/login/"
user = 'https://m.mafengwo.cn'


data = {'passport':"akaachea@163.com",'password':"5021529"}
s = requests.Session()
l = s.post(lg, data=data, headers=header)
# print(l.text)
print(l.cookies)
r = s.get(user)
print(r.cookies)
print(r.text)

# print(res.text)

# def mafengwoLogin(account, password):
#     # 马蜂窝模仿登录
#     print ("开始模拟登录马蜂窝")
#     postUrl = "https://passport.mafengwo.cn/login/"
#     postData = {
#         "passport": account,
#         "password": password,
#     }
#     responseRes = requests.post(postUrl, data = postData, headers = header)
#     # 打印登陆后的界面
#     # print(f"text = {responseRes.text}")
#     c = responseRes.cookies
#     # print(responseRes.headers)
#     return c

# c = mafengwoLogin("akaachea@163.com", "5021529")
# dk = "https://m.mafengwo.cn/activity/daka"
# res = requests.get(dk,cookies=c)