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

    def searchZhihu(self, url, range_id = 1):
        httpRes = httpReq.getData(url)
        # print httpRes.info()
        httpSoup = httpReq.bs4HttpData(httpRes.read())
        zh_main = httpSoup.find('div', class_='zu-main-content')

        question_title = zh_main.find('div', id='zh-question-title').find('span', class_='zm-editable-content').get_text().strip()
        question_detail = zh_main.find('div', id='zh-question-detail').find('div', class_='zm-editable-content').get_text().strip()

        answer_main = zh_main.find('div', id='zh-question-answer-wrap').find_all('div', class_='zm-item-answer')

        answer_count = 0
        answer_list = []
        created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        for answer in answer_main:
            answer_item = httpReq.bs4HttpData(unicode(answer))

            answer_id = answer_item.find('div', class_='zm-item-answer').get('data-atoken')

            answer_author = answer_item.find('div', class_='zm-item-answer-author-info')
            author_link = answer_author.find('a', class_='author-link')
            if author_link:
                answer_author_name = author_link.get_text().strip()
                answer_author_link = 'https://www.zhihu.com%s' % author_link.get('href')
            else:
                answer_author_name = u'匿名用户'
                answer_author_link = ''
##            print answer_author_name, answer_author_link
            answer_vote = answer_item.find('span', class_='js-voteCount').get_text()
##            print vote_count
            answer_date = answer_item.find('a', class_='answer-date-link').get_text()
##            print answer_date
            answer_content = answer_item.find('div', class_='zm-editable-content').get_text().strip()
            answer_count += 1

            answer_list.append([
                answer_id,
                range_id,
                question_title,
                question_detail,
                answer_author_name,
                answer_author_link,
                answer_date,
                answer_vote,
                answer_content,
                created_at,
                updated_at
            ])

        answer_main = zh_main.find('div', id='zh-question-collapsed-wrap').find_all('div', class_='zm-item-answer')
        for answer in answer_main:
            answer_item = httpReq.bs4HttpData(unicode(answer))

            answer_id = answer_item.find('div', class_='zm-item-answer').get('data-atoken')
            answer_author = answer_item.find('div', class_='zm-item-answer-author-info')
            author_link = answer_author.find('a', class_='author-link')
            if author_link:
                answer_author_name = author_link.get_text().strip()
                answer_author_link = 'https://www.zhihu.com%s' % author_link.get('href')
            else:
                answer_author_name = u'匿名用户'
                answer_author_link = ''
##            print answer_author_name, answer_author_link
            answer_vote = answer_item.find('span', class_='js-voteCount').get_text()
##            print vote_count
            answer_date = answer_item.find('a', class_='answer-date-link').get_text()
##            print answer_date
            answer_content = answer_item.find('div', class_='zm-editable-content').get_text().strip()
            answer_content = re.subn(r'\s+', ' ', answer_content)[0]
            answer_count += 1

            answer_list.append([
                answer_id,
                range_id,
                question_title,
                question_detail,
                answer_author_name,
                answer_author_link,
                answer_date,
                answer_vote,
                answer_content,
                created_at,
                updated_at
            ])
            # answer_list.append({
            #     'answer_id': answer_id,
            #     'question_id': range_id,
            #     'question_title': question_title,
            #     'question_detail': question_detail,
            #     'answer_author_name': answer_author_name,
            #     'answer_author_link': answer_author_link,
            #     'answer_date': answer_date,
            #     'answer_vote': answer_vote,
            #     'answer_content': answer_content,
            #     'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            #     'updated_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # })

        return {
            'columns': ['answer_id', 'question_id', 'question_title', 'question_detail', 'answer_author_name', 'answer_author_link', 'answer_date', 'answer_vote', 'answer_content', 'created_at', 'updated_at'],
            'values': answer_list
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

    def run(self, rangeId = 21031319):
        url = 'https://www.zhihu.com/question/%d' % rangeId
        item = self.searchZhihu(url, rangeId)
        return item

    def init(self):
        return {
            'range': {
                'start': 10000000,
                'end': 99999999
            },
            # 'range': [1,3,8,2,41,42,12,32,13],
            'threads': 5,
            'table': 'sp_zhihu',
            'doctype': 'mysql',
            'unique_key': ['question_id', 'answer_id']
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
