# -*-coding:utf-8-*-
import scrapy
import re
import json
import time
from fake_useragent import UserAgent
from jd_guess.items import JdGuessItem


class GuessYouLikeSpider(scrapy.Spider):
    name = 'guess_you_like'
    page = 0
    base_url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&suggest=2.his.0.0&wq=%E6%89%8B%E6%9C%BA&pvid=ce9b2495b7114ac7be1aa163107a3074&page="
    start_urls = [base_url + str(page)]
    id = None

    def parse(self, response):
        link = response.xpath("//*[@id='J_goodsList']/ul/li/div/div[1]/a/@href").extract()
        for i in link:
            url = "https:" + i
            # print(url)
            yield scrapy.Request(url, callback=self.parse_info, meta={"url": url})
        price = response.xpath("//*[@id='J_goodsList']/ul/li/div/div[3]/strong/i//text()").extract()
        if price != []:
            self.page += 1
            yield scrapy.Request(self.base_url + str(self.page), callback=self.parse)

    def parse_info(self, response):
        item = JdGuessItem()
        url = response.meta["url"]
        name = re.findall(">商品名称：(.*?)<", response.body.decode("utf-8"), re.S)
        color = response.xpath("//*[@id='choose-attr-1']/div[2]/div/a/img/@alt").extract()
        size = response.xpath("//*[@id='choose-attr-2']/div[2]/div/@title").extract()
        try:
            year = re.findall("<dt>上市年份</dt><dd>(.*?)</dd>", response.body.decode("utf-8"), re.S)[0]
        except:
            year = "暂时没有相关信息"
        try:
            mouth = re.findall("<dt>上市月份</dt><dd>(.*?)<", response.body.decode("utf-8"), re.S)[0]
        except:
            mouth = "暂时没有相关信息"
        self.id = re.findall("https://item.jd.com/(.*?).html", url, re.S)[0]
        lianjie = "https://item.jd.com/" + self.id + ".html"
        item["name"] = name
        item["color"] = color
        item["size"] = size
        item["year"] = year
        item["mouth"] = mouth
        item["link"] = lianjie
        url1 = "https://club.jd.com/comment/productPageComments.action?&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1".format(
            self.id)
        yield scrapy.Request(url1, callback=self.parse_prate, meta={"item": item, "id": self.id})

    def parse_prate(self, response):
        item = response.meta["item"]
        id = response.meta["id"]
        try:
            content = json.loads(response.body.decode("utf-8"))[0]
            Praise_rate = str(content.get("productCommentSummary").get("goodRateShow")) + "%"
            item["Praise_rate"] = Praise_rate
        except:
            item["Praise_rate"] = "暂时不能显示"
        url2 = "https://p.3.cn/prices/mgets?type=1&area=1_72_55653_0&pdtk=&pduid=1636251432262541638300&pdpin=jd_49fe4088ace97&pin=jd_49fe4088ace97&pdbp=0&skuIds={}".format(
            id)
        yield scrapy.Request(url2, callback=self.prase_price, meta={"item": item})

    def prase_price(self, response):
        item = response.meta["item"]
        try:
            html1 = json.loads(response.body.decode("utf-8"))[0]
            price = html1.get("p")
            item["price"] = price
        except:
            item["price"] = "暂时不能显示"
        print(item)
        yield item
