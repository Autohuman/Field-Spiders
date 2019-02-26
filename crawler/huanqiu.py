#coding:utf-8
import sys
sys.path.append("..")
from config import XinHuaConfig as tc
from logger import Logger
from pipelines import Pipeline

from func import Req
from lxml import etree

class Huanqiu(object):
    keys = []
    milite = {
        'head': 'mil',
        'contains': ['world', 'strategysituation', 'aerospace', 'milmovie', 'gt'],
        'field': 3
    }
    keys.append(milite)
    tech = {
        'head': 'tech',
        'contains': ['discovery', 'Enterprise', 'special', 'foreign_report', 'net', 'digi', 'business', 'science', 'aerospace', 'comm', 'it', 'internet', 'fantasy', 'globalgeek', 'per', 'front'],
        'field': 5
    }
    keys.append(tech)
    smart = {
        'head': 'smart',
        'contains': ['encounter', 'viewpoint', 'photo', 'prospect', 'video', 'roll', 'ai', 'vr', 'travel', 'iot', 'city'],
        'field': 5
    }
    keys.append(smart)
    sports = {
        'head': 'sports',
        'contains': ['basketball/cba', 'basketball/nba', 'soccer/gn', 'soccer/xj', 'soccer/yc', 'soccer/yj', 'others/zh', 'review/bj'],
        'field': 2
    }
    keys.append(sports)
    game = {
        'head': 'tech',
        'contains': ['game'],
        'field': 10
    }
    keys.append(game)
    finance = {
        'head': 'finance',
        'contains': ['financepic', 'hqsl', 'xinsanb', 'shangh', 'nengy', 'quyuy', 'xiaofeil', 'chuangr', 'baoxianl', 'gjcx', 'ssgs', 'jijinx', 'zhengq', 'lingdu', 'jinr', 'caigc', 'chanjing', 'roll'],
        'field': 4
    }
    keys.append(finance)
    art = {
        'head': 'art',
        'contains': ['news', 'calligraphyandpainting', 'master', 'collection', 'video', 'artandcraft', 'exhibition', 'auction', 'comment'],
        'field': [35, 5]
    }
    keys.append(art)
    quality = {
        'head': 'quality',
        'contains': ['policy', 'brand', 'businessman', 'expert', 'international', 'exposure', 'automobile', 'property', 'intelligent', 'momkids', 'foods', 'home', 'medicine', 'traveling', 'outdoors', 'beauty', 'dress', 'fmcg'],
        'field': 14
    }
    keys.append(quality)
    world = {
        'head': 'world',
        'contains': ['article', 'weinxingonghao', 'regions', 'exclusive', 'photo'],
        'field': 11
    }
    keys.append(world)
    society = {
        'head': 'society',
        'contains': ['article', 'anecdotes', 'socialnews', 'photonew','societylaw'],
        'field': 39
    }
    keys.append(society)
    city = {
        'head': 'city',
        'contains': ['travel'],
        'field': [8, 28]
    }
    keys.append(city)
    culture = {
        'head': 'cul',
        'contains': ['zixun', 'music', 'video'],
        'field': 8
    }
    keys.append(culture)
    book = {
        'head': 'cul',
        'contains': ['wenxue'],
        'field': [8, 31]
    }
    keys.append(book)
    lvyou = {
        'head': 'go',
        'contains': ['news/tour', 'news/hotel', 'news/airline', 'news/tourism', 'news/qyly', 'news/csgm', 'news/lyfp'],
        'field': 28
    }
    keys.append(lvyou)


    def get_page(self):
        for y in self.keys:
            for x in y['contains']:
                for page in range(30):
                    if page == 0:
                        url = 'http://'+y['head']+'.huanqiu.com/'+ x +'/'
                    else:
                        url = 'http://mil.huanqiu.com/'+ x +'/'+ str(page+1) +'.html'
                    try:
                        response = Req(url).get_select()
                        selector = etree.HTML(response.content)
                        data = selector.xpath('//ul[@class="listPicBox"]/li[@class="item"]')
                        for i in data:
                            item = dict()
                            item['title'] = i.xpath('h3/a/text()')[0]
                            item['link'] = i.xpath('h3/a/@href')[0]
                            item['datetime'] = i.xpath('h6/text()')[0]
                            item['field'] = y['field']
                            item['status'] = False
                            item['home'] = False
                            yield item
                    except:
                        print(url)
                        print("LaLaLa")

    def get_list(self):
        url = 'http://ent.huanqiu.com/'
        try:
            response = Req(url).get_select()
            selector = etree.HTML(response.content)
            data = selector.xpath('//div[@class="leftList"]/ul/li[@name="item"]')
            for i in data:
                item = dict()
                item['title'] = i.xpath('a/dl/dt/h3/text()')[0]
                item['link'] = i.xpath('a/@href')[0]
                item['field'] = 1
                item['status'] = False
                item['home'] = False
                yield item
        except:
            print(url)
            print("LaLaLa")



def run():
    tc.log_path = "../" + tc.log_path
    sets = Pipeline(tc.site_id, tc.site_name).structure_set()
    Pipeline(tc.site_id, tc.site_name).open_spider(sets)
    for item in Huanqiu().get_page():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)

    for item in Huanqiu().get_list():
        Pipeline(tc.site_id, tc.site_name, item['field']).process_item(item)
        Pipeline(tc.site_id, tc.site_name, item['field']).upload_item(item, sets)

    try:
        Pipeline(tc.site_id, tc.site_name).close_spider()
    except:
        Logger().setLogger(tc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()