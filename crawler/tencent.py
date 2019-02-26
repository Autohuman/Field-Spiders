#coding:utf-8
import sys
sys.path.append("..")
from config import TencentConfig as tc
from logger import Logger
from pipelines import Pipeline

from func import Req
import json
import datetime

class Tencent(object):
    open_api = 'https://pacaio.match.qq.com/openapi/json?'
    rcd_api = 'https://pacaio.match.qq.com/irs/rcd?'
    params = {}

    def __init__(self):
        open_type = []
        ent = {
            'type': 'ent',
            'api': '',
            'field_id': [1, 2]
        }
        open_type.append(ent)
        sports = {
            'type': 'sports',
            'api': '',
            'field_id': 2
        }
        open_type.append(sports)
        finance = {
            'type': 'finance',
            'field_id': 4
        }
        open_type.append(finance)
        tech = {
            'type': 'tech',
            'field_id': 5
        }
        open_type.append(tech)
        fashion = {
            'type': 'fashion',
            'field_id': 6
        }
        open_type.append(fashion)
        life = {
            'type': 'edu',
            'field_id': 7
        }
        open_type.append(life)
        cul = {
            'type': 'cul',
            'field_id': 8
        }
        open_type.append(cul)
        self.open_type = open_type
        rcd_type = []

        rcd_ent = {
            'cid': '92',
            'token': '54424c1ebe77ea829a41040a3620d0e7',
            'ext': 'ent',
            'field_id': 1
        }
        rcd_type.append(rcd_ent)
        rcd_milite = {
            'cid': '135',
            'token': '6e92c215fb08afa901ac31eca115a34f',
            'ext': 'milite_pc',
            'field_id': 3
        }
        rcd_type.append(rcd_milite)
        rcd_tech = {
            'cid': '135',
            'token': '6e92c215fb08afa901ac31eca115a34f',
            'ext': 'tech',
            'field_id': 5
        }
        rcd_type.append(rcd_tech)
        rcd_politics1 = {
            'cid': '135',
            'token': '6e92c215fb08afa901ac31eca115a34f',
            'ext': 'world',
            'field_id': 9
        }
        rcd_politics2 = {
            'cid': '108',
            'token': '349ee24cdf9327a050ddad8c166bd3e3',
            'ext': 'politics',
            'field_id': 9
        }
        rcd_politics3 = {
            'cid': '4',
            'token': '9513f1a78a663e1d25b46a826f248c3c',
            'ext': 'politics',
            'field_id': 9
        }
        rcd_type.append(rcd_politics1)
        rcd_type.append(rcd_politics2)
        rcd_type.append(rcd_politics3)
        self.rcd_type = rcd_type

    def api_requests(self):
        for x in self.open_type:
            type = x['type']
            date = int(str(datetime.datetime.today())[:10].replace('-',''))
            for i in range(date-15,date+1):   #启用此选项以从open/api爬取多日信息
                self.params['key'] = type + ":" + str(date)
                response = Req(self.open_api, params=self.params).get_select()
                data = json.loads(response.content.decode('utf8'))['data']
                for i in data:
                    item = dict()
                    item['datetime'] = i['publish_time']
                    item['link'] = i['url']
                    item['title'] = i['title']
                    item['field'] = x['field_id']
                    item['status'] = True
                    item['home'] = False
                    yield item


    def rcd_requests(self):
        for x in self.rcd_type:
            for page in range(15):
                params = {
                    'cid': x['cid'],
                    'token': x['token'],
                    'ext': x['ext'],
                    'page': page
                }
                response = Req(url=self.rcd_api,params=params).get_select()
                data = json.loads(response.content.decode('utf8'))['data']
                for i in data:
                    item = dict()
                    item['datetime'] = i['publish_time']
                    item['link'] = i['url']
                    item['title'] = i['title']
                    item['field'] = x['field_id']
                    item['status'] = True
                    item['home'] = False
                    yield item

def run():

    tc.log_path = "../" + tc.log_path
    sets = Pipeline(tc.site_id, tc.site_name).structure_set()
    Pipeline(tc.site_id, tc.site_name).open_spider(sets)
    for item in Tencent().api_requests():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)
    for item in Tencent().rcd_requests():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)

    try:
        Pipeline(tc.site_id, tc.site_name).close_spider()
    except:
        Logger().setLogger(tc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
