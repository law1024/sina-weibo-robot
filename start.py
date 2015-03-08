#!/usr/bin/env python
#encoding:utf-8

import weibo.weibo as weibo
import requests
from bs4 import BeautifulSoup

# #将抓到的数据保存到文件里
def save_file(data, path, coding='gbk'):
    f = open(path, 'wb')
    f.write(data.encode(coding))
    f.close()

# def main():
#     resp = requests.get("http://1.baidu.com")
#     resp.encoding = 'gbk'
#     soup = BeautifulSoup(resp.content)

#     nameList = soup.find_all('a', class_='goods-name')
#     timeList = soup.find_all('li', class_='count-down')

    
# main()

wb = weibo.Weibo("username", "password")
wb.login()