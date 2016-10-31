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

    def searchCjol(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.code
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        httpSoup = httpSoup.find('div', id='inner_left_main_inner')
        detail = httpSoup.find('div', class_='companyinfoshow')
        corp_name = detail.find('h1', class_='companyinfoshow_name_box').get_text().strip()
        corp_fullname = ''
        corp_link = detail.find('p', class_='companyinfoshow_link').find('a').get('href').strip()

        corp_items = httpSoup.find('div', class_='company_detailedinfo').find_all('li')
        # 公司基本信息
        corp_type = corp_items[0].get_text().replace(u'行业：', '').strip()
        corp_address = corp_items[1].get_text().replace(u'地址：', '').strip()
        corp_process = corp_items[5].get_text().replace(u'公司性质：', '').strip()
        corp_number = corp_items[4].get_text().replace(u'公司规模：', '').strip()

        corp_contact = ''
        corp_products = []

        # 公司介绍
        corp_content = httpSoup.find('div', class_='common_linebox_con').get_text().strip()
        corp_content = re.sub(r'\s+', '', corp_content)
        return {
            'columns': ['corp_id', 'corp_name', 'corp_fullname', 'corp_type', 'corp_process', 'corp_number', 'corp_address', 'corp_content', 'corp_products', 'corp_link', 'created_at', 'updated_at'],
            'values': [[corp_id, corp_name, corp_fullname, corp_type, corp_process, corp_number, corp_address, corp_content, ','.join(corp_products), corp_link, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]]
        }

    def run(self, rangeId = 272623):
        url = 'http://www.cjol.com/jobs/company-%d' % rangeId
        item = self.searchCjol(url, rangeId)
        return item

    def init(self):
        # 中国人才热线
        return {
            'range': {
                'start':     1,
                'end':  600001
            },
            'threads': 1,
            'table': 'sp_cjol',
            'doctype': 'mysql',
            'id_offset': 0,
            'unique_key': 'corp_id'
        }

if __name__ == '__main__':
    t = Scrape()
    item = t.run()
    for key in item:
        print key, item[key]
