# -*- coding: utf-8 -*-

import sys
import requests
import os
import getopt
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
    

# 模拟浏览器访问

home_url = "http://student.7net.cc/Default"
base_login = "http://student.7net.cc/Login"  # 一定不能写成http,否则无法登录

session = requests.session()
Login = False

def Check_Login():
    if Login == False:
        data = {
            '_septnet_document' : '{"usercode":"'+user+'","password":"'+pwdd+'"}'
        }
    
        response = session.post(base_login, data=data, headers=headers)
    else: return
# print(response.content.decode("utf-8"))

    # 第六步 保存cookie


# 获取首页信息
# resp = session.get(home_url, headers=headers, allow_redirects=False)
        
    

def DetailPreProcess():
    if os.path.exists('./Detail.raw'):
        if os.path.getsize('./Detail.raw'):
            return
    json.dump([],open('./Detail.raw','w'))
     

        
def GetTestDetail(exGuid, studentCode):
    DetailPreProcess()
    TList=json.load(open("Detail.raw","r"))

    for tl in TList:
        if tl['examPlanGuid'] == exGuid:
            return tl
    Check_Login()
    requrl="http://student.7net.cc/exam/defaulExamInfo"
    st = '{"examGuid":"'+exGuid+'","studentCode":"'+studentCode+'"}'
    data={
        "_septnet_document" : st
        }
    response = session.post(requrl, data=data, headers=headers)
    TestList=response.content.decode("utf-8")
    TestList=TestList[4:]
    #print(TestList)
    TestFinal=json.loads(TestList)
    TList.append(TestFinal)
    json.dump(TList,open("Detail.raw","w"))
    return TestFinal


def UpdateTestList():
    Check_Login()
    requrl="http://student.7net.cc/Exam/claimExamList"
    data={
        "_septnet_document" : '{"viewIndex":1,"viewLength":200,"score":1}'
        }
    response = session.post(requrl, data=data, headers=headers)
    TestList=response.content.decode("utf-8")
    TestList=TestList[4:]
    #print(TestList)
    TestFinal=json.loads(TestList)
    json.dump(TestFinal['List'],open("Tests.raw","w"))



def GetTestList():
    obj = json.load(open("Tests.raw","r"))
    return obj

    
def PrintSingalTest(Test, i):
    print('\033[1m\033[32m'+str(i)+'.',Test['time'].split()[0],Test['examName'])
#    PrintDetailedTest(Test)

    
def PrintRecentTest(num = 10):

    TList=json.load(open("Tests.raw","r"))
    for i in range(0,min(num,len(TList))):
        PrintSingalTest(TList[i],i+1)

def PrintDetailedTest(Test):
    print('\033[1m\033[36m'+Test['examName'])
    for i in Test['km']:
        st='\033[1m\033[32m['+i['Name']+'] '
        st+='[Score:'+str(i['Score'])+'] '
        st+='\033[0m'
        print('\033[1m\033[32m%-10s%+5s' %(i['Name'],str(i['Score'])))
    print('\033[1m\033[33m%-10s%5.0f'%('排名估计',Test['studentCount']-Test['allPercent']*Test['studentCount']*0.01))
    print('\033[0m')


def main(argv):    
    try:
        opts, args = getopt.getopt(argv,"hRUr:t:",["id=","ofile="])
    except getopt.GetoptError:
        print ('7net.py -R -r <num> -t <test_id> -U')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('7net.py -R -r <num> -t <test_id> -U')
            sys.exit()
        elif opt in ("-R"):
            PrintRecentTest()
        elif opt in ("-r"):
            PrintRecentTest(int(arg))
        elif opt in ("-t"):
            num = int(arg)
            num = num-1
            ts=GetTestList()
            Test=GetTestDetail(ts[num]['examPlanGuid'],ts[num]['studentCode'])
            PrintDetailedTest(Test)
        elif opt in ("-U"):
            UpdateTestList()
            print("\033[1m\033[32mSuccess\033[0m")
           
          


if __name__ == "__main__":
    main(sys.argv[1:])

# ts = GetTestList()
# PrintDetailedTest(GetTestDetail(ts[0]['examPlanGuid'],ts[0]['studentCode']))


