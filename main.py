#! /usr/bin/env python
#-*- coding:utf-8 -*-
import os
import re
import multiprocessing
import pdb
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

def parseScrapy(spider):
    print spider
    exec('from %s.%s import Scrape' % (spiderModule, spider))
    sp = Scrape()
    config = sp.init()
    if 'threads' in config:
        threads = config['threads']
    else:
        threads = 1

    if 'range' in config:
        range_ids = config['range']
        it_start = 0
        it_end = 0
        it_type = 'list'

        if isinstance(range_ids, dict):
            it_start = range_ids['start']
            it_end = range_ids['end']
            it_type = 'dict'
        elif isinstance(range_ids, list) or isinstance(range_ids, tuple):
            it_start = 0
            it_end = len(range_ids)
            it_type = 'list'
    else:
        raise Exception('please init ranges!')

    if (it_end - it_start) < threads:
        print ('warning: threads num < total ranges => auto lower threads!')
        threads = it_end - it_start

    it_step_float = (it_end - it_start) * 1.0 / threads
    it_step = int(it_step_float)
    if it_step != it_step_float:
        print ('warning: threads num cannot divisible by total range num => auto remove some range ids!')

    threadlist = []
    for thread in range(0, threads):
        it_end_t = it_start + it_step

        if it_type == 'dict':
            tmp_range = {
                'start': it_start,
                'end': it_end_t
            }
        elif it_type == 'list':
            tmp_range = range_ids[it_start : it_end_t]
        it_start = it_end_t

        init_config = {
            'spider': spider,
            'scrape_class': Scrape,
            'range': tmp_range,
            'range_type': it_type
        }
        init_config = dict(config, **init_config)
        threadlist.append(init_config)
    return threadlist


def runScrapy(config, msg_queue = None):
    spider = config['spider']
    print (spider)
    Scrape = config['scrape_class']
    sp = Scrape()

    # 存储实例
    config['saveIns'] = SaveData(os.path.join(currPath, 'output/'))

    if 'doctype' in config:
        if config['doctype'] == 'mysql':
            mysqlServer = settings.MYSQLSERVER
            config['saveIns'].mysqlConnect(mysqlServer)

    if 'range' in config:
        range_ids = config['range']
        it_start = 0
        it_end = 0
        it_type = config['range_type']

        if it_type == 'dict':
            it_start = range_ids['start']
            it_end = range_ids['end']
        elif it_type == 'list':
            it_start = 0
            it_end = len(range_ids)
        print ('%s range: %d-%d' % (spider, it_start, it_end))

        it_index = it_start
        while True:
            if it_index >= it_end:
                break
            if it_type == 'list':
                rangeId = range_ids[it_index]
            elif it_type == 'dict':
                rangeId = it_index
            it_index += 1
            try:
                print 'runspider %s - %s' % (spider, rangeId)
                spData = sp.run(rangeId)
                if 'indexs' not in spData:
                    config['indexs'] = [rangeId]
                saveScrapy(spData, config)
            except Exception as what:
                print 'runspider error: %s - %s' % (spider, what)
    else:
        raise Exception('please init ranges!')

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

    unique_key = None
    if 'unique_key' in config:
        unique_key = config['unique_key']

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
            print ('save spider %s-%s' % (table, newData['values'][0][0]))
            saveIns.excelWriter(newData, tb_name = table, if_exists = 'append', id_offset = id_offset)
        except Exception as what:
            print ('save errir %s-%s' % (table, what))
        print 'excel saved'

    elif doctype == 'mysql':
        try:
            print ('%s-%s' % (table, newData['values'][0][0]))
            saveIns.mysqlWriter(newData, tb_name = table, if_exists = 'append', unique_key = unique_key)
        except Exception as what:
            print ('%s-%s' % (table, what))
        print 'mysql saved'


if __name__ == '__main__':

    msg_queue = multiprocessing.Queue()
    # 获取脚本
    spiderlist = loadScrapy()

    processlist = []
    for spider in spiderlist:
        processlist.extend(parseScrapy(spider))
    # print processlist

    # # for debug
    # for process in processlist:
    #     runScrapy(process)

    # 初始化多进程
    processlist = map(lambda x: (x,), processlist) # 多进程参数必须为tuple
    mp = MultiProcess(runScrapy, process_num = len(processlist), process_params = processlist)
    mp.run(isJoin = False)
