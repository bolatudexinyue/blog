import json


from lxml import etree

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
import re
import time
from weibo.items import *
from scrapy_redis.spiders import RedisCrawlSpider

class Mysiper(RedisCrawlSpider):
    name = 'weibospider'
    redis_key = 'weibo:start_urls'
    #微博文章接口,其中还包含有部分用户信息，同时也有进入手机web端关注和粉丝列表页面的链接，有了这个链接进去后就可以用开发者工具调试找到follows和fans的接口
    #进入手机web端关注和粉丝列表页面的链接在crads[1].get('card_group')[0].get('scheme'),example:https://m.weibo.cn/p/index?containerid=231051_-_followers_-_1989252873_-_1042015%253AtagCategory_032&luicode=10000011&lfid=1076031989252873
    #这个链接在自己的文章接口里没有
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={id}&type={id}&page=1&containerid=107603{id}'
    #微博用户信息接口
    #user_url = 'https://weibo.com/p/100505{id}/info?mod=pedit_more'
    user_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{id}_-_INFO&luicode=10000011&lfid=230283{id}&featurecode=20000320'
    #微博关注接口，只能爬10页，约200个关注
    follows_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{id}&luicode=10000011&lfid=107603{id}&page={page}'
    #微博粉丝接口,可以爬250页，共5000个粉丝
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{id}&luicode=10000011&lfid=107603{id}&since_id={since_id}'
    #依次为      杨幂id,  胡歌id， 思想聚焦id, 恐怖电影频道id, 全球健身中心id, 情感馆主id, 谷大白话id
    #start_id = [1195242865, 1223178222, 1742566624, 2818008641, 2142168143, 1106957832, 1788911247]

    start_id = [1223178222]



    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        'Host': 'm.weibo.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'}

    cookies = {'_T_WM': 'fd71d6898c4ef379fcbf55fd7130e881', 'ALF': '1530856113',
               'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WhWFcDNxSlo32q.J.UbOPie5JpX5K-hUgL.Fo2ceo.pSK54S0e2dJLoI7D8dG9DMfv2dc4r',
               'SCF': 'Ap_sWUsaj47YpxRzJazJwdZK7CwLoCO2xUjB8t-U8e-VOMx5Mb6lhJIKNx0kErRa_a9UmVdgY2w8I3T8asUALn0.',
               'SUB': '_2A252E-ekDeRhGedI6VsQ9S7FzD-IHXVV_4nsrDV6PUJbktANLXnckW1NV7YNXpNbktzO1LXue9m3UNxvx0nixOD1',
               'SUHB': '0N2EVh4OByZB71', 'SSOLoginState': '1528272884', 'MLOGIN': '1', 'WEIBOCN_FROM': '1110006030',
               'M_WEIBOCN_PARAMS': 'luicode%3D10000011%26lfid%3D2302835940597074%26featurecode%3D20000320%26fid%3D2302835940597074_-_INFO%26uicode%3D10000011'}

    #cookies = {'SINAGLOBAL': '7160919484502.779.1527500681778', 'un': '13820592407', 'TC-Page-G0': '444eec11edc8886c2f0ba91990c33cda', '_s_tentry': '-', 'Apache': '8987204970637.05.1528251482936', 'ULV': '1528251482962:9:3:3:8987204970637.05.1528251482936:1528210500896', 'TC-V5-G0': '589da022062e21d675f389ce54f2eae7', 'TC-Ugrow-G0': 'e66b2e50a7e7f417f6cc12eec600f517', 'login_sid_t': '4d2ca262fe6959a4d7537190d72353c1', 'cross_origin_proto': 'SSL', 'wb_view_log': '1366*7681', 'WBtopGlobal_register_version': 'cd58c0d338fe446e', 'SCF': 'Ap_sWUsaj47YpxRzJazJwdZK7CwLoCO2xUjB8t-U8e-VFvzaPZyzw8mLuYnlW1nNT3gRAE0mt59AgGihOx14g70.', 'SUB': '_2A252EwXhDeRhGedI6VsQ9S7FzD-IHXVVaXAprDV8PUNbmtAKLXHNkW9NV7YNXo1BLS_r777tLuzu7K0jkdKmTf50', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WhWFcDNxSlo32q.J.UbOPie5JpX5K2hUgL.Fo2ceo.pSK54S0e2dJLoI7D8dG9DMfv2dc4r', 'SUHB': '0d4PdgK6TbMsi8', 'ALF': '1528868684', 'SSOLoginState': '1528264113', 'wvr': '6', 'UOR': 'www.baidu.com,www.weibo.com,www.baidu.com'}

    def start_requests(self):
        for id in self.start_id:
            yield Request(self.weibo_url.format(id=id),callback=self.parse_weibo)

    def parse_weibo(self,response):
        witem = WeiboItem()
        uitem = WeiboUserItem()
        s = json.loads(response.text)
        if s.get('ok') and s.get('data'):
            cards = s.get('data').get('cards')
            mblog = cards[0].get('mblog')
            usercollection = mblog.get('user')
            id = usercollection.get('id')
            witem['id'] = id
            name = usercollection.get('screen_name')
            witem['user'] = name
            field_map = {'id':'id','name':'screen_name','verified':'verified',
                         'verified_reason':'verified_reason','vip_level':'mbrank','level':'urank',
                         'follows_count':'followers_count','fans_count':'follow_count',
                         'headImg':'avatar_hd','weibos_count':'statuses_count','description':'description'}
            for k,v in field_map.items():
                uitem[k] = usercollection.get(v)
            uitem['is_vip'] = True if usercollection.get('mbrank') else False
            yield uitem
            if 'isTop' not in mblog:
                witem['is_top'] = False
                witem['latest_created_at'] = mblog.get('created_at')
                witem['source'] = mblog.get('source')
                field_list = ['transmit_count','comments_count','like_count','pictures','content']
                for field in field_list:
                    witem[field] = None
            else:
                witem['is_top'] = True
                field_map = {'transmit_count':'reposts_count','comments_count':'comments_count',
                             'like_count':'attitudes_count','content':'text'}
                for k,v in field_map.items():
                    witem[k] = mblog.get(v)
                pictures = []
                if mblog.get('pics'):
                    for pic in mblog.get('pics'):
                        pictures.append(pic.get('url'))
                witem['pictures'] = pictures
                try:
                    mblog_first = cards[2].get('mblog')
                    witem['latest_created_at'] = mblog_first['created_at']
                    witem['source'] = mblog_first['source']
                except Exception as e:
                    witem['latest_created_at'] = None
                    witem['source'] = None
            yield witem

            #yield Request(self.user_url.format(id=id),headers=self.headers1,cookies=self.cookies,meta={'id':id},callback=self.parse_user)
            #yield Request(self.user_url.format(id=id),meta={'id':id},callback=self.parse_user)
            yield Request(self.follows_url.format(id=id,page=1),meta={'id':id,'page':1},callback=self.parse_follows)
            yield Request(self.fans_url.format(id=id,since_id=1),meta={'id':id,'since_id':1},callback=self.parse_fans)




    def parse_user(self,response):

        id = response.meta.get('id')
        uitem = WeiboUserItem()
        uitem['id'] = id
        #print(response.text)
        s = json.loads(response.text)

        print(s)
        if s.get('ok') and s.get('data'):
            s1 = s.get('data')
            s2 = s1.get('cards')[0]

            card_group = s2.get('card_group')
            for card in card_group:
                if card.get('item_name') == '注册时间':
                    uitem['register_date'] = card.get('item_content')
            if len(s1.get('cards')) >= 2:
                s3 = s1.get('cards')[1]
                card_group1 = s3.get('card_group')
                for card in card_group1:
                    if card.get('item_name') == '性别':
                        uitem['gender'] = card.get('item_content')

                    if card.get('item_name') == '生日':
                        uitem['birth'] = card.get('item_content')

                    if card.get('item_name') == '所在地':
                        uitem['location'] = card.get('item_content')

                    if card.get('item_name') == '大学':
                        uitem['college'] = card.get('item_content')

                    if card.get('item_name') == '公司':
                        uitem['company'] = card.get('item_content')

                    if card.get('item_name') == '血型':
                        uitem['bloodType'] = card.get('item_content')
        field_list = ['register_date','gender','birth','location','college','company','bloodType']
        for field in field_list:
            if not uitem.get(field):
                uitem[field] = None
        yield uitem

    #解析用户信息的备用方法
    # def parse_user(self,response):
    #     id = response.meta.get('id')
    #     uitem = WeiboUserItem()
    #     uitem['id'] = id
    #     #print(response.text)
    #     res = BeautifulSoup(response.text, 'lxml')
    #     scripts = res.select('script')
    #     #print(scripts)
    #     for script in scripts:
    #         if '基本信息' in script.text:
    #             print('-------------------------------')
    #             s = script.text
    #             t = s.lstrip('FM.view(').rstrip(')')
    #             result = json.loads(t)
    #             print(result)
    #             temp = result['html']
    #             # print(temp)
    #             fre = '<!DOCTYPE html><html><head><meta charset="utf-8"/><title></title></head><body>'
    #             after = '</body></html>'
    #             newhtml = fre + temp + after
    #             ehtml = etree.HTML(newhtml)
    #             ul = ehtml.xpath('/html/body/div[1]/div/div[2]/div/ul')[0]
    #             #print(ul)
    #             for li in ul:
    #                 label = li.xpath('./span[1]/text()')[0]
    #                 print(label)
    #                 content = None
    #                 if li.xpath('./a'):
    #                     content = li.xpath('./a/text()')[0].strip()
    #                 if li.xpath('./span[2]'):
    #                     content = li.xpath('./span[2]/text()')[0].strip()
    #                 if label == '注册时间：':
    #                     uitem['register_date'] = content
    #                 if label == '生日：':
    #                     uitem['birth'] = content
    #                 if label == '性别：':
    #                     uitem['gender'] = content
    #                 if label == '血型：':
    #                     uitem['bloodType'] = content
    #                 if label == '所在地：':
    #                     uitem['location'] = content
    #                 if label == '大学：':
    #                     uitem['college'] = content
    #                 if label == '公司：':
    #                     uitem['company'] = content
    #     field_list = ['register_date', 'gender', 'birth', 'location', 'college', 'company', 'bloodType']
    #     for field in field_list:
    #         if not uitem.get(field):
    #             uitem[field] = None
    #     yield uitem



    def parse_follows(self,response):
        id = response.meta.get('id')
        page = response.meta.get('page')
        follows_item = UserRleationItem()
        follows_item['id'] = id
        s = json.loads(response.text)
        follows_list = []
        if s.get('ok') and s.get('data') and s.get('data').get('cards'):
            s1 = s.get('data').get('cards')[-1]
            card_group = s1.get('card_group')
            for card in card_group:
                follows = card.get('user')
                uid = follows.get('id')
                name = follows.get('screen_name')
                temp = {'id':uid,'name':name}
                follows_list.append(temp)
                yield Request(self.weibo_url.format(id=uid),callback=self.parse_weibo)
            follows_item['follows'] = follows_list
            follows_item['fans'] = []
            #print(follows_list)
            #print('---------------------------------------------------------------')
            #print(follows_item)
            yield follows_item
            #print('*******************************************************************')
            page = page +1
            yield Request(self.follows_url.format(id=id,page=page),meta={'id':id,'page':page},callback=self.parse_follows)


    def parse_fans(self,response):
        id = response.meta.get('id')
        since_id = response.meta.get('since_id')
        fans_item = UserRleationItem()
        fans_item['id'] = id
        s = json.loads(response.text)
        fans_list = []
        if s.get('ok') and s.get('data') and s.get('data').get('cards'):
            s1 = s.get('data').get('cards')[-1]
            card_group = s1.get('card_group')
            for card in card_group:
                fans = card.get('user')
                uid = fans.get('id')
                name = fans.get('screen_name')
                temp = {'id':uid,'name':name}
                fans_list.append(temp)
                yield Request(self.weibo_url.format(id=uid),callback=self.parse_weibo)
            fans_item['fans'] = fans_list
            fans_item['follows'] = []
            #print(fans_list)
            #print('---------------------------------------------------------------')
            #print(fans_item)
            yield fans_item
            #print('*******************************************************************')
            since_id = since_id +1
            yield Request(self.fans_url.format(id=id,since_id=since_id),meta={'id':id,'since_id':since_id},callback=self.parse_fans)

















