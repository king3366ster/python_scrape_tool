#! /usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
sys.path.append('../')

import random, time, hashlib, re
import urllib, cStringIO
from ScrapeLib.HttpRequest import HttpRequest
# import ScrapeLib.pytesser.pytesser as pytesser

httpReq = HttpRequest()

# time_now = time.strftime("%Y/%m/%d", time.localtime())

class Scrape:
    def __init__(self):
        pass

    def searchGanjiCorp(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.code
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        httpSoup = httpSoup.find('div', id='wrapper')
        corp_name = httpSoup.find('div', class_='c-title').find('h1').get_text().strip()
        corp_fullname = ''

        corp_items = httpSoup.find('ul', class_='clearfix').find_all('li')

        # 公司基本信息
        corp_number = corp_items[1].get_text().replace(u'公司规模：', '').strip()
        corp_link = corp_items[2].find('a').get('href').strip()
        corp_type = corp_items[2].get_text().replace(u'公司行业：', '').strip()
        corp_process = corp_items[3].get_text().replace(u'公司类型：', '').strip()
        corp_address = corp_items[6].get_text().replace(u'公司地址：', '').strip()
        corp_contact = corp_items[5].find('img').get('src')
        corp_contact = 'http://www.ganji.com%s' % corp_contact
        corp_contact_name = corp_items[4].get_text().replace(u'联 系 人：', '').strip()
        corp_contact = '%s:<img src="%s">' % (corp_contact_name, corp_contact)
        # pytesser.recognize_image(corp_contact)

        corp_products = []

        # 公司介绍
        corp_content = httpSoup.find('p', id='company_description').get_text().strip()

        return {
            'columns': ['corp_id', 'corp_name', 'corp_fullname', 'corp_type', 'corp_process', 'corp_number', 'corp_address', 'corp_content', 'corp_products', 'corp_contact', 'corp_link', 'created_at', 'updated_at'],
            'values': [[corp_id, corp_name, corp_fullname, corp_type, corp_process, corp_number, corp_address, corp_content, ','.join(corp_products), corp_contact, corp_link, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]]
        }

    def run(self, rangeId = 43611725):
        url = 'http://www.ganji.com/gongsi/%d/' % rangeId
        item = self.searchGanjiCorp(url, rangeId)
        return item

    def init(self):
        return {
            'range': {
                'start':      1,
                'end': 50000001
            },
            'threads': 10,
            'table': 'sp_ganji',
            'doctype': 'mysql',
            'id_offset': 0,
            'unique_key': 'corp_id'
        }

if __name__ == '__main__':
    t = Scrape()
    item = t.run()
    for key in item:
        print key, item[key]
