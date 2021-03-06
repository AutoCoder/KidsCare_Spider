'''
Created on 2014.6.12

@author: HELI
'''
from scrapy.selector import Selector
from scrapy.http import Request

#from spiderutility import SpiderUtility
from kidscare.items import Milk
from kidscare.spiders.basespider import MilkSpider
from scrapy import log

import sys
#import re
#import json

class SFMilk_Spider(MilkSpider):
    name = "sfbest"
    allowed_domains = ["www.sfbest.com"]
    start_urls = [
        "http://www.sfbest.com/baby/79-0-0-0-0-2-0-0-0-0-0.html",
        "http://www.sfbest.com/baby/80-0-0-0-0-2-0-0-0-0-0.html",
        "http://www.sfbest.com/baby/81-0-0-0-0-2-0-0-0-0-0.html",
        "http://www.sfbest.com/baby/82-0-0-0-0-2-0-0-0-0-0.html",
        "http://www.sfbest.com/baby/83-0-0-0-0-2-0-0-0-0-0.html",
        "http://www.sfbest.com/baby/84-0-0-0-0-2-0-0-0-0-0.html",
    ]
    
    def __init__(self):
        super(SFMilk_Spider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        #sel = Selector(response)
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        listdata = sel.xpath('//ul[@class="list-all"]/li')
        
        item = Milk()
        for prod in listdata:
            try:
                prod_inner_node = prod.xpath('div[@class="l-wrap"]')
                title = prod_inner_node.xpath('div[@class="title-c"]/a/@title').extract()[0]
                prod_link = prod_inner_node.xpath('div[@class="title-c"]/a/@href').extract()[0]
                pic_link = prod_inner_node.xpath('div[@class="pic"]/a/img/@data').extract()[0]
                price = prod_inner_node.xpath('div[@class="price"]/span/strong/text()').extract()[0]
                item["prod_link"] = prod_link
                item["pic_link"] = pic_link
                item["price"] = float(price)
                dict = super(SFMilk_Spider, self).ParseTitleToDict(title)
                item["name"] = dict["name"]
                item["brand"] = dict["brand"]
                item["segment"] = dict["segment"]
                item["volume"] = dict["volume"]
                item["unitprice"] = item["price"] / dict["volume"] * 100.0
                if item["unitprice"] < 90 and item["unitprice"] > 10:
                    yield item
                    
            except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[sf_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg('[sf_milk] item : %s' % item, log.ERROR)
        
        nextpage_node = sel.xpath('//a[@class="next"]/@href')
        if not nextpage_node:
            return
        else:
            nextpage_link = nextpage_node.extract()[0]
        
        yield Request(url=nextpage_link, callback=self.parse)
        
    def __unicode__(self):
        return unicode(self.name)