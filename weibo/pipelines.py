# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from weibo.items import *
import re
import time

class TimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,WeiboItem) or isinstance(item,WeiboUserItem):
            item['crawled_at'] = time.strftime('%Y-%m-%d %H:%M',time.localtime())
        return item


#对微博发布时间进行数据清洗，转化为本地标准化时间
class WeiboPipeline(object):
    def parse_time(self,date):
        if re.match('刚刚',date):
            date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        if re.match('(\d+)分钟前',date):
            minute = re.match('(\d+)分钟前',date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-float(minute)*60))
        if re.match('(\d+)小时前',date):
            hour = re.match('(\d+)小时前',date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-float(hour)*60*60))
        if re.match('昨天.*',date):
            pre_date = re.match('昨天(.*)',date).group(1)
            date = time.strftime('%Y-%m-%d',time.localtime(time.time()-float(24)*60*60)) + pre_date
        if re.match('今天.*',date):
            pre_date = re.match('今天(.*)',date).group(1)
            date = time.strftime('%Y-%m-%d',time.localtime(time.time())) + pre_date
        if re.match('(\d+)月(\d+)日(.*)',date):
            month = re.match('(\d+)月(\d+)日(.*)',date).group(1)
            day = re.match('(\d+)月(\d+)日(.*)',date).group(2)
            aft_date = re.match('(\d+)月(\d+)日(.*)',date).group(3)
            date = time.strftime('%Y-',time.localtime(time.time())) + month + '-'+day + aft_date
        return date
    def process_item(self, item, spider):
        if isinstance(item,WeiboItem):
            if item.get('created_at'):
                item['created_at'] = self.parse_time(item['created_at'])
            if item.get('latest_created_at'):
                item['latest_created_at'] = self.parse_time(item['latest_created_at'])
        return item

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_uri = crawler.settings.get('MONGO_URI'),mongo_db=crawler.settings.get('MONGO_DATABASE'))

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[WeiboUserItem.collection].create_index([('id',pymongo.ASCENDING)])
        self.db[WeiboItem.collection].create_index([('id',pymongo.ASCENDING)])

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        if isinstance(item,WeiboUserItem) or isinstance(item,WeiboItem):
            self.db[item.collection].update({'id':item.get('id')},{'$set':item},True)
        if isinstance(item,UserRleationItem):
            print('UserRleationItem is coming')
            self.db[item.collection].update({'id':item.get('id')},{'$addToSet':{'follows':{'$each':item['follows']},'fans':{'$each':item['fans']}}},True)
        return item








