#coding:utf-8
import sys
sys.path.append("..")
from config import XinHuaConfig as xh
from logger import Logger
from pipelines import Pipeline


from func import Req
import json

class Xinhua(object):
    LIS = list()
    politics = {
        'nid': '113352',
        'field': 9
    }
    LIS.append(politics)
    china = {
        'nid': '11139635',
        'field': 3
    }
    LIS.append(china)
    world = {
        'nid': '11139636',
        'field': 3
    }
    LIS.append(world)
    ent1 = {
        'nid': '116713',
        'field': 1
    }
    ent2 = {
        'nid': '116716',
        'field': 1
    }
    ent3 = {
        'nid': '116727',
        'field': 1
    }
    ent4 = {
        'nid': '116714',
        'field': 1
    }
    ent5 = {
        'nid': '116715',
        'field': 1
    }
    ent6 = {
        'nid': '1118296',
        'field': 1
    }
    ent7 = {
        'nid': '116750',
        'field': 1
    }
    ent8 = {
        'nid': '118113',
        'field': 1
    }
    LIS.append(ent1)
    LIS.append(ent2)
    LIS.append(ent3)
    LIS.append(ent4)
    LIS.append(ent5)
    LIS.append(ent6)
    LIS.append(ent7)
    LIS.append(ent8)

    finance = {
        'nid': '11147664',
        'field': 4
    }
    LIS.append(finance)
    tech1 = {
        'nid': '11109303',
        'field': 5
    }
    tech2 = {
        'nid': '11109242',
        'field': 5
    }
    tech3 = {
        'nid': '11109297',
        'field': 5
    }
    tech4 = {
        'nid': '11109298',
        'field': 5
    }
    tech5 = {
        'nid': '11109299',
        'field': 5
    }
    tech6 = {
        'nid': '11109300',
        'field': 5
    }
    LIS.append(tech1)
    LIS.append(tech2)
    LIS.append(tech3)
    LIS.append(tech4)
    LIS.append(tech5)
    LIS.append(tech6)
    fashion = {
        'nid': '11110196',
        'field': 6
    }
    LIS.append(fashion)
    culture1 = {
        'nid': '11111478',
        'field': 8
    }
    culture2 = {
        'nid': '11111477',
        'field': 8
    }
    culture3 = {
        'nid': '11111482',
        'field': 8
    }
    culture4 = {
        'nid': '11111473',
        'field': 8
    }
    culture5 = {
        'nid': '11111483',
        'field': 8
    }
    culture6 = {
        'nid': '11111484',
        'field': 8
    }
    culture7 = {
        'nid': '11111489',
        'field': 8
    }
    LIS.append(culture1)
    LIS.append(culture2)
    LIS.append(culture3)
    LIS.append(culture4)
    LIS.append(culture5)
    LIS.append(culture6)
    LIS.append(culture7)

    def get_api(self, nid, field):
        url = 'http://qc.wa.news.cn/nodeart/list'
        params = {
            'nid': nid,
            'cnt': '20',     #cnt控制每次获取数量，页面默认为10
            'tp': '1',
            'orderby': '1'
        }
        for page in range(1, 50):
            params['pgnum'] = page
            response = Req(url=url, params=params).get_select()
            try:
                data = json.loads(response.content[1:-1])['data']['list']
                for i in data:
                    item = dict()
                    item['title'] = i['Title']
                    item['datetime'] = i['PubTime']
                    item['link'] = i['LinkUrl']
                    item['home'] = False
                    item['status'] = False
                    item['field'] = field
                    yield item
            except:
                print("Failed to get page, ,normal error, url is " + response.url)
                # Logger().setLogger(xh.log_path, 2, "Failed to get page, ,normal error, url is " + response.url)
                pass


def run():
    # xh.log_path = "../" + xh.log_path
    # sets = Pipeline(xh.site_id, xh.site_name).structure_set()
    # Pipeline(xh.site_id, xh.site_name).open_spider(sets)
    for i in Xinhua().LIS:
        for item in Xinhua().get_api(i['nid'], i['field']):
            print(item)
    #         Pipeline(xh.site_id, xh.site_name, item['field']).process_item(item)
    #         Pipeline(xh.site_id, xh.site_name, item['field']).upload_item(item, sets)
    # try:
    #     Pipeline(xh.site_id, xh.site_name).close_spider()
    # except:
    #     Logger().setLogger(xh.log_path, 4, "Failed to close spider,db_session may failed")
    #     pass

if __name__ == '__main__':
    run()