import scrapy
from scrapy.selector import HtmlXPathSelector,Selector
# from scrapy. import
class XiaohuanSpider(scrapy.Spider):
    name='xh'
    allowed_domains=['xiaohuar.com']
    start_urls=['http://www.xiaohuar.com/hua/']

    def parser(self,response):
        #//a 表示要找整个页面的所有的a标签
        # print(response.text)
        hxs=HtmlXPathSelector(response)
        result=hxs.select('//div[@class="masonry_brick"]')
        #result=hxs.select('//div[@class="masonry_brick"]').extract() #这样就会变成列表 , 如果不加extract 就是对象

        print(result)
        #   .extract
        #正则查找  找到所有的页码 re:test
        result=hxs.xpath('/a[re:test(@href,"http://www.xiaohuar.com/list-1-\d+.html")]/@href')

        hxs=Selector(response)
        hxs.xpath('//div[@class="part2"]/share-link')



        #递归的再回去爬取下一页的 parser
        for url in result:
            yield  Request(url=url,callback=self.parser)




