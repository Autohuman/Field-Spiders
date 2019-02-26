#coding:utf-8
import sys
sys.path.append("..")
from config import iFengConfig as tc
from logger import Logger
from pipelines import Pipeline

from func import Req
from datetime import datetime
import json


class iFeng(object):
    url = 'https://api.iclient.ifeng.com/nlist'
    params = {
        'id': 'CJ33,FOCUSCJ33,HNCJ33',
        'action': 'up',
        'pullNum': '3',
        'gv': '6.3.9',
        'av': '6.3.9',
        'uid': '11223344',
        'deviceid': '11223344',
        'proid': 'ifengnews',
        'os': 'android_17',
        'df': 'androidphone',
        'vt': '5',
        'screen': '1200x1824',
        'publishid': '2856',
        'nw': 'wifi',
        'loginid': None,
        'st': '1550998587',
        'sn': '3d9159e112c6d63d3a5f46fa983557c2'
    }
    LIS = list()
    finance = {
        'id': 'CJ33,FOCUSCJ33,HNCJ33',
        'field': 4
    }
    LIS.append(finance)
    ent = {
        'id': 'YL53,FOCUSYL53,SECNAVYL53',
        'field': 1
    }
    LIS.append(ent)
    mili = {
        'id': 'JS83,FOCUSJS83',
        'field': 3
    }
    LIS.append(mili)
    tech = {
        'id': 'KJ123,FOCUSKJ123,SECNAVKJ123',
        'field': 5
    }
    LIS.append(tech)
    sports = {
        'id': 'TY43,FOCUSTY43,TYTOPIC',
        'field': 2
    }
    LIS.append(sports)
    world = {
        'id': 'GJPD,FOCUSGJPD',
        'field': 11
    }
    LIS.append(world)
    lvyou = {
        'id': 'LY67,FOCUSLY67,SECNAVLY67',
        'field': 28
    }
    LIS.append(lvyou)
    fashion = {
        'id': 'SS78,FOCUSSS78,SECNAVSS78',
        'field': 6
    }
    LIS.append(fashion)
    history = {
        'id': 'LS153,FOCUSLS153',
        'field': 30
    }
    LIS.append(history)
    cul = {
        'id': 'WH25,FOCUSWH25',
        'field': 8
    }
    LIS.append(cul)
    game = {
        'id': 'YX11,FOCUSYX11',
        'field': 10
    }
    LIS.append(game)


    def api_get(self):
        for u in self.LIS:
            self.params['id'] = u['id']

            sets = set()
            for m in range(1, 70):
                self.params['os'] = 'android_' + str(m)
                for pullNum in range(1, 10):
                    self.params['pullNum'] = pullNum

                    try:
                        response = Req(url=self.url, params=self.params).get_select()
                        data = json.loads(response.content.decode('utf8'))
                        less = list()
                        for x in data:
                            for y in x['item']:
                                less.append(y)
                        for x in less:
                            if 'adId' not in x.keys():
                                try:
                                    item = dict()
                                    item['title'] = x['title']
                                    item['link'] = x['link']['weburl']

                                    try:
                                        item['datetime'] = datetime.strptime(x['updateTime'],
                                                                             "%Y/%m/%d %H:%M:%S").strftime(
                                            "%Y-%m-%d %H:%M:%S")
                                    except:
                                        item['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                    item['field'] = u['field']

                                    if item['title'] not in sets:
                                        sets.add(item['title'])
                                        yield item
                                    else:
                                        pass
                                except:
                                    pass
                    except:
                        Logger().setLogger(tc.log_path, 4, "Failed to request, url is" + str(self.params))
                        pass

def run():
    tc.log_path = "../" + tc.log_path
    sets = Pipeline(tc.site_id, tc.site_name).structure_set()
    Pipeline(tc.site_id, tc.site_name).open_spider(sets)
    for item in iFeng().api_get():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)

    try:
        Pipeline(tc.site_id, tc.site_name).close_spider()
    except:
        Logger().setLogger(tc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
