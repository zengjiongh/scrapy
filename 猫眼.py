import requests
import json
import os
import csv


def html():
    url = 'https://piaofang.maoyan.com/dashboard-ajax?orderType=0&uuid=180febf91d0c8-0aa11a58568e7e-14333270-144000-180febf91d0c8&timeStamp=1656749496477&User-Agent=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMy4wLjAuMCBTYWZhcmkvNTM3LjM2&index=698&channelId=40009&sVersion=2&signKey=4c4a8ed44256c0ddbdf3c8d933328382'
    headers = {
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
        'Cookie': "xxx",
    }
    # 'Cookie': '_lxsdk_cuid=17c182bb097c8-0d0be42dcbd786-b7a1a38-e1000-17c182bb098c8; _lxsdk=17c182bb097c8-0d0be42dcbd786-b7a1a38-e1000-17c182bb098c8; _lxsdk_s=17cdfaf225a-c41-74e-934^%^7C^%^7C1; __mta=248413496.1632493094258.1632558998979.1635840369399.8',
    content = requests.get(url, headers=headers).text
    content = json.loads(content)
    # content = ast.literal_eval(content)
    return content


def tvlist(content):
    tv_list = []
    tv_info = content.get('tvList').get('data').get('list')
    for info in range(len(tv_info)):
        tv_dict = {}
        tv_dict["平台"] = tv_info[info].get('channelName')
        tv_dict["剧情"] = tv_info[info].get('programmeName')
        tv_dict['关注率'] = tv_info[info].get('attentionRateDesc')
        tv_list.append(tv_dict)
    return tv_list


def web(content):
    web_list = []
    web_info = content.get('webList').get('data').get('list')
    for info in range(len(web_info)):
        web_dict = {}
        web_dict['名字'] = web_info[info].get('seriesInfo').get('name')
        web_dict['平台'] = web_info[info].get('seriesInfo').get('platformDesc')
        web_dict['实时热度'] = web_info[info].get('currHeatDesc')
        web_list.append(web_dict)
    return web_list


def movie(content):
    movie_list = []
    all_info = content.get('movieList').get('data').get('list')
    for info in range(len(all_info)):
        info = all_info[info].get('movieInfo')
        movie_list.append(info)
    return movie_list


def save(info, name, name1, name2, name3):
    os.makedirs('排行榜', exist_ok=True)
    with open(os.path.join('排行榜', name + '.csv'), 'w', newline="", encoding='utf-8') as f:
        witer = csv.DictWriter(f, fieldnames=[name1, name2, name3])
        witer.writeheader()
        witer.writerows(info)


def run():
    movie1 = movie(html())
    save(movie1, '电影', "movieId", 'movieName', 'releaseInfo')
    web1 = web(html())
    save(web1, '网剧', '名字', '平台', '实时热度')
    tv = tvlist(html())
    save(tv, '电视', '平台', '剧情', '关注率')


if __name__ == '__main__':
    run()
