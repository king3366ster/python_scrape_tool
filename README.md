# python_scrape_tool
python爬虫引擎

## 安装依赖
- pip install xmltodict
- pip install bs4
- pip install lxml
- pip install openpyxl
- pip install mysql DBUtils
** 若使用最小近邻字符比较
- pip install python-Levenshtein

## 工程原理
- 在settings目录下配置工程全局配置，如MysqlServer相关参数
- 在spiders里添加需要执行的爬虫脚本，至少需要包含：
  - Scrape类, 其下只是需要包含init方法与run方法
    - init 函数，返回相应的配置信息，包括：爬虫网站变量id(range)、存储文件类型如mysql/excel(doctype)、存储对应数据库表名或excel文件名(table)、已经id的偏置(id_offset)
    - run 函数，实际多进程执行的主函数，最终在函数中返回dict类型的数据，包含columns字段与values字段；values字段需为二位数组（因为爬虫脚本允许多个网页数据合并，综合输出）
- 在命令行中执行 python main.py，爬虫工程即自动多进程执行工程spiders目录下的爬虫脚本（一个脚本一个进程）

## 公共方法
- spiders 可调用的公共方法均在ScrapeLib下，主要包含用于网站请求的：
  1. HttpRequest类
    - 由于某些网站做了反爬虫，会需要进行用户登录认证，HttpRequest方法中的请求均使用了cookie粘连，记录用户每次请求所获得的cookie，用于二次访问网站
  2. Process类
    - 一般不需要用户收到调用，已在main.py中使用了多进程实例
  3. SaveData类
    - 用于建立mysql连接、excel读写等
