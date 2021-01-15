#-*- coding:utf-8 -*-
__author__ = 'Zach_z & XuYan'

import time
import requests
import re
import sys
import importlib
# importlib.reload(sys)
reload(sys)
# sys.setdefaultencoding('utf-8')

class Login:

    #初始化
    def __init__(self):
        #检测间隔时间，单位为秒
        self.every = 15

    #模拟登录
    def login(self):
        print(self.getCurrentTime())
	print("拼命连网中...\n")

        url="http://202.204.48.66"
        #消息头#Chrome
        headers={
        'User-Agent':"Mozilla/5.0 (X12; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
        #'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
        }
        #提交的信息
        payload={
        'DDDDD':'s20200473',#账号
        'upass':'07295430',#密码
        '0MKKey':''
        }
        try:
            requests.post(url,headers=headers,data=payload)
            print(self.getCurrentTime())
	    print('连上了...现在开始看连接是否正常\n')
        except:
            print("error")
    #判断当前是否可以连网
    def canConnect(self):
        try:
            q=requests.get("http://www.baidu.com",timeout=5)
            m=re.search(r'STATUS OK',q.text)
            if m:
                return True
            else:
                return False
        except:
            print('error')
            return False

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #主函数
    def main(self):
        print(self.getCurrentTime())
	print("Hi，欢迎使用自动登陆系统\n")
        while True:
            self.login()
            while True:
                can_connect = self.canConnect()
                if not can_connect:
                    print(self.getCurrentTime())
		    print("断网了...\n")
                    self.login()
                else:
                    print(self.getCurrentTime())
		    print("一切正常...\n")
                time.sleep(self.every)
            time.sleep(self.every)

login = Login()
login.main()
