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

    def search58Corp(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.code
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        corp_name = httpSoup.find('div', class_='compHead').find('a', class_='businessName').get_text().strip()
        if corp_name == '':
            raise Exception('no corp_name error')
        corp_fullname = ''

        # 公司基本信息
        corp_title = httpSoup.find('div', class_='basicMsg').find('ul', class_='basicMsgList')
        corp_item = corp_title.find('li')
        corp_item = corp_item.find_next_sibling().find_next_sibling().find_next_sibling()
##        print corp_item # 联系电话

        corp_item = corp_item.find_next_sibling()
        corp_process = corp_item.get_text().replace(u'公司性质：', '').strip()

        corp_item = corp_item.find_next_sibling()
        corp_link = corp_item.get_text().replace(u'企业网址：', '').strip()

        corp_item = corp_item.find_next_sibling()
        corp_number = corp_item.get_text().replace(u'公司规模：', '').strip()

        corp_item = corp_item.find_next_sibling()
        corp_address = corp_item.get_text().replace(u'公司地址：', '').replace(u'查看地图', '').strip()

        corp_item = corp_item.find_next_sibling()
        corp_type = corp_item.get_text().replace(u'公司行业：', '').strip()

##        print corp_process, corp_link, corp_number, corp_address, corp_type
        corp_products = []

        # 公司介绍
        corp_content = httpSoup.find('div', class_='compIntro').find('p').get_text().strip()

##        corp_contact = httpSoup.find('div', class_='company-content').find_all('p', class_='MsoNormal')[-1]
##        print corp_contact.get_text()

        return {
            'columns': ['corp_id', 'corp_name', 'corp_fullname', 'corp_type', 'corp_process', 'corp_number', 'corp_address', 'corp_content', 'corp_products', 'corp_link', 'created_at', 'updated_at'],
            'values': [[corp_id, corp_name, corp_fullname, corp_type, corp_process, corp_number, corp_address, corp_content, ','.join(corp_products), corp_link, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]]
        }

    def run(self, rangeId = 5124):
        url = 'http://qy.58.com/%d/' % rangeId
        item = self.search58Corp(url, rangeId)
        return item

    def init(self):
        return {
            'range': {
                'start': 1,
                'end':  107770926945303,
            },
            'threads': 5,
            'table': 'sp_58tc',
            'doctype': 'mysql',
            'id_offset': 0,
            'unique_key': 'corp_id'
        }

if __name__ == '__main__':
    t = Scrape()
    url = 'http://qy.58.com/37770926945303/'
    item = t.search58Corp(url)
    for key in item:
        print key, item[key]
