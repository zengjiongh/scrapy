import requests
from lxml import etree
import redis
import os
from multiprocessing.dummy import Pool

url = 'http://book.sbkk8.com/waiguo/dongyeguiwu/baiyexing/'
cookies = {
    'BAIDU_SSP_lcr': 'https://www.baidu.com/link?url=6orEan5TAWCfeHEvEkZRvDjtp3x9JNxmlRsHSZCbObcF7EANAKVLK_yQMNlrhv2qfstl3mlWx0egr1AjVSSKf_&wd=&eqid=a566d8710002a87d0000000261501c3d',
    'Hm_lvt_6364f0945f0ae7d2c71e1de11b20c0d5': '1632640070',
    '__gads': 'ID=44bca754aa33207c-22d95a25eccb0088:T=1632640067:RT=1632640067:S=ALNI_MZN6o0De42uz1roqn_NkRjHYOX-6A',
    'Hm_lpvt_6364f0945f0ae7d2c71e1de11b20c0d5': '1632640145',
}
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://www.baidu.com/link?url=6orEan5TAWCfeHEvEkZRvDjtp3x9JNxmlRsHSZCbObcF7EANAKVLK_yQMNlrhv2qfstl3mlWx0egr1AjVSSKf_&wd=&eqid=a566d8710002a87d0000000261501c3d',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'If-None-Match': 'W/^\\^613804d4-378a^\\^',
    'If-Modified-Since': 'Wed, 08 Sep 2021 00:33:24 GMT',
}
response = requests.get(url, headers=headers, cookies=cookies, verify=False)
# print(response)
content = response.content.decode('gbk')
# print(content)
html = etree.HTML(content)
start_url = 'http://book.sbkk8.com'
http = html.xpath('//*[@id="left"]/div[2]/ul/li/a/@href')
http_true = []
for i in http:
    http_true1 = start_url + i
    http_true.append(http_true1)
# print(http_true)
https = redis.StrictRedis()
for http in http_true:
    https.lpush('https6',http)
contn = https.lrange('https6',0,500)
print(contn)
print(https.llen('https6'))

def html(url):
    url = url
    response = requests.get(url, headers=headers, cookies=cookies, verify=False)
    content = response.content.decode('gbk')
    html = etree.HTML(content)
    title = html.xpath('//*[@id="maincontent"]/h1/text()')
    art = html.xpath('//*[@id="content"]/p/text()')
    art = '\n'.join(art)
    return title,art

content1 = Pool(8)
artic = content1.map(html,http_true)
os.makedirs('白夜行',exist_ok=True)
# print(artic)
for i in artic:
    with open(os.path.join('白夜行',i[0][0]+'.txt'),'w',encoding='utf-8') as f:
        f.write(i[1])
