#-*- coding: UTF-8 -*-
__author__ = 'guoguo'

import requests
import time
import os
import sys
import  json
from HTMLParser import HTMLParser
class iShadowSocksParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isFreeSection = False
        self.isServerSection = False
        self.serverinfo = []

    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            for attr in attrs:
                if attr[1] == 'free':
                    self.isFreeSection = True
                    break
        if self.isFreeSection:
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'col-lg-4 text-center':
                    self.isServerSection = True

    def handle_endtag(self, tag):
        if tag == 'section':
            if self.isFreeSection:
                    self.isFreeSection = False
        if tag == 'div' and self.isServerSection:
            self.isServerSection = False

    def handle_data(self, data):
        if self.isServerSection:
            serverAddress = "服务器地址"
            password = "密码"
            port = "端口"
            encreptType = "加密方式"


            parts = data.split('\n')
            i = 0
            tempInfo = {}
            for part in parts:
                i = i +1
                part = part.strip()
                if part.__contains__(':'):
                    key = part.split(':')[0]
                    value = part.split(':')[1]
                    if  key.__contains__('A') and key.__contains__(serverAddress):
                        tempInfo["server"] = value
                        self.serverinfo.append(tempInfo)
                    if key.__contains__('A') and key.__contains__(password):
                        tempInfo["password"] = value
                        self.serverinfo.append(tempInfo)
                    if port == key:
                        tempInfo["server_port"] = value
                        self.serverinfo.append(tempInfo)
                    if encreptType == key:
                        tempInfo["method"] = value
                        self.serverinfo.append(tempInfo)
                    if  key.__contains__('B') and key.__contains__(serverAddress):
                        tempInfo["server"] = value
                        self.serverinfo.append(tempInfo)
                    if key.__contains__('B') and key.__contains__(password):
                        tempInfo["password"] = value
                        self.serverinfo.append(tempInfo)
                    if  key.__contains__('C') and key.__contains__(serverAddress):
                        tempInfo["server"] = value
                        self.serverinfo.append(tempInfo)
                    if key.__contains__('C') and key.__contains__(password):
                        tempInfo["password"] = value
                        self.serverinfo.append(tempInfo)




ishadowsocksUrl = "http://www.ishadowsocks.com"
ishadowsocksPort = 80
userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36"
requestHeaders = {}
requestHeaders["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
requestHeaders["Accept-Encoding"] = "gzip, deflate, sdch"
requestHeaders["Accept-Language"] = "en-US,en;q=0.8,ar;q=0.6,fr;q=0.4,ja;q=0.2,pt;q=0.2,zh-CN;q=0.2,zh-TW;q=0.2"
requestHeaders["Cache-Control"] = "max-age=0"
requestHeaders["Connection"] = "keep-alive"
requestHeaders["Host"] = "www.ishadowsocks.com"
requestHeaders["User-Agent"] = userAgent
requestHeaders["Refer"] = "www.ishadowsocks.com"

#print requestHeaders
'''
request = urllib2.Request(ishadowsocksUrl)
for header in requestHeaders.keys():
    request.add_header(header, requestHeaders[header])

response = urllib2.urlopen(request)
page = response.read()
page.decode("utf-8")
'''
response = requests.get(ishadowsocksUrl, headers=requestHeaders)

parser = iShadowSocksParser()
parser.feed(response.content)



time.sleep(2)
server = {"local_port":1080, "timeout":600,}
for i in range(0, 4):
    item = parser.serverinfo[i]

    if item.has_key('server'):
        server["server"] = item.get('server')
    if item.has_key('server_port'):
        server["server_port"] = item.get('server_port')
    if item.has_key('password'):
        server["password"] = item.get('password')
    if item.has_key('method'):
        server["method"] = item.get('method')
resultStr = json.dumps(server, ensure_ascii=False)
print resultStr
# jsonPath = "/home/haiming/.shadowsocks.json"
# jsonFile = open(jsonPath, 'w')
# jsonFile.write(resultStr.strip().encode('utf-8'))
# jsonFile.close()