import json
import logging
import requests
import time
from scrapy import signals

class ProxyMiddleware(object):
    def __init__(self,proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    @classmethod
    def from_crawler(cls,crawler):
         return cls(proxy_url=crawler.settings.get('PROXY_URL'))

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self,request,spider):
        if request.meta.get('retry_times'):
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理'+ str(proxy))
                request.meta['proxy'] = uri

import redis
mydb = redis.StrictRedis(host='10.11.58.50', port=6379, password='123456',db=1)

class ProxyMiddleware1(object):
    def process_request(self,request,spider):
        if request.meta.get('retry_times') == 1:
            print('开始将失败的url存入数据库')
            if 'uid' in request.url:
                if mydb.zadd('failurl_weibo', 0, request.url):
                    print('url:'+request.url+'保存成功')
            elif 'followers' in request.url:
                if mydb.zadd('failurl_followers', 0, request.url):
                    print('url:'+request.url+'保存成功')
            elif 'fans' in request.url:
                if mydb.zadd('failurl_fans', 0, request.url):
                    print('url:'+request.url+'保存成功')

'''
class CookiesMiddleware():
    def __init__(self,cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url

    @classmethod
    def from_crawler(cls,crawler):
        return cls(cookies_url =crawler.settings.get('COOKIES_URL'))

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies =json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self,request,spider):
        self.logger.debug('正在获取cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            self.logger.debug('使用cookies'+json.dumps(cookies))
'''
