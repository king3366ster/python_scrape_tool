#! /usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append('../')
from bs4 import BeautifulSoup
import random, time, hashlib, re
from ScrapeLib.HttpRequest import HttpRequest
httpReq = HttpRequest()

time_now = time.strftime("%Y/%m/%d", time.localtime())

class Scrape:
    def __init__(self):
        pass

    def bs4HttpData(self, data):
        bsHandle = BeautifulSoup(data, 'lxml')
        return bsHandle

    def getAnchorHref(self, soupData):
        httpSoup = self.bs4HttpData(unicode(soupData))
        searchList = httpSoup.findAll('a')
        urlList = []
        for searchItem in searchList:
            urlList.append(searchItem.get('href'))
        return urlList

    def searchItjuzi(self, keyword = ''):
        url = 'https://www.itjuzi.com/search'
        data = {
            'key': keyword
        }
        httpData = httpReq.getHttpData(url, data).read()
        httpSoup = self.bs4HttpData(httpData)
        searchList = httpSoup.find_all(id='the_search_list')
        if isinstance(searchList, list) and len(searchList) > 0:
            urlList = self.getAnchorHref(searchList[0])
            print urlList
            for corpUrl in urlList:
                self.searchItjuziCorp(corpUrl)
        else:
            return 'not found'

    def run(self):
        print 'itjuzi'

if __name__ == '__main__':
    t = Scrape()
    keyword = '中科方德'
    keyword = '阿里巴巴'
    # t.searchItjuzi(keyword = keyword)
    item = t.searchLagou(keyword = keyword)
    for key in item:
        print key, item[key]
