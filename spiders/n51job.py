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

    def search51jobCorp(self, url, corp_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.code
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        httpSoup = httpSoup.find('div', class_='tCompany_center')
        corp_title = httpSoup.find('div', class_='tHeader')
        corp_name = corp_title.find('h1').get_text().strip()
        corp_fullname = ''

        corp_link = url
        corp_info = corp_title.find('p', class_='ltype').get_text().strip()
        corp_info = re.split(r'\|', corp_info)

        # 公司基本信息
        corp_type = corp_info[2].strip()
        corp_process = corp_info[0].strip()
        corp_number = corp_info[1].strip()

        corp_address = httpSoup.find('div', class_ = 'bmsg').find('p', class_ = 'fp').get_text().replace('\n', '')
        corp_address = re.subn(r'\s+', ' ', corp_address)[0].strip()
        corp_products = []

        # 公司介绍
        corp_content = httpSoup.find('div', class_='con_msg').find('p').get_text().strip()
        corp_content = re.subn(r'\s+', ' ', corp_content)[0]

        return {
            'columns': ['corp_id', 'corp_name', 'corp_fullname', 'corp_type', 'corp_process', 'corp_number', 'corp_address', 'corp_content', 'corp_products', 'corp_link', 'created_at', 'updated_at'],
            'values': [[corp_id, corp_name, corp_fullname, corp_type, corp_process, corp_number, corp_address, corp_content, ','.join(corp_products), corp_link, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]]
        }

    def run(self, rangeId = 5124):
        url = 'http://jobs.51job.com/all/co%d.html' % rangeId
        item = self.search51jobCorp(url, rangeId)
        return item

    def init(self):
        return {
            'range': {
                'start': 1,
                'end': 10000000
            },
            'threads': 4,
            'table': 'sp_51job',
            'doctype': 'mysql',
            'id_offset': 0,
            'unique_key': 'corp_id'
        }

if __name__ == '__main__':
    t = Scrape()
    url = 'http://jobs.51job.com/all/co3485436.html'
    item = t.search51jobCorp(url)
    for key in item:
        print key, item[key]
