#! /usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append('../')

import random, time, hashlib, re
from ScrapeLib.HttpRequest import HttpRequest
httpReq = HttpRequest()

# time_now = time.strftime("%Y/%m/%d", time.localtime())

class Scrape:
    def __init__(self):
        pass

    def getAnchorHref(self, soupData):
        httpSoup = self.bs4HttpData(unicode(soupData))
        searchList = httpSoup.findAll('a')
        urlList = []
        for searchItem in searchList:
            urlList.append(searchItem.get('href'))
        return urlList

    def searchLagou(self, keyword = ''):
        url = 'http://www.lagou.com/jobs/list_%s' % keyword
        httpData = httpReq.getData(url).read()
        httpSoup = httpReq.bs4HttpData(httpData)
        searchItem = httpSoup.find(id='positionHead')
        if searchItem is None:
            return 'Not Found'
        searchItem = searchItem.find('div', class_='company-card')
        searchItem = searchItem.find('li', class_='c_btn')
        searchUrls = self.getAnchorHref(searchItem)
        searchUrl = 'http:%s' % searchUrls[0]
        return self.searchLagouCorp(searchUrl)

    def searchLagouCorp(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.code
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        corp_title = httpSoup.find('div', class_='company_main').find('a')
        corp_name = corp_title.get_text().strip()
        corp_fullname = corp_title.get('title')
        corp_link = corp_title.get('href')
        # print corp_fullname
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
        corp_products = []
        searchItems = httpSoup.find('div', id='container_left').find('div', id='company_products').find_all('div', class_='product_details')
        for searchItem in searchItems:
            tmp = searchItem.find('div', 'product_url').find('a')
            product_name = tmp.get_text().strip()
            # product_url = tmp.get('href')
            # product_profile = searchItem.find('div', class_='product_profile').get_text()
            # corp_products.append({
            #         'product_name': product_name,
            #         'product_url': product_url,
            #         'product_profile': product_profile
            #     })
            corp_products.append(product_name)

        # 公司介绍
        searchItem = httpSoup.find('div', id='company_intro')
        corp_content = searchItem.find('span', class_='company_content').get_text()

        return {
            'columns': ['corp_id', 'corp_name', 'corp_fullname', 'corp_type', 'corp_process', 'corp_number', 'corp_address', 'corp_content', 'corp_products', 'corp_link', 'created_at', 'updated_at'],
            'values': [[corp_id, corp_name, corp_fullname, corp_type, corp_process, corp_number, corp_address, corp_content, ','.join(corp_products), corp_link, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]]
        }
        # return {
        #     'corp_name': unicode(corp_name),
        #     'corp_fullname': unicode(corp_fullname),
        #     'corp_type': unicode(corp_type),
        #     'corp_process': unicode(corp_process),
        #     'corp_number': unicode(corp_number),
        #     'corp_address': unicode(corp_address),
        #     'corp_content': unicode(corp_content).replace('\n', '  '),
        #     'corp_products': ','.join(corp_products),
        # }

    def run(self, rangeId = 5124):
        url = 'http://www.lagou.com/gongsi/%d.html' % rangeId
        item = self.searchLagouCorp(url, rangeId)
        return item

    def init(self):
        return {
            'range': range(1, 1000000),
            'table': 'sp_lagou',
            'doctype': 'mysql'
        }

if __name__ == '__main__':
    t = Scrape()
##    keyword = '中科方德'
##    keyword = '阿里巴巴'
##    item = t.searchLagou(keyword = keyword)
##    for key in item:
##        print key, item[key]
    url = 'http://www.lagou.com/gongsi/5124.html'
    # url = 'http://www.lagou.com/gongsi/4.html'
    item = t.searchLagouCorp(url)
    for key in item:
        print key, item[key]
