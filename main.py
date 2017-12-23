# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as BS
import time
from subprocess import Popen  # 打开图片
import http.cookiejar
import re
import json
import pickle

user='xxxx'
pwdd='xxxx'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}

def GetTestScore():
    requrl="http://student.7net.cc/exam/defaulExamInfo"
    data={
        "_septnet_document" : '{"examGuid":"dea920f7-f6b7-449f-a8ef-41b2cb40ed21","studentCode":"215272710"}'
        }
    response = session.post(requrl, data=data, headers=headers)
    print(response.content.decode("utf-8"))

def GetTestList():
    requrl="http://student.7net.cc/Exam/claimExamList"
    data={
        "_septnet_document" : '{"viewIndex":1,"viewLength":200,"score":1}'
        }
    response = session.post(requrl, data=data, headers=headers)
    TestList=response.content.decode("utf-8")
    TestList=TestList[4:]
    #print(TestList)
    TestFinal=json.loads(TestList)
    return TestFinal['List']


def FetchDetailedTest(TestList):
    json.dump(TestList, open("tmp.txt","w"))

    obj2=json.load(open("tmp.txt","r"))
    print(obj2)
            
    

# 模拟浏览器访问

home_url = "http://student.7net.cc/Default"
base_login = "http://student.7net.cc/Login"  # 一定不能写成http,否则无法登录

session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename='ZhiHuCookies')
try:
    # 加载Cookies文件
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未保存或cookie已过期")
    # # 第一步 获取_xsrf
    # _xsrf = BS(session.get(home_url, headers=headers).text, "lxml").find("input", {"name": "_xsrf"})["value"]

    # # 第二步 根据账号判断登录方式
    # account = input("请输入您的账号：")
    # password = input("请输入您的密码：")

    # # 第三步 获取验证码图片
    # gifUrl = "http://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000)) + "&type=login"
    # gif = session.get(gifUrl, headers=headers)
    # # 保存图片
    # with open('code.gif', 'wb') as f:
    #     f.write(gif.content)
    # # 打开图片
    # Popen('code.gif', shell=True)
    # # 输入验证码
    # captcha = input('captcha: ')


    # # 第四步 判断account类型是手机号还是邮箱
    # if re.match("^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$", account):
    #     # 邮箱
    #     data["email"] = account
    #     base_login = base_login + "email"
    # else:
    #     # 手机号
    #     data["phone_num"] = account
    #     base_login = base_login + "phone_num"

    # print(data)

    # 第五步 登录

data = {
        '_septnet_document' : '{"usercode":"'+user+'","password":"'+pwdd+'"}'
}
    
response = session.post(base_login, data=data, headers=headers)
# print(response.content.decode("utf-8"))

    # 第六步 保存cookie
session.cookies.save()

# 获取首页信息
resp = session.get(home_url, headers=headers, allow_redirects=False)
# print(resp.content.decode("utf-8"))
FetchDetailedTest(GetTestList())

