#coding:utf-8
import datetime

class ORM(object):
    #服务器
    username = 'hao'
    password = '991004'
    host = 'localhost'
    port = '3306'
    database= 'news-aggregation'

    # #本机
    # username = 'root'
    # password = ''
    # host = 'localhost'
    # port = '3306'
    # database = 'hahaha'

    today = str(datetime.date.today())

class MainConfig(object):
    log_path = "log/main.log"

class PipelineConfig(object):
    log_path = "log/pipelines.log"

class FuncConfig(object):
    log_path = "log/req.log"

class TencentConfig(object):
    site_id = 2
    site_name = '腾讯'
    log_path = "log/tencent.log"

class SinaConfig(object):
    site_id = 3
    site_name = '新浪'
    log_path = "log/sina.log"

class NeteaseConfig(object):
    site_id = 7
    site_name = '网易新闻'
    log_path = "log/netease.log"

class XinHuaConfig(object):
    site_id = 9
    site_name = '新华网'
    log_path = "log/xinhua.log"

class BBCConfig(object):
    site_id = 12
    site_name = 'bbc'
    log_path = "log/bbc.log"

class iFengConfig(object):
    site_id = 12
    site_name = '凤凰网'
    log_path = "log/ifeng.log"