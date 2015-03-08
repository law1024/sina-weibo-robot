#!/usr/bin/env python
#encoding:utf-8

import re
import rsa
import time
import json
import urllib
import base64
import random
import binascii
import requests
from bs4 import BeautifulSoup

class Weibo(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    #登录
    def login(self):
        # step1
        resp = requests.get("http://login.sina.com.cn/signup/signin.php?entry=sso")
        # step2
        data = {
            "entry"   : "sso",
            #不传callback返回的就是纯json数据
            "callback": "",
            "su"      : "",
            "rsakt"   : "mod",
            "client"  : "ssologin.js(v1.4.15)",
            "_"       : int(time.time() * 1000)
        }
        resp = requests.get("http://login.sina.com.cn/sso/prelogin.php", params=data)
        #把各个字段都解析出来
        resp = json.loads(resp.content.decode('gbk'))
        # 几个比较重要的字段
        nonce      = resp["nonce"]
        servertime = resp["servertime"]
        pcid       = resp["pcid"]
        pubkey     = resp["pubkey"]
        # step3 对用户名和密码进行加密
        su  = base64.b64encode(urllib.parse.quote(self.username).encode('gbk'))
        key = rsa.PublicKey(int(pubkey, 16), 65537)
        st  = str(servertime) + '\t' + nonce + '\n' + self.password

        sp  = rsa.encrypt(st.encode('gbk'), key)
        sp  = binascii.b2a_hex(sp)
        # step4 请求登录接口
        data = {
            "entry": "sso",
            "gateway": 1,
            "from": "null",
            "savestate": 0,
            "useticket": 0,
            "pagerefer": "http://login.sina.com.cn/sso/login.php?client=ssologin.js",
            "vsnf": 1,
            "su": su,
            "service": "sso",
            "servertime": servertime,
            "nonce": nonce,
            "pwencode": "rsa2",
            "rsakv": "1330428213",
            "sp": sp,
            "sr": "1366*768",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": random.randint(20, 150),
            "returntype": "TEXT"
        }

        resp = requests.post("http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=" + str(int(time.time() * 1000)), params=data)
        uri  = json.loads(resp.content.decode('gbk'))["crossDomainUrlList"][0]
        # data = {
        #     "retcode"     : "0",
        #     "url"         : urllib.parse.quote("http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&sudaref=weibo.com")
        # }
        # for k, v in data.items():
        #     uri += "&" + k + "=" + v
        resp = requests.get(uri)
        # print(uri)
        # print(resp.cookies)
        # resp = requests.get("http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&sudaref=weibo.com")
        resp = requests.get("http://weibo.com", cookies=resp.cookies)
        return resp.content
        print(resp.content)


    #发送新鲜事
    def send(**news):
        pass

    #搜索用户
    def search():
        pass

    #添加关注
    def follow():
        pass

    #取消关注
    def cancel():
        pass