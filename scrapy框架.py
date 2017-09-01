#
"""
scrapy框架的优点
∆延迟下载
#如果程序在一直爬别的网站时需要一个时间间隔，如果没有间隔可能会被禁爬

#如果在一个网站碰到两个同样的URL：肯定只下载一个就够
∆去重

在抓取网站内容时，是进入下一个页面，还是在当前继续爬下一个标签，这里涉及到  深度优先，或者 广度优先






"""



import scrapy


from scrapy.selector import HtmlXPathSelector
# class DmozItem(scrapy.Item):
#     title=scrapy.Field()
#     link=scrapy.Field()
#     desc=scrapy.Field()

# class DmozSpider(scrapy.Spider):
#     name = "baidu"
#     allowed_domains = ["baidu.org"]
#     start_urls = [
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
#     ]
#
#     def parse(self, response):
#         filename = response.url.split("/")[-2]
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#


































