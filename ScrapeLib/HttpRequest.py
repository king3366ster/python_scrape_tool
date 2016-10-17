#! /usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2, urllib, cookielib
import json, xmltodict
from bs4 import BeautifulSoup

class HttpRequest:
    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def getData(self, url, data = None):
        if data is None:
            url = url
        else:
            params = urllib.urlencode(data)
            url = url + '?' + params

        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            }
##        print url
        req = urllib2.Request(url, headers = headers);
        res_data = self.opener.open(req) # urllib2.urlopen(req)
        return res_data

    # dataType formdata/text/json/xml
    def postData(self, url, data = {}, header = {}, dataType = 'formdata'):
        initHeader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        if dataType == 'formdata':
            if isinstance(data, dict):
                data = urllib.urlencode(data)
            tempHeader = {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        elif dataType == 'json':
            if isinstance(data, dict):
                data = json.dumps(data)
            tempHeader = {
                'Content-Type': 'application/json;'
            }
        elif dataType == 'plain':
            data = str(data)
            tempHeader = {
                'Content-Type': 'text/plain;'
            }
        elif dataType == 'xml':
            if isinstance(data, dict):
                data = xmltodict.unparse(data)
            tempHeader = {
                'Content-Type': 'text/xml;'
            }
        tempHeader['Content-Length'] = len(data)
        headers = dict(initHeader.items() + tempHeader.items() + header.items())

        req = urllib2.Request(url, data, headers = headers);
        res_data = self.opener.open(req)
        return res_data

    def bs4HttpData(self, data):
        bsHandle = BeautifulSoup(data, 'lxml')
        return bsHandle

if __name__ == '__main__':

    q = {
        'wd': '测试'
    }
    t = HttpRequest()
    print t.getData('https://www.baidu.com/s?wd=%E6%B5%8B%E8%AF%95').read()
    # t.postData('http://', data = q, dataType = 'formdata')
