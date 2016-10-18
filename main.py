#! /usr/bin/env python
#-*- coding:utf-8 -*-
import os
import re
import multiprocessing
currPath = os.getcwd()

from ScrapeLib.SaveData import SaveData
from ScrapeLib.Process import MultiProcess

import settings

def loadScrapy():
    spiderList = []
    spiderPath = os.path.join(currPath, 'spiders')
    parents = os.listdir(spiderPath)
    for parent in parents:
        if re.search('\.py$', parent):
            if parent != '__init__.py':
                spiderList.append(parent.replace('.py', ''))
    return spiderList

def parseScrapy(spider, msg_queue = None):
    print spider
    exec('from spiders.%s import Scrape' % spider)
    sp = Scrape()
    config = sp.init()

    # 存储实例
    config['saveIns'] = SaveData(os.path.join(currPath, 'output/'))

    if 'doctype' in config:
        if config['doctype'] == 'mysql':
            mysqlServer = settings.MYSQLSERVER
            config['saveIns'].mysqlConnect(mysqlServer)

    if 'range' in config:
        rangeIds = config['range']
        for rangeId in rangeIds:
            try:
                print '%s - %s' % (spider, rangeId)
                spData = sp.run(rangeId)
                config['indexs'] = [rangeId]
                saveScrapy(spData, config)
            except Exception as what:
                print '%s - %s' % (spider, what)
    else:
        try:
            spData = sp.run()
            saveScrapy(spData, config)
        except Exception as what:
            print what

def saveScrapy(data, config = {}):
    doctype = 'excel'
    if 'doctype' in config:
        doctype = config['doctype']

    table = 'test'
    if 'table' in config:
        table = config['table']

    id_offset = 0
    if 'id_offset' in config:
        id_offset = config['id_offset']

    newData = dict({
        'indexs': [1],
        'columns': data['columns'],
        'values': data['values']
    })
    if 'indexs' in config:
        newData['indexs'] = config['indexs']

    saveIns = config['saveIns']

    if doctype == 'excel':
        try:
            print ('%s-%s' % (table, newData['values'][0][0]))
            saveIns.excelWriter(newData, tb_name = table, if_exists = 'append', id_offset = id_offset)
        except Exception as what:
            print ('%s-%s' % (table, what))
        print 'excel saved'

    elif doctype == 'mysql':
        try:
            print ('%s-%s' % (table, newData['values'][0][0]))
            saveIns.mysqlWriter(newData, tb_name = table, if_exists = 'append')
        except Exception as what:
            print ('%s-%s' % (table, what))
        print 'mysql saved'


if __name__ == '__main__':

    msg_queue = multiprocessing.Queue()
    # 获取脚本
    spiderList = loadScrapy()
    # for spider in spiderList:
    #     parseScrapy(spider)

    # 初始化多进程
    spiderList = map(lambda x: (x,), spiderList)
    mp = MultiProcess(parseScrapy, process_num = len(spiderList), process_params = spiderList)
    mp.run(isJoin = False)
