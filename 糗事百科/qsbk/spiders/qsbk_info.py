import scrapy
import re
from qsbk.items import QsbkItem
class QsbkInfoSpider(scrapy.Spider):
    name = 'qsbk_info'
    # allowed_domains = ['qiushibaike.com/text/']
    page = 1
    base_url = 'https://www.qiushibaike.com/text/page/'
    start_urls = [base_url + str(page)]

    def parse(self, response):
        # url_link = response.xpath("//*[@class='article block untagged mb15 typs_long']/a/@href")
        url_link = re.findall('<a href="/article/(.*?)"',response.body.decode("utf-8"),re.S)
        # print(url_link)
        for i in url_link:
            http = "https://www.qiushibaike.com/article/" + i
            # print(http)
            yield scrapy.Request(http,callback=self.prase_info,meta={"url":http})
        next_page = response.xpath("//*[@id='content']/div/div[2]/ul/li/a/span/text()").extract()
        # next_page = next_page.replace("\n","")
        # print(next_page)
        if "\n下一页\n" in next_page:
            self.page += 1
            yield scrapy.Request(self.base_url + str(self.page),callback=self.parse)
        else:
            return

    def prase_info(self,response):
        item = QsbkItem()
        link = response.meta["url"]
        author = response.xpath("//*[@id='articleSideLeft']/div/div[1]/a/span/text()").extract()
        content = response.xpath("//*[@id='single-next-link']/div/text()").extract()
        # content = content.replace("\n","")
        content = ".\n".join(content)

        item["author"] = author
        item["content"] = content
        item["url_link"] = link
        print(item)
        yield item





