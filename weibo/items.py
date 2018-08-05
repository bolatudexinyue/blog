# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class WeiboUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'users'
    id = Field()
    name = Field()
    headImg = Field()
    gender = Field()
    description = Field()
    fans_count = Field()
    follows_count = Field()
    weibos_count = Field()
    verified = Field()
    verified_reason = Field()
    follows = Field()
    fans = Field()
    location = Field()
    birth = Field()
    bloodType = Field()
    register_date = Field()
    college = Field()
    company = Field()
    level = Field()
    is_vip = Field()
    vip_level = Field()
    crawled_at = Field()

class UserRleationItem(scrapy.Item):
    collection = 'users'
    id = Field()
    follows = Field()
    fans = Field()


class WeiboItem(scrapy.Item):
    collection = 'weibo'
    id = Field()
    user = Field()
    is_top = Field()
    transmit_count = Field()
    comments_count = Field()
    like_count = Field()
    pictures = Field()
    content = Field()
    created_at = Field()
    source = Field() #排除置顶微博后最近一条微博是用什么客户端发的
    latest_created_at = Field()#排除置顶微博后最近的一条微博是什么时间发的
    crawled_at = Field()



