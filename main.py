#! /usr/bin/env python
#-*- coding:utf-8 -*-
import os
import re
import multiprocessing
currPath = os.getcwd()

from ScrapeLib.SaveData import SaveData
from ScrapeLib.Process import MultiProcess

import settings
try:
    spiderModule = settings.SPIDERPATH
except:
    spiderModule = 'spiders'

def loadScrapy():
    spiderList = []
    spiderPath = os.path.join(currPath, spiderModule)
    parents = os.listdir(spiderPath)
    for parent in parents:
        if re.search('\.py$', parent):
            if parent != '__init__.py':
                spiderList.append(parent.replace('.py', ''))
    return spiderList

def parseScrapy(spider, msg_queue = None):
    print spider
    exec('from %s.%s import Scrape' % (spiderModule, spider))
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
        it_start = 0
        it_end = 0
        it_type = 'list'
        if isinstance(rangeIds, dict):
            it_start = rangeIds['start']
            it_end = rangeIds['end']
            it_type = 'dict'
        elif isinstance(rangeIds, list) or isinstance(rangeIds, tuple):
            it_start = rangeIds[0]
            it_end = rangeIds[-1]
            it_type = 'list'
        it_index = it_start
        while True:
            if it_index >= it_end:
                break
            if it_type == 'list':
                rangeId = rangeIds[it_index]
            elif it_type == 'dict':
                rangeId = it_index
            it_index += 1
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
