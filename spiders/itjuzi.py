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
##
##    def searchItjuzi(self, keyword = ''):
##        url = 'https://www.itjuzi.com/search'
##        data = {
##            'key': keyword
##        }
##        httpData = httpReq.getHttpData(url, data).read()
##        httpSoup = self.bs4HttpData(httpData)
##        searchList = httpSoup.find_all(id='the_search_list')
##        if isinstance(searchList, list) and len(searchList) > 0:
##            urlList = self.getAnchorHref(searchList[0])
##            print urlList
##            for corpUrl in urlList:
##                self.searchItjuziCorp(corpUrl)
##        else:
##            return 'not found'
##
##    def searchItjuziCorp(self, url):
##        httpRes = self.getHttpData(url)
##        httpSoup = self.bs4HttpData(httpRes.read())

    def searchLagou(self, keyword = ''):
        url = 'http://www.lagou.com/jobs/list_%s' % keyword
        httpData = httpReq.getData(url).read()
        httpSoup = self.bs4HttpData(httpData)
        searchItem = httpSoup.find(id='positionHead')
        if searchItem is None:
            return 'Not Found'
        searchItem = searchItem.find('div', class_='company-card')
        searchItem = searchItem.find('li', class_='c_btn')
        searchUrls = self.getAnchorHref(searchItem)
        searchUrl = 'http:%s' % searchUrls[0]
        return self.searchLagouCorp(searchUrl)

    def searchLagouCorp(self, url):
        httpRes = httpReq.getData(url)
        httpSoup = self.bs4HttpData(httpRes.read())
        # 公司基本信息
        searchItem = httpSoup.find('div', id='container_right')
        corp_type = searchItem.find('i', class_ = 'type').parent
        corp_type = corp_type.find('span').get_text()
        corp_process = searchItem.find('i', class_ = 'process').parent
        corp_process = corp_process.find('span').get_text()
        corp_number = searchItem.find('i', class_ = 'number').parent
        corp_number = corp_number.find('span').get_text()
        corp_address = searchItem.find('i', class_ = 'address').parent
        corp_address = corp_address.find('span').get_text()
        # 产品介绍
        searchItem = httpSoup.find('div', class_='product_details')
        product_url = searchItem.find('div', class_='product_url')
        product_url = product_url.get_text()
        product_profile = searchItem.find('div', class_='product_profile')
        product_profile = product_profile.get_text()
        # 公司介绍
        searchItem = httpSoup.find('div', id='company_intro')
        corp_content = searchItem.find('span', class_='company_content').get_text()
        return {
            'title': unicode(product_url),
            'corp_type': unicode(corp_type),
            'corp_process': unicode(corp_process),
            'corp_number': unicode(corp_number),
            'corp_address': unicode(corp_address),
            'corp_content': unicode(corp_content),
            'product_profile': unicode(product_profile),
        }

if __name__ == '__main__':
    t = Scrape()
    keyword = '中科方德'
    keyword = '阿里巴巴'
    # t.searchItjuzi(keyword = keyword)
    item = t.searchLagou(keyword = keyword)
    for key in item:
        print key, item[key]
