'''
Created on 2014.7.17

@author: HELI
'''
from scrapy.selector import Selector
from scrapy.http import Request
from kidscare.items import Milk
from kidscare.spiders.basespider import MilkSpider
from scrapy import log

import sys
#import re
#import json

class WWMilk_Spider(MilkSpider):
    name = "weiwei"
    allowed_domains = ["www.homevv.com"]
    start_urls = [
        "http://www.homevv.com/vvshopProSearchList/conParams-101168.jhtml",
    ]
    
    def __init__(self):
        super(WWMilk_Spider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        listdata = sel.xpath('//div[@class="list_prot"]/ul/li')
        item = Milk()
        for prod in listdata:
            try:
                price_str = prod.xpath('div/div[@class="shop_price"]/span[@class="mo_b"]/text()').extract()[0][1:]
                title = prod.xpath('div/div[@class="introduction"]/a/@title').extract()[0]
                prod_link = self.allowed_domains[0] + prod.xpath('div/div[@class="shop_appearance"]/a/@href').extract()[0]
                pic_link = self.allowed_domains[0] + prod.xpath('div/div[@class="shop_appearance"]/a/img/@src').extract()[0]
                item["prod_link"] = prod_link
                item["pic_link"] = pic_link
                item["price"] = float(price_str)                
                dict = super(WWMilk_Spider, self).ParseTitleToDict(title)
                item["name"] = dict["name"]
                item["brand"] = dict["brand"]
                item["segment"] = dict["segment"]
                item["volume"] = dict["volume"]
                item["unitprice"] = item["price"] / dict["volume"] * 100.0
                if item["unitprice"] < 90 and item["unitprice"] > 10:
                    yield item
                    
            except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[weiwei_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg('[weiwei_milk] item : %s' % item, log.ERROR)
        
#         nextpage_node = sel.xpath('//a[@class="next"]/a/@href')
#         if not nextpage_node:
#             return
#         else:
#             nextpage_link = "http://" + self.allowed_domains[0] + nextpage_node.extract()[0]
#         
#         yield Request(url=nextpage_link, callback=self.parse)
        
    def __unicode__(self):
        return unicode(self.name)