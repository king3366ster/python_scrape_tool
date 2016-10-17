#! /usr/bin/env python
#-*- coding:utf-8 -*-
import os
import re
currPath = os.getcwd()

from ScrapeLib.SaveData import SaveData
sd = SaveData(os.path.join(currPath, 'output/'))

def loadScrapy():
    spiderList = []
    spiderPath = os.path.join(currPath, 'spiders')
    parents = os.listdir(spiderPath)
    for parent in parents:
        if re.search('\.py$', parent):
            if parent != '__init__.py':
                spiderList.append(parent.replace('.py', ''))
    return spiderList

def parseScrapy(spider):
    print spider
    exec('from spiders.%s import Scrape' % spider)

    sp = Scrape()
    config = sp.init()
    if 'range' in config:
        rangeIds = config['range']
        for rangeId in rangeIds:
            try:
                print '%s - %s' % (spider, rangeId)
                spData = sp.run(rangeId)
                config['indexs'] = [rangeId]
                saveScrapy(spData, config)
            except Exception as what:
                print what
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

    if doctype == 'excel':
        newData = dict({
                'indexs': [6],
                'columns': data['columns'],
                'values': data['values']

            })
        if 'indexs' in config:
            newData['indexs'] = config['indexs']
        try:
            print newData['values'][0][0]
            sd.excelWriter(newData, node = table, if_exists = 'append')
        except Exception as what:
            print what
        print 'excel saved'



if __name__ == '__main__':

    spiderList = loadScrapy()
    for spider in spiderList:
        parseScrapy(spider)
