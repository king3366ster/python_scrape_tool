# -*- coding:utf-8 -*-

import os, re, json
import datetime
import pandas as pd
import tushare as ts
# import numpy as np
from ScrapeLib.HttpRequest import HttpRequest

xhr = HttpRequest()

def get_qgqp (page = 1):
  url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=QGQP_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=Code&sr=1&p=%d&ps=50&rt=50507794' % page
  data = xhr.getData(url).read().decode('utf-8', 'ignore')
  df = pd.DataFrame(json.loads(data))
  df.to_excel(u'data/千股千评%d.xlsx' % page)
  return df

def get_ylyc (page = 1):
  # url = 'http://data.eastmoney.com/report/ylyc.html'
  # url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=GEMCPF&st=(AllNum)&sr=-1&p=%d&ps=50&cb=&token=3a965a43f705cf1d9ad7e1a3e429d622&rt=50507142' % page
  url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=GEMCPF&st=(AllNum)&sr=-1&p=%d&ps=50&cb=&token=3a965a43f705cf1d9ad7e1a3e429d622&rt=51641551' % page
  data = xhr.getData(url).read().decode('utf-8', 'ignore')
  data = data[3:-3]
  data = re.split(r'","', data)
  result = []
  for item in data:
    info = item.split(',')
    if info[3] == '-':
      info[3] = 0
    result.append({
      u'code': '%06d' % int(info[1]),
      u'name': info[2],
      u'price': float(info[3]),
      u'change': info[4],
      u'research_num': int(info[5]),
      u'research_buy': int(info[6]),
      u'research_add': int(info[7]),
      u'research_mid': int(info[8]),
      u'research_del': int(info[9]),
      u'research_sel': int(info[10]),
      u'2017_profit': info[11],
      u'2018_profit': info[12],
      u'2018_pe': info[13],
      u'2019_profit': info[14],
      u'2019_pe': info[15],
      u'2020_profit': info[16],
      u'2020py_pe': info[17],
    })
  df = pd.DataFrame(result)
  col = df['code']
  df.drop(labels=['code'], axis=1, inplace=True)
  df.insert(0, 'code', col)
  col = df['name']
  df.drop(labels=['name'], axis=1, inplace=True)
  df.insert(1, 'name', col)
  df.to_excel(u'data/盈利预测%d.xlsx' % page)
  return df

if __name__ == '__main__':
## 盈利预测
  for page in range(1, 71):
    print (page)
    get_ylyc(page)

  df = None
  for page in range(1, 71):
    print (page)
    filename = u'data/盈利预测%d.xlsx' % page
    df_tmp = pd.read_excel(filename)
    if df is None:
      df = df_tmp
    else:
      df = pd.concat([df, df_tmp], axis=0, join='outer')
  df = df.reset_index(drop = True)
  df['code'] = df['code'].astype('str')
  for index, item in df.iterrows():
    df = df.set_value(index, 'code', '%06d' % int(item.code))
  df = df[df['research_num']>10]
  df.sort_values(by='research_buy', ascending=False, inplace=True)
  df.to_excel(u'盈利预测.xlsx')

  # for page in range(1, 73):
  #   print page
  #   get_qgqp(page)

  # df = None
  # for page in range(1, 73):
  #   print page
  #   filename = u'盈利预测/千股千评%d.xlsx' % page
  #   df_tmp = pd.read_excel(filename)
  #   if df is None:
  #     df = df_tmp
  #   else:
  #     df = pd.concat([df, df_tmp], axis=0, join='outer')
  # df = df.reset_index(drop = True)
  # df = df.rename(columns={
  #   'Code': 'code',
  #   'Name': 'name'
  # })
  # df.to_excel(u'千股千评.xlsx')

## 业绩报表
  # for year in range(2014, 2018):
  #   for month in range(1, 5):
  #     print '%d-%d' % (year, month)
  #     df = ts.get_report_data(year, month)
  #     df.to_excel(u'报表数据/业绩报告%d-%d.xlsx' % (year, month))
  #     df = ts.get_profit_data(year, month)
  #     df.to_excel(u'报表数据/盈利能力%d-%d.xlsx' % (year, month))

  # ttm_date = [
  #   '2016-4',
  #   '2017-1',
  #   '2017-2',
  #   '2017-3',
  # ]
  # ttm_profits = {}
  # for d in ttm_date:
  #   ttm_profits[d] = pd.read_excel(u'报表数据/盈利能力%s.xlsx' % d)

  # df_profit = pd.read_excel(u'盈利预测.xlsx')
  # data = []
  # for index, item in df_profit.iterrows():
  #   # code = '%06d' % item.code
  #   code = item.code
  #   print code
  #   eps = 0
  #   eps_count = 0
  #   for d in ttm_date:
  #     df_tmp = ttm_profits[d]
  #     df_tmp = df_tmp[df_tmp['code'] == int(code)]
  #     if not df_tmp.empty:
  #       eps += df_tmp.iloc[0].eps
  #       eps_count += 1.0
  #   data.append({
  #     'code': code,
  #     'eps_ttm': eps/(eps_count + 0.0001),
  #     'eps_count': eps_count
  #   })
  # df_eps = pd.DataFrame(data
  # df = df_profit.merge(df_eps, how='left', on='code')
  # df.to_excel(u'盈利预测_PETTM.xlsx')
  
  # df_basic = ts.get_stock_basics()
  # df_basic.to_excel(u'基本信息.xlsx')
  # df_basic = pd.read_excel(u'千股千评.xlsx')
  # df_profit = pd.read_excel(u'盈利预测.xlsx')
  # df = df_basic.merge(df_profit, how='left', on=['code', 'name'])
  # df.to_excel(u'盈利预测_PE.xlsx')

