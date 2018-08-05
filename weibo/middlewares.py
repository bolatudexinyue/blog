# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class WeiboSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
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


class WeiboDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        #request.cookies = {'Cookie':'SINAGLOBAL=7160919484502.779.1527500681778; un=13820592407; TC-Page-G0=444eec11edc8886c2f0ba91990c33cda; _s_tentry=-; Apache=8987204970637.05.1528251482936; ULV=1528251482962:9:3:3:8987204970637.05.1528251482936:1528210500896; TC-V5-G0=589da022062e21d675f389ce54f2eae7; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; login_sid_t=4d2ca262fe6959a4d7537190d72353c1; cross_origin_proto=SSL; wb_view_log=1366*7681; UOR=www.baidu.com,www.weibo.com,login.sina.com.cn; WBtopGlobal_register_version=cd58c0d338fe446e; SCF=Ap_sWUsaj47YpxRzJazJwdZK7CwLoCO2xUjB8t-U8e-VFvzaPZyzw8mLuYnlW1nNT3gRAE0mt59AgGihOx14g70.; SUB=_2A252EwXhDeRhGedI6VsQ9S7FzD-IHXVVaXAprDV8PUNbmtAKLXHNkW9NV7YNXo1BLS_r777tLuzu7K0jkdKmTf50; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhWFcDNxSlo32q.J.UbOPie5JpX5K2hUgL.Fo2ceo.pSK54S0e2dJLoI7D8dG9DMfv2dc4r; SUHB=0d4PdgK6TbMsi8; ALF=1528868684; SSOLoginState=1528264113'}
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


