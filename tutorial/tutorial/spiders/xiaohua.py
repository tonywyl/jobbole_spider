# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request

class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://www.jobbole.com/']
    cookie_dict={}
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,dont_filter=True,callback=self.parse0)

    def parse0(self,response):
        """
        登录
        :param response:
        :return:
        """
        login_url='http://www.jobbole.com/wp-admin/admin-ajax.php'

        post_data={
            "action": "user_login",
            "user_login": 'oldhiu',
            "user_pass": 'YX9kjnRnIyv4d5U)',
            "remember_me": 1,
            "redirect_url": "http://www.jobbole.com",
        }
        import urllib.parse

        yield Request(url=login_url,
                      method='POST',
                      body=urllib.parse.urlencode(post_data),
                      headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'},
                      callback=self.parse,
                      )


    def parse(self, response):
        """
        进入首页
        :param response:
        :return:
        """
        # print(response.text)
        # result=Selector(text=response.text).xpath('//h3/text()').extract()#不加extract 是保留HTML标签
        # print(response.text,'----')
        yield Request(url='http://www.jobbole.com/',callback=self.parse00)


        """
        android---- http://android.jobbole.com/wp-admin/admin-ajax.php
        top:        http://top.jobbole.com/wp-admin/admin-ajax.php
        http://group.jobbole.com/wp-admin/admin-ajax.php

        点赞
        formdata
        {
        action:vote_post_action
        post_id:93250
        }
        """


    def parse00(self,response):
        """
        跳转至这一篇文章
        :param response:
        :return:
        """
        # print(response.text,'=-=-=-')

        url_list = response.selector.xpath('//div[@class="post-meta"]/p/a[@class="meta-title"]/@href').extract()
        # print(url_list)
        for url in url_list:
            yield Request(url=url, method='GET', callback=self.parse1)


    def parse1(self,response):

        last_url=re.findall('http://\w+\.\w+\.com',response.url)[0]#http://blog.jobbole.com/112239
        last_url=last_url+'/wp-admin/admin-ajax.php'
        hxs=Selector(response)
        id=hxs.xpath('//div[@class="post-adds"]/span/@data-post-id').extract_first()
        # print(id,'=======')
        """cookie 获取"""
        from scrapy.http.cookies import CookieJar
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)

        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        data={
          "action":"vote_post_action",
          "post_id":id,

      }
        # print(last_url)
        import urllib.parse
        # print(id, '---#--------')
        yield Request(url=last_url,
                      method='POST',
                      body=urllib.parse.urlencode(data),
                      headers={"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"},
                      callback=self.parse2)

    def parse2(self,response):

        print(response.text,'---',)
        print(response.encoding('utf-8'),'---',)