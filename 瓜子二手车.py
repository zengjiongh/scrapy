import requests
import json
import os
import csv

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}
page = 1
info_cars = []
while True:
    url = "https://mapi.guazi.com/car-source/carList/pcList?minor=benz&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=&order=&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page={}&pageSize=20&city_filter=12&city=12&guazi_city=12&versionId=0.0.0.0&osv=Unknown&platfromSource=wapp".format(
        page)
    response = requests.get(url=url, headers=headers)
    html = response.content.decode("utf-8")
    content = json.loads(html)
    postList = content.get("data").get("postList")
    if postList == []:
        break
    else:
        page += 1
    # print(postList)
    for value in postList:
        info_car = {}
        info_car["汽车名字"] = value["title"]
        info_car["年份"] = value["license_date"]
        # info_car["钱"] = value["price"]
        try:
            info_car["价钱"] = value["buyOutPrice"]
        except:
            info_car["价钱"] = "暂时没有信息"
        info_cars.append(info_car)
    print(info_cars, len(info_cars))

with open(os.path.join("奔驰车信息" + ".csv"), "w", encoding="GB18030", newline="") as f:
    witer = csv.DictWriter(f, fieldnames=["汽车名字", "年份", "价钱"])
    witer.writeheader()
    witer.writerows(info_cars)
