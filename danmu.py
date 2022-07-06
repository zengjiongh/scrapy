import csv
import json
import ast
import requests
import re
import time
from multiprocessing.dummy import Pool
import os
from fake_useragent import UserAgent

au = UserAgent


proxies = {
    "http":"http://112.195.120.57:8080"
}
headers = {
    "User-Agent": au.random,
    "Cookie":"RK=q9pB6cvfU7; ptcz=67fae2b0cfa5bed0b2e9ab686552b462d127fa38348011a71a8a107cc0348062; pgv_pvid=177465968; _ga=GA1.2.1830253812.1616927238; tvfe_boss_uuid=c931edf2f7be4922; video_guid=57cd81146f9dc506; video_platform=2; eas_sid=u1s6W225F6x721s3d2I9q3V2f9; pac_uid=0_a9b1c6b7e2159; _video_qq_login_time_init=1633077187; o_cookie=1981756870; pgv_info=ssid=s8402550408; video_omgid=57cd81146f9dc506; vversion_name=8.2.95"
}
def get_danmu_list(url):
    timestamp = 15
    danmu_list = []
    while True:
        time.sleep(1)
        try:
            url1 = url[1:]
            url2 = url1+"&timestamp={}".format(timestamp)
            response = requests.get(url = url2,headers = headers,proxies=proxies)
            html = response.text
            content = json.loads(html)
            count = content.get("count")
            if count == 0:
                break
            else:
                timestamp += 30
            comments = content.get("comments")
            l = 0
            for i in range(len(comments)):
                dict = {}
                dict["id"] = comments[i].get("commentid")
                dict["用户名"] = comments[i].get("opername")
                dict["弹幕内容"] = comments[i].get("content")
                dict["vip等级"] = comments[i].get("uservip_degree")
                danmu_list.append(dict)
            print(danmu_list,len(danmu_list))
        except:
            print("这集完了")
            break
    return danmu_list

def get_first_id():
    url1 = "https://v.qq.com/x/cover/m441e3rjq9kwpsc/m00253deqqo.html"
    response = requests.get(url=url1,headers=headers,proxies=proxies)
    html = response.text
    frist_id = re.findall('"nomal_ids":(.*?),"payfree_num"',html,re.S)[0]
    frist_id_t = ast.literal_eval(frist_id)
    id_list = []
    for i in frist_id_t:
        id_list.append(i["V"])
    print(id_list,len(id_list))
    return id_list

def get_finally_id(id_list):
    url2 = "https://access.video.qq.com/danmu_manage/regist?vappid=97767206&vsecret=c0bdcbae120669fff425d0ef853674614aa659c605a613a4&raw=1"
    targetid_list = []
    for nums,vaule in enumerate(id_list):
        time.sleep(0.2)
        data = {
            "wRegistType": 2,
            "vecIdList": [vaule],
            "wSpeSource": 0,
            "bIsGetUserCfg": 1,
            "mapExtData": {vaule:
                               {"strCid": "m441e3rjq9kwpsc", "strLid": ""}
            }}
        response = requests.post(url=url2,headers=headers,json=data,proxies=proxies)
        html3 = response.text
        content = json.loads(html3)
        targetid = content.get("data").get("stMap").get(vaule).get("strDanMuKey")
        targetid_t = re.findall("targetid=(.*?)&",targetid,re.S)
        targetid_list.append(targetid_t)
        print(targetid_t)
    return targetid_list

def get_url(targetid_list,id_list):
    id_list_t = []
    for nums,id in enumerate(targetid_list):
        id1 = id[0]
        id_t = '"https://mfm.video.qq.com/danmu?target_id=' + id1 +"%26vid%3D"+ id_list[nums]
        id_list_t.append(id_t)
        print(id_list_t)
    return id_list_t

def run():
    id_list = get_first_id()
    targetid_list = get_finally_id(id_list)
    url = get_url(targetid_list,id_list)

    # danmu_list = []
    # l = 0
    # for id ,url_id in enumerate(url):
    #     danmu = get_danmu_list(url_id)
    #     danmu_list.append(danmu)
    #     l += len(danmu)
    #     save(danmu,id)
    #     print(danmu,len(danmu),l)
    # return danmu_list

    pool = Pool(30)
    danmu_list = pool.map(get_danmu_list,url)
    return danmu_list

def save():
    danmu_list = run()
    for i,val in enumerate(danmu_list):
        os.makedirs("斗罗大陆弹幕",exist_ok=True)
        with open(os.path.join("斗罗大陆弹幕","第{}集弹幕".format(i+1)+'.csv'),'w',encoding='GB18030') as f:
            witer = csv.DictWriter(f,fieldnames=["id","用户名","弹幕内容","vip等级"])
            witer.writeheader()
            witer.writerows(val)
            print(f"第{i+1}集弹幕保存完了")

if __name__ == '__main__':
    save()



