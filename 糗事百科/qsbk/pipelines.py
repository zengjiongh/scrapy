# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql


class QsbkPipeline:
    def __init__(self):
        self.f = open("qsbk.json", "w", encoding="utf-8")

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        con = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(con)
        return item


class MysqlQsbkPiple(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host="127.0.0.1", port=3306, user='root', password='zjr', db="ZJR", charset="utf8")

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            value = 'insert into qsbk (作者,内容,链接) values ("%s","%s","%s")' % (
            item["author"], item["content"], item["url_link"])
            self.cursor.execute(value)
            self.conn.commit()
            # print(item)
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.conn.close()
