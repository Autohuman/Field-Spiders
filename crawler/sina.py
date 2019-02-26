#coding:utf-8
import sys
sys.path.append("..")
from config import SinaConfig as tc
from logger import Logger
from pipelines import Pipeline

from func import Req
import json
import datetime

class Sina(object):
    api = 'http://feed.mix.sina.com.cn/api/roll/get?'
    fashion_api = 'https://interface.sina.cn/pc_api/public_news_data.d.json?'

    def __init__(self):
        api_1 = []
        ent = {
            'lid': '2513',
            'field_id': 1
        }
        api_1.append(ent)
        sports = {
            'lid': '2512',
            'field_id': 2
        }
        api_1.append(sports)
        milite = {
            'lid': '2514',
            'field_id': 3
        }
        api_1.append(milite)
        finance_1 = {
            'lid': '2516',
            'field_id': 4
        }
        api_1.append(finance_1)
        finance_2 = {
            'lid': '2517',
            'field_id': 4
        }
        api_1.append(finance_2)
        finance_3 = {
            'lid': '2518',
            'field_id': 4
        }
        api_1.append(finance_3)
        tech = {
            'lid': '2515',
            'field_id': 5
        }
        api_1.append(tech)
        all = {
            'lid': '2509',
            'field_id': None
        }
        api_1.append(all)
        life = {
            'lid': '2669',
            'field_id': 7
        }
        api_1.append(life)
        politics_1 = {
            'lid': '2510',
            'field_id': 9
        }
        api_1.append(politics_1)
        politics_2 = {
            'pageid': '153',
            'lid': '2511',
            'field_id': 9
        }
        api_1.append(politics_2)
        self.api_1 = api_1

        culture = {
            'pageid': '411',
            'lid': '2595',
            'field_id': 8,
            'num': '100',
        }
        self.culture = culture

        fashion = {
            'cids': '260',
            'pageSize': '20',
            'down': '0',
            'field_id': 6
        }
        self.fashion = fashion

    def api_requests(self):
        for x in self.api_1:
            params = {
                'pageid': '153',
                'lid': x['lid'],
                'num': '50'
            }
            for page in range(1,51):
                params['page'] = page
                try:
                    response = Req(url=self.api, params=params).get_select()
                    print(response.url)
                    data = json.loads(response.content.decode('utf8'))['result']['data']
                    for i in data:
                        item = dict()
                        item['link'] = i['url']
                        item['title'] = i['title']
                        item['datetime'] = datetime.datetime.utcfromtimestamp(int(i['intime'])).strftime(
                            "%Y-%m-%d %H:%M:%S")
                        item['field'] = x['field_id']
                        item['status'] = False
                        item['home'] = False
                        yield item
                except:
                    print(self.api)
                    print(params)
                    print("Failed to get web page json")

    def culture_req(self):
        x = self.culture
        params = {
            'pageid': x['pageid'],
            'lid': x['lid'],
            'num': '22'
        }
        for page in range(1,51):
            params['page'] = page
            try:
                response = Req(url=self.api, params=params).get_select()
                print(response.url)
                data = json.loads(response.content.decode('utf8'))['result']['data']
                for i in data:
                    item = dict()
                    item['link'] = i['url']
                    item['title'] = i['title']
                    item['datetime'] = datetime.datetime.utcfromtimestamp(int(i['intime'])).strftime(
                        "%Y-%m-%d %H:%M:%S")
                    item['field'] = x['field_id']
                    item['status'] = False
                    item['home'] = False
                    yield item
            except:
                print(self.api)
                print(params)
                print("Failed to get web page json")

    def fashion_req(self):
        x = self.fashion
        params = {
            'cids': x['cids'],
            'pageSize': '20',
            'editLevel': '0,1,2,3',
            'down': 0
        }
        for page in range(50):
            params['up'] = page
            try:
                response = Req(url=self.fashion_api, params=params).get_select()
                data = json.loads(response.content.decode('utf8'))['data']
                for i in data:
                    item = dict()
                    item['link'] = i['url']
                    item['title'] = i['title']
                    item['datetime'] = datetime.datetime.utcfromtimestamp(int(i['ctime'])).strftime("%Y-%m-%d %H:%M:%S")
                    item['field'] = x['field_id']
                    item['status'] = False
                    item['home'] = False
                    yield item
            except:
                print(self.fashion_api)
                print(params)
                print("Failed to get web page json")

def run():
    tc.log_path = "../" + tc.log_path
    sets = Pipeline(tc.site_id, tc.site_name).structure_set()
    Pipeline(tc.site_id, tc.site_name).open_spider(sets)
    for item in Sina().api_requests():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)
    for item in Sina().culture_req():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)
    for item in Sina().fashion_req():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)

    try:
        Pipeline(tc.site_id, tc.site_name).close_spider()
    except:
        Logger().setLogger(tc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
