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

    def searchZhaopinCorp(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.code
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        httpSoup = httpSoup.find('div', class_='mainLeft')
        corp_name = httpSoup.find('h1').get_text().strip()
        corp_fullname = ''

        corp_title = httpSoup.find('table', class_='comTinyDes')
        corp_items = corp_title.find_all('tr')

        # 公司基本信息
        corp_process = corp_items[0].get_text().replace(u'公司性质：', '').strip()
        corp_number = corp_items[1].get_text().replace(u'公司规模：', '').strip()
        corp_link = corp_items[2].get_text().replace(u'公司网站：', '').strip()
        corp_type = corp_items[3].get_text().replace(u'公司行业：', '').strip()
        corp_address = corp_items[4].get_text().replace(u'公司地址：', '').replace(u'查看公司地图', '').strip()

        corp_products = []

        # 公司介绍
        corp_content = httpSoup.find('div', class_='company-content').get_text().strip()
##        corp_contact = httpSoup.find('div', class_='company-content').find_all('p', class_='MsoNormal')[-1]
##        print corp_contact.get_text()

        return {
            'columns': ['corp_id', 'corp_name', 'corp_fullname', 'corp_type', 'corp_process', 'corp_number', 'corp_address', 'corp_content', 'corp_products', 'corp_link', 'created_at', 'updated_at'],
            'values': [[corp_id, corp_name, corp_fullname, corp_type, corp_process, corp_number, corp_address, corp_content, ','.join(corp_products), corp_link, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]]
        }

    def run(self, rangeId = 5124):
        url = 'http://company.zhaopin.com/CC%d.html' % rangeId
        item = self.searchZhaopinCorp(url, rangeId)
        return item

    def init(self):
        return {
            'range': {
                'start': 100000001,
                'end':  1009732211
            },
            'threads': 5,
            'table': 'sp_zhaopin',
            'doctype': 'mysql',
            'id_offset': 0,
            'unique_key': 'corp_id'
        }

if __name__ == '__main__':
    t = Scrape()
    url = 'http://company.zhaopin.com/CC209732211.htm'
    item = t.searchZhaopinCorp(url)
    for key in item:
        print key, item[key]
