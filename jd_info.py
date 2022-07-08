import csv

import requests
import json
from lxml import etree
import re
import time
import os
from multiprocessing import Pool
from fake_useragent import UserAgent
import pymysql
import random

con = pymysql.Connect(host="127.0.0.1", port=3306, user="root", password="zjr", db='ZJR', charset='utf8')

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
# print(https_ip_list)
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'cookie': 'shshshfpa=f9f300d1-106b-2f1b-ed5a-4b3b34e972c8-1636251432; shshshfpb=xdNLUP6VOlbdDKJE9e5MaJA%3D%3D; areaId=0; __jdu=1636251432262541638300; qrsc=3; pinId=n4OlR52jvHJ1kED2e-l_jLV9-x-f3wj7; pin=jd_49fe4088ace97; unick=jd_49fe4088ace97; _tp=HMYGyo58KaPYBsv58H4BqUUe%2F0PRX2buD4sG170RhUQ%3D; _pst=jd_49fe4088ace97; ipLoc-djd=1-72-55653-0; user-key=97568692-c140-4c2e-b081-f7ff054d7280; mt_xid=V2_52007VwMVUFpbVloaSxpfAmQHF1JaWltYHkgpXA1uURVaDV9OXB1AS0AAMAJGTg4PVA0DQRwLBGFUQVoJXlsPL0oYXwV7AxJOXVtDWhpCGFsOZAMiUG1YYl8ZTRFVBmEKE1JtXVNTGQ%3D%3D; unpl=V2_ZzNtbRBVQRAnWE9QKUxcUGIFQg1LUktCcwARU39OWwwyChINclRCFnUURlRnGVgUZwoZWUFcQhFFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHseXgJkBxJYQFRAEnYMQ1R8G1UHZgIibUVncyVzCUZXeyldNWYzUAkeUUIcdwBGGXseXgJkBxJYQFRAEnYMQ1R8G1UHZgIiXHJU; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_c334ca85cd1d47aa849f79f65f68d81a|1636973564993; PCSYCityID=CN_0_0_0; __jda=122270672.1636251432262541638300.1636251432.1636709185.1636973565.17; __jdc=122270672; shshshfp=84a46e76ff87fb0199eb2856cd699464; rkv=1.0; wlfstk_smdl=aml3jvyxhphm62lzt86iw4b56v51rmv2; TrackID=1xZG1IC1KFdHtPQQgPVY__TM3SS4ClPEUxxvE5vmlEIqhZKmjCPR3j2Th_faj43WHMRzWeXhPIpEc74GhVCjZjTrB17qwa1NlU8ejpzVJ11Y; thor=0F4BB709E13D4A49811F12E9BA7902C53F6E8041EEA43F26C34B6B2D3615505A4124D50791F8DCAC01EDCDF289AD4052B5794DEC13A12682FF4974C3313A662F0A88B09F6397D0E0AC12336E512CD8D27418BA18E93BB395EDA1EDAA85E24A4A7757581F7372C8AE990C3C305A4137F93A7827726A939B95E7F2CF62F5B7841D34C450C02369CA82BDABEF7FB3DDF67B268CCA75782C4B5B69380AD9AED0F7DE; ceshi3.com=000; __jdb=122270672.5.1636251432262541638300|17.1636973565; shshshsID=27978fe5a2944839d8679aed5036fceb_3_1636973616852; 3AB9D23F7A4B3C9B=JL2O6STR2EZO7RCYFDWNEOROT7M47E6CBAAVHPPDZVUYTKTRYEYT2CWIQLYXUDEFLH3BCBW7YSCIRDK35RQCA4Z65A'
}
ip_info = []
all_info = []


def get_url():
    page = 0
    url_ip_list = []
    while True:
        try:
            url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&pvid=99b7bb5bfe5f4009aad578e24e466c50&page={}".format(
                page)
            session = requests.session()
            response = session.get(url=url, headers=headers, proxies=random.choice(https_ip_list))
            content = response.text
            html = etree.HTML(content)
            price = html.xpath("//*[@id='J_goodsList']/ul/li/div/div[3]/strong/i//text()")
            http = html.xpath("//*[@id='J_goodsList']/ul/li/div/div[1]/a/@href")
            lis = []
            if price == lis:
                break
            else:
                page += 1
            for value in http:
                url = "https:" + value
                url_ip_list.append(url)
        except:
            print("已经没有了")
            break
        print(url_ip_list, len(url_ip_list), page)
    return url_ip_list


def get_info(url):
    time.sleep(1)
    session = requests.session()
    response = session.get(url=url, headers=headers, proxies=random.choice(https_ip_list))
    content = response.text
    html = etree.HTML(content)
    try:
        pro_name = re.findall("商品名称：(.*?)<", content, re.S)[0]
    except:
        pro_name = "网卡了"

    color = html.xpath("//*[@id='choose-attr-1']/div[2]/div/a/img/@alt")

    size = html.xpath("//*[@id='choose-attr-2']/div[2]/div/@title")
    # list_c = []
    # for i in size:
    #     size1 = i.replace("\n", "").replace(" ", "")
    #     list_c.append(size1)
    try:
        year = re.findall("<dt>上市年份</dt><dd>(.*?)</dd>", content, re.S)[0]
    except:
        year = "暂时没有消息"
    try:
        mouth = re.findall("<dt>上市月份</dt><dd>(.*?)<", content, re.S)[0]
    except:
        mouth = "暂时没有消息"

    id = re.findall("https://item.jd.com/(.*?).html", url, re.S)[0]
    url1 = "https://club.jd.com/comment/productPageComments.action?&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1".format(
        id)
    session1 = requests.session()
    html1 = session1.get(url=url1, headers=headers, proxies=random.choice(https_ip_list))
    html1 = html1.text
    try:
        content = json.loads(html1)
        Praise_rate = str(content.get("productCommentSummary").get("goodRateShow")) + "%"
    except:
        try:
            time.sleep(1)
            content = json.loads(html1)
            Praise_rate = str(content.get("productCommentSummary").get("goodRateShow")) + "%"
        except:
            Praise_rate = "暂时不能显示"
    url2 = "https://p.3.cn/prices/mgets?type=1&area=1_72_55653_0&pdtk=&pduid=1636251432262541638300&pdpin=jd_49fe4088ace97&pin=jd_49fe4088ace97&pdbp=0&skuIds={}".format(
        id)
    session2 = requests.session()
    html2 = session2.get(url=url2, headers=headers, proxies=random.choice(https_ip_list)).text
    try:
        html2 = json.loads(html2)[0]
        price = html2.get("p")
    except:
        price = "暂时不能显示"
    lianjie = "https://item.jd.com/" + id + ".html"
    dic = {}
    dic["手机名称"] = pro_name
    dic["上市年份"] = year
    dic["上市月份"] = mouth
    dic["手机颜色"] = color
    dic["手机配置内存"] = size
    dic["价格"] = price
    dic["好评率"] = str(Praise_rate)
    dic["链接"] = lianjie
    print(dic)
    return dic


def all_info_ip(url_ip_list):
    pool = Pool(30)
    info = pool.map(get_info, url_ip_list)
    return info
    # info_list = []
    # for i,value in enumerate(url_ip_list):
    #     time.sleep(0.3)
    #     list1 = []
    #     info = get_info(value)
    #     list1.append(info)
    # with open(os.path.join("京东手机信息" + ".csv"), "a+", encoding="GB18030") as f:
    #     witer = csv.DictWriter(f, fieldnames=["手机名称", "上市年份", "上市月份", "手机颜色", "手机配置内存", "价格", "好评率", "链接"])
    #     witer.writeheader()
    #     witer.writerows(list1)
    #     info_list.append(info)
    #     print(info_list,len(info_list))
    # return info_list


def run():
    url_ip_list = get_url()
    all_info = all_info_ip(url_ip_list)
    print(all_info, len(all_info))
    return all_info


def save():
    all_info = run()
    with open(os.path.join("京东手机信息" + ".csv"), "w", newline="", encoding="GB18030") as f:
        witer = csv.DictWriter(f, fieldnames=["手机名称", "上市年份", "上市月份", "手机颜色", "手机配置内存", "价格", "好评率", "链接"])
        witer.writeheader()
        witer.writerows(all_info)


if __name__ == '__main__':
    save()
