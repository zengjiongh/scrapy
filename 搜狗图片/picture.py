import requests
import json
import os
import time

headers={
    'Connection': 'keep-alive',
    'sec-ch-ua': '^\\^Google',
    'Accept': 'application/json, text/plain, */*',
    'X-FOR-WITH': '8GjzdiNjLeukNDUsK++bX2Zau0iMbzb+ANoiqfRAKpMlXy2kBwXteEDBVayhCZw46TzNK67545RTBuxT2PA7FIJUNI6O37X1YKoM9FUfeZQ6ZuT46iRgWBSYApwe/tKt51maXTfwA/bOespNF6BYCtLelitWB8h4uc0YuvoYXB3Bfyj63zTWPo9SZwJKqIPDNDjoti+e35YTxuVay4j6ag==',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'sec-ch-ua-platform': '^\\^Windows^^',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://piaofang.maoyan.com/dashboard',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'SUV=1615035047992594; SMYUV=1615035047993479; SUID=241A54B41431A40A00000000608A1473; usid=051A54B4E33D990A00000000608A1476; IPLOC=CN5301; FUV=9bcb9e077d9ac176e1d0ac8f7258e0f1; SNUID=7251FA2053519C94F363C1A454B01483; search_tip=1635831295131; ABTEST=0^|1635835919^|v1',
}
def get_name():
    name = input("请输入你想搜索的图片:")
    return name


def get_jpg_list(name):
    jpg_list = []
    start = 0
    while True:
        try:
            url1 = "https://pic.sogou.com/napi/pc/searchList?mode=1&start={}&xml_len=48&query={}".format(start,name)
            response = requests.get(url=url1,headers=headers)
            content  =response.text
            dict = json.loads(content)
            if dict["info"] == "empty":
                break
            else:
                start += 48
            jpg = dict.get("data").get("items")
            for i in jpg:
                http = i['locImageLink']
                jpg_list.append(http)
            print(jpg_list,len(jpg_list))
        except:
            print("保存完了")
    return jpg_list

def save(jpg_list,name):
    os.makedirs(f"{name}",exist_ok=True)
    for i ,value in enumerate(jpg_list):
        page = requests.get(value)
        with open(os.path.join(f"{name}","第{}张".format(i+1)+'.jpg'),"wb") as f:
            f.write(page.content)


def run():
    name = get_name()
    jpg_list = get_jpg_list(name)
    save(jpg_list,name)



if __name__ == '__main__':
    run()



