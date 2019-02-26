import requests
import re
from lxml import etree
import json

response = requests.get('http://mp.weixin.qq.com/profile?src=3&timestamp=1548326010&ver=1&signature=v-HOIkkRdfsi8AUIc9ZRKsb3GBQ2m71AEEtZeL2rJcBJrRBCx8UyRRD7iCwtFqyZ3piXoF0A98kymQ91mChGOA==')
selector = etree.HTML(response.content)
part = selector.xpath('/html/body/script[8]/text()')[0]

pattren = re.compile(r'.*?var name="(.*?)";.*?var msgList = ({"list":\[.*?\]});.*?',re.S)
m = re.match(pattren, part)
name = m.groups()[0]
msg_list = m.groups()[1]
# print(msg_list)1
msg_list = json.loads(msg_list)
now = msg_list['list']
for i in now:
    print(i)
    # if 'title' in i['app_msg_ext_info'].keys():
    #     item['title'] = i['app_msg_ext_info']['title']
    #     item['url'] = i['app_msg_ext_info']['content_url']

