# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from jd_guess.settings import http_ip_list,https_ip_list
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent
import pymysql
class JdGuessSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdGuessDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    ua = UserAgent()
    # con = pymysql.Connect(host="127.0.0.1", port=3306, user="root", password="zjr", db='ZJR', charset='utf8')
    # cos = con.cursor()
    # all = None
    # try:
    #     cos.execute("""select * from ip;""")
    #     all = cos.fetchall()
    #     con.commit()
    # except:
    #     con.rollback()
    # cos.close()
    # con.close()
    # http_ip_list = []
    # https_ip_list = []
    # for i in all:
    #     if "http" in i:
    #         http_ip = i[1] + "://" + i[2] + ":" + i[3]
    #         http_ip_list.append(http_ip)
    #     else:
    #         https_ip = i[1] + "://" + i[2] + ":" + i[3]
    #         https_ip_list.append(https_ip)
    # print(https_ip_list)
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # request.headers["User-Agent"] = self.ua.random
        # if request.url.split(":")[0] == "http":
        #     request.meta["proxy"] = random.choice(http_ip_list).strip()
        #
        # else:
        request.meta["proxy"] = random.choice(https_ip_list).strip()
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called


    def process_response(self, request, response, spider):
        if response.status != 200:
            if request.url.split(":")[0] == "http":
                request.meta["proxy"] = random.choice(http_ip_list).strip()
                print(random.choice(http_ip_list))

            else:
                request.meta["proxy"] = random.choice(https_ip_list)
                print(random.choice(https_ip_list))
            return request
        return response

        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        return None


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
