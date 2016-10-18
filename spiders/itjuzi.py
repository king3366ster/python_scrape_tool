#! /usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append('../')

import random, time, hashlib, re
from ScrapeLib.HttpRequest import HttpRequest
httpReq = HttpRequest()

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

    def searchItjuziCorp(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        corp_title = httpSoup.find('div', class_='thewrap').find('div', class_ = 'rowhead')
        corp_name = corp_title.find('div', class_='line-title').find('b').get_text().strip()
        corp_name = re.subn('\s+', '', corp_name)
        corp_process = corp_title.find('div', class_='line-title').find('b').find('span', class_='t-small').get_text().strip()

        corp_name = corp_name[0].replace(corp_process, '')
        corp_process = corp_process.replace('(', '').replace(')', '')

        # 公司基本信息
        corp_type = corp_title.find('span', class_ = 'c-gray-aset').find_all('a')[1].get_text().strip()

        corp_address = corp_title.find('span', class_ = 'loca').get_text().strip()
        corp_address = re.subn('\s+', '', corp_address)[0]
        corp_link = corp_title.find('a', class_ = 'weblink').get('href')

        # 产品介绍
        corp_products = []
        searchItems = httpSoup.find('ul', class_='list-prod').find_all('div', class_='on-edit-hide')
        for searchItem in searchItems:
            tmp = searchItem.find('b').find('a')
            product_name = tmp.get_text().strip()
            # product_url = tmp.get('href')
            # product_profile = searchItem.find('p').get_text()
            # corp_products.append({
            #         'product_name': product_name,
            #         'product_url': product_url,
            #         'product_profile': product_profile
            #     })
            corp_products.append(product_name)

        # 公司介绍
        searchItem = httpSoup.find('div', class_='block-inc-info')
        corp_content = searchItem.find('div', class_='des').get_text().strip()
        corp_descs = searchItem.find('div', class_='des-more').find_all('div')
        corp_fullname = corp_descs[0].get_text().strip().replace(u'公司全称：', '')
        corp_number = corp_descs[1].find_all('span')[1].get_text().strip().replace(u'公司规模：', '')

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

    def run(self, rangeId = 666):
        url = 'http://itjuzi.com/company/%d' % rangeId
        item = self.searchItjuziCorp(url, rangeId)
        return item

    def init(self):
        return {
            'range': range(1, 400000),
            'table': 'sp_itjuzi',
            'doctype': 'mysql'
        }

if __name__ == '__main__':
    t = Scrape()
##    keyword = '中科方德'
##    keyword = '阿里巴巴'
##    item = t.searchLagou(keyword = keyword)
##    for key in item:
##        print key, item[key]

    item = t.run()
    for key in item:
        print key, item[key]
