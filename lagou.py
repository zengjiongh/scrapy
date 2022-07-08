import random

import requests
from lxml import etree
from multiprocessing.dummy import Pool
import re
import os
import csv
import time
import pymysql
from fake_useragent import UserAgent
con = pymysql.Connect(host = "127.0.0.1",port=3306,user="root",password="zjr",db='ZJR',charset='utf8')

ua = UserAgent()
cos = con.cursor()
try:
    cos.execute("""select * from ip;""")
    all = cos.fetchall()
    con.commit()
except:
    con.rollback()
cos.close()
con.close()
# print(all)
http_ip_list = []
https_ip_list = []
ip_list = []

for i in all:
    if "http" in i:
        dic_http = {}
        http_ip = i[1] + "://" + i[2] + ":" + i[3]
        dic_http["http"] = http_ip
        http_ip_list.append(dic_http)
        ip_list.append(dic_http)

    else:
        dic_https = {}
        https_ip = i[1] + "://" + i[2] + ":" + i[3]
        dic_https["htpps"] = https_ip
        https_ip_list.append(dic_https)
        ip_list.append(dic_https)
url = 'https://www.lagou.com/'
headers = {
    'user-agent': ua.random,
    'cookie': 'RECOMMEND_TIP=true; user_trace_token=20211115215926-1387e870-785b-49ea-8cde-a96f5c9c9f16; LGUID=20211115215926-ef7ab9bb-8b3b-4d0e-a79e-b7ee1128a035; _ga=GA1.2.1622339288.1636984770; LG_HAS_LOGIN=1; JSESSIONID=ABAAABAABAGABFABC8555CD684A2800DEDDF58A582589BE; WEBTJ-ID=20220526184319-180fff6b4564f7-036c9ac9659342-14333270-1327104-180fff6b459b8c; PRE_UTM=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1653561801; privacyPolicyPopup=false; _gid=GA1.2.715954214.1653561801; _gat=1; sensorsdata2015session=%7B%7D; LGSID=20220526184320-3923b48f-d2d2-4810-922a-d30f05e0f175; PRE_HOST=www.google.com.hk; PRE_SITE=https%3A%2F%2Fwww.google.com.hk%2F; sm_auth_id=a0n0d1qo1npif2bf; gate_login_token=eb8232277d605eac3891111a81b9a03d3f948d20113612b757f89072ecaae887; _putrc=342257C297CFEF01123F89F2B170EADC; login=true; unick=%E6%9B%BE%E7%BB%A7%E6%A6%95; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=3; index_location_city=%E6%88%90%E9%83%BD; X_HTTP_TOKEN=b21f6488231e763b648165356184a2f228d93452d0; __SAFETY_CLOSE_TIME__21854315=1; LGRID=20220526184406-b62b8704-61c7-4757-b8f2-9bd9150cf568; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1653561847; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2221854315%22%2C%22first_id%22%3A%2217d23e54d80c49-0e7f3cc894a9d9-57b1a33-1327104-17d23e54d81d16%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%22101.0.4951.67%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217d23e54d80c49-0e7f3cc894a9d9-57b1a33-1327104-17d23e54d81d16%22%7D'
}
with open("D:/文本数据挖掘/文本挖掘数据及自学代码/期末实训/上海堡垒/ip.txt", "r", encoding="utf-8") as f:
    ip_list = ['http://' + line.strip() for line in f.readlines()]
proxy = random.choice(ip_list)
print(proxy)
proxies = {
    'http': 'http://' + proxy
}
response = requests.get(url,headers=headers,proxies=proxies)
# print(response)
content = response.text
# print(content)
html = etree.HTML(content)
http = html.xpath("//div[@class='menu_main job_hopping']/div/a/@href")
# print(http)
name = html.xpath("//div[@class = 'category-list']/a/h3//text()")
# print(name)
def rec_info(url):
    url = url
    with open("D:/文本数据挖掘/文本挖掘数据及自学代码/期末实训/上海堡垒/ip.txt", "r", encoding="utf-8") as f:
        ip_list = ['http://' + line.strip() for line in f.readlines()]
    proxy = random.choice(ip_list)
    print(proxy)
    proxies = {
        'http': 'http://' + proxy
    }
    #         response = requests.get(url=url,headers = headers,proxies=proxies)
    response = requests.get(url=url, headers=headers, proxies=proxies).text
    # response = requests.get(url,headers = headers,proxies=random.choice(https_ip_list)).text
    html1 = etree.HTML(response)
    position = html1.xpath("//div[@class='position']/div[1]/a/h3//text()")
    company = html1.xpath("//div[@class='company_name']/a/text()")
    wages = html1.xpath("//div[@class='p_bot']/div/span/text()")
    exper_degree = re.findall("<!--<i></i>-->(.*?) ", response, re.S)
    inf_list = []
    for i in range(len(position)):
        info = {}
        info['职位'] = position[i]
        info['薪资'] = wages[i]
        info['经验/学历'] = exper_degree[i]
        info['公司'] = company[i]
        inf_list.append(info)
    return inf_list
pool = Pool(10)
infom = pool.map(rec_info,http)
print(infom)
for values,info in enumerate(infom):
    with open(os.path.join(name[values]+'.csv'),'w',encoding='utf-8') as f:
        witer = csv.DictWriter(f, fieldnames=['职位', '薪资', '经验/学历', '公司'])
        # print(name[values])
        witer.writeheader()
        witer.writerows(info)
        time.sleep(10)




