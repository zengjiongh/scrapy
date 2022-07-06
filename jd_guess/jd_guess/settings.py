# Scrapy settings for jd_guess project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql
from fake_useragent import UserAgent

BOT_NAME = 'jd_guess'

SPIDER_MODULES = ['jd_guess.spiders']
NEWSPIDER_MODULE = 'jd_guess.spiders'

LOG_LEVEL = "WARNING"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'jd_guess (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
ua = UserAgent()
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': ua.random,
    'cookie': "shshshfpa=f9f300d1-106b-2f1b-ed5a-4b3b34e972c8-1636251432; shshshfpb=xdNLUP6VOlbdDKJE9e5MaJA%3D%3D; areaId=0; __jdu=1636251432262541638300; qrsc=3; pinId=n4OlR52jvHJ1kED2e-l_jLV9-x-f3wj7; pin=jd_49fe4088ace97; unick=jd_49fe4088ace97; _tp=HMYGyo58KaPYBsv58H4BqUUe%2F0PRX2buD4sG170RhUQ%3D; _pst=jd_49fe4088ace97; ipLoc-djd=1-72-55653-0; user-key=97568692-c140-4c2e-b081-f7ff054d7280; mt_xid=V2_52007VwMVUFpbVloaSxpfAmQHF1JaWltYHkgpXA1uURVaDV9OXB1AS0AAMAJGTg4PVA0DQRwLBGFUQVoJXlsPL0oYXwV7AxJOXVtDWhpCGFsOZAMiUG1YYl8ZTRFVBmEKE1JtXVNTGQ%3D%3D; unpl=V2_ZzNtbRBVQRAnWE9QKUxcUGIFQg1LUktCcwARU39OWwwyChINclRCFnUURlRnGVgUZwoZWUFcQhFFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHseXgJkBxJYQFRAEnYMQ1R8G1UHZgIibUVncyVzCUZXeyldNWYzUAkeUUIcdwBGGXseXgJkBxJYQFRAEnYMQ1R8G1UHZgIiXHJU; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_c334ca85cd1d47aa849f79f65f68d81a|1636973564993; PCSYCityID=CN_0_0_0; __jda=122270672.1636251432262541638300.1636251432.1636709185.1636973565.17; __jdc=122270672; shshshfp=84a46e76ff87fb0199eb2856cd699464; rkv=1.0; wlfstk_smdl=aml3jvyxhphm62lzt86iw4b56v51rmv2; TrackID=1xZG1IC1KFdHtPQQgPVY__TM3SS4ClPEUxxvE5vmlEIqhZKmjCPR3j2Th_faj43WHMRzWeXhPIpEc74GhVCjZjTrB17qwa1NlU8ejpzVJ11Y; thor=0F4BB709E13D4A49811F12E9BA7902C53F6E8041EEA43F26C34B6B2D3615505A4124D50791F8DCAC01EDCDF289AD4052B5794DEC13A12682FF4974C3313A662F0A88B09F6397D0E0AC12336E512CD8D27418BA18E93BB395EDA1EDAA85E24A4A7757581F7372C8AE990C3C305A4137F93A7827726A939B95E7F2CF62F5B7841D34C450C02369CA82BDABEF7FB3DDF67B268CCA75782C4B5B69380AD9AED0F7DE; ceshi3.com=000; __jdb=122270672.5.1636251432262541638300|17.1636973565; shshshsID=27978fe5a2944839d8679aed5036fceb_3_1636973616852; 3AB9D23F7A4B3C9B=JL2O6STR2EZO7RCYFDWNEOROT7M47E6CBAAVHPPDZVUYTKTRYEYT2CWIQLYXUDEFLH3BCBW7YSCIRDK35RQCA4Z65A"
}

# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'jd_guess.middlewares.JdGuessSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'jd_guess.middlewares.JdGuessDownloaderMiddleware': 543,
}

con = pymysql.Connect(host="127.0.0.1", port=3306, user="root", password="zjr", db='ZJR', charset='utf8')
cos = con.cursor()
all = None
try:
    cos.execute("""select * from ip;""")
    all = cos.fetchall()
    con.commit()
except:
    con.rollback()
cos.close()
con.close()
http_ip_list = []
https_ip_list = []
for i in all:
    if "http" in i:
        http_ip = i[1] + "://" + i[2] + ":" + i[3]
        http_ip_list.append(http_ip)
    else:
        https_ip = i[1] + "://" + i[2] + ":" + i[3]
        https_ip_list.append(https_ip)
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'jd_guess.pipelines.JdGuessPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# FEED_EXPORT_ENCODING ='GB18030'
