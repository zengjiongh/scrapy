# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import json
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JdGuessPipeline:
    def __init__(self):
        self.f = open("id_info.csv", "a", newline="", encoding="GB18030")
        self.fieldnames = ["name", "color", "size", "year", "mouth", "Praise_rate", "price", "link"]
        self.writer = csv.DictWriter(self.f, self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.f.close()
