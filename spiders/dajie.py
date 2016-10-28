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

    def searchDajie(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.code
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        httpSoup = httpSoup.find('div', class_='cor-container')
        detail = httpSoup.find('div', class_='detail-box')
        corp_name = detail.find('h3').get_text().strip()
        corp_fullname = ''
        corp_items = httpSoup.find('ul', class_='detail').find_all('li')

        # 公司基本信息
        corp_type = corp_items[0].get_text().replace(u'行业：', '').strip()
        corp_type = re.sub(r'\s+', '', corp_type)
        corp_process = corp_items[1].get_text().replace(u'性质：', '').strip()
        corp_number = corp_items[2].get_text().replace(u'规模：', '').strip()
        corp_link = corp_items[3].get_text().replace(u'网址：', '').strip()
        if corp_link == u'暂无':
            corp_link = 'http://www.dajie.com/corp-pro/%d' % corp_id
        corp_area = corp_items[4].get_text().replace(u'地区：', '').strip()
        corp_address = corp_items[5].get_text().replace(u'地址：', '').strip()
        corp_address = re.sub(r'\s+', '', corp_area) + ' - ' + re.sub(r'\s+', '', corp_address)

        corp_contact = ''
        corp_products = []

        # 公司介绍
        corp_content = httpSoup.find('div', class_='compny-desc').find('p', class_='desc').get_text().strip()
        corp_content = re.split(r'\s+', corp_content)
        corp_content = map(lambda x: x.strip(), corp_content)
        corp_content = ' '.join(corp_content)
        return {
            'columns': ['corp_id', 'corp_name', 'corp_fullname', 'corp_type', 'corp_process', 'corp_number', 'corp_address', 'corp_content', 'corp_products', 'corp_link', 'created_at', 'updated_at'],
            'values': [[corp_id, corp_name, corp_fullname, corp_type, corp_process, corp_number, corp_address, corp_content, ','.join(corp_products), corp_link, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]]
        }

    def run(self, rangeId = 1001899): #2811939):
        url = 'http://www.dajie.com/corp-pro/%d/' % rangeId
        item = self.searchDajie(url, rangeId)
        return item

    def init(self):
        return {
            'range': {
                'start':       1,
                'end':  4000001
            },
            'threads': 4,
            'table': 'sp_dajie',
            'doctype': 'mysql',
            'id_offset': 0,
            'unique_key': 'corp_id'
        }

if __name__ == '__main__':
    t = Scrape()
    item = t.run()
    for key in item:
        print key, item[key]
