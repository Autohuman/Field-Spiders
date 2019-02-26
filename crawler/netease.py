#coding:utf-8
import sys
sys.path.append("..")
from config import NeteaseConfig as nt
from logger import Logger
from pipelines import Pipeline

from func import Req
import json
from datetime import datetime

class Netease(object):
    LIS = list()
    ent  = {
        'link': 'ent.163.com',
        'code': '000380VU',
        'type': 'newsdata_index',
        'field': 1
    }
    LIS.append(ent)
    sports = {
        'link': 'sports.163.com',
        'code': '000587PR',
        'type': 'newsdata_n_index',
        'field': 2
    }
    LIS.append(sports)
    milite = {
        'link': 'temp.163.com',
        'code': '00804KVA',
        'type': 'cm_war',
        'field': 3
    }
    LIS.append(milite)
    finance = {
        'link': 'money.163.com',
        'code': '00259BVP',
        'type': 'news_flow_index',
        'field': 4
    }
    LIS.append(finance)
    tech = {
        'link': 'tech.163.com',
        'code': '00097UHL',
        'type': 'tech_datalist',
        'field': 5
    }
    LIS.append(tech)
    fashion = {
        'link': 'temp.163.com',
        'code': '002688FE',
        'type': 'fashion_datalist',
        'field': 6
    }
    LIS.append(fashion)
    edu = {
        'link': 'edu.163.com',
        'code': '002987KB',
        'type': 'newsdata_edu_hot',
        'field': 12
    }
    LIS.append(edu)
    art = {
        'link': 'art.163.com',
        'code': '00999815',
        'type': 'art_redian_api',
        'field': 35
    }
    LIS.append(art)
    politics = {
        'link': 'temp.163.com',
        'code': '00804KVA',
        'type': 'cm_guonei',
        'field': 9
    }
    LIS.append(politics)

    def net_api(self, m, link, code, type, field):
        for x in range(1, m):
            if x == 1:
                url = 'http://' + link + '/special/'+ code + '/' + type + '.js?callback=data_callback'
            elif x <= 9:
                x = '_0' + str(x)
                url = 'http://' + link + '/special/'+ code + '/' + type + x +'.js?callback=data_callback'
            else:
                x = '_' + str(x)
                url = 'http://' + link + '/special/'+ code + '/' + type + str(x) +'.js?callback=data_callback'

            response = Req(url).get_select()
            if response.status_code == 404:
                print(response.url)
                print('！！！！！')
            else:
                data = json.loads(response.content[14:-1].decode('gbk'))
                for i in data:
                    item = dict()
                    item['title'] = i['title']
                    item['link'] = i['docurl']
                    item['datetime'] = i['time']
                    try:
                        item['datetime'] = datetime.strptime(item['datetime'], '%m/%d/%Y %H:%M:%S')
                        item['datetime'] = item['datetime'].strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        pass
                    item['field'] = field
                    item['status'] = False
                    item['home'] = False
                    yield item


def run():
    nt.log_path = "../" + nt.log_path
    sets = Pipeline(nt.site_id, nt.site_name).structure_set()
    Pipeline(nt.site_id, nt.site_name).open_spider(sets)
    for i in Netease().LIS:
        for item in Netease().net_api(50, i['link'], i['code'], i['type'], i['field']):
            Pipeline(nt.site_id, nt.site_name, item['field']).process_item(item)
            Pipeline(nt.site_id, nt.site_name, item['field']).upload_item(item, sets)
    try:
        Pipeline(nt.site_id, nt.site_name).close_spider()
    except:
        Logger().setLogger(nt.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()