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
import re
#import json

class DDMilk_Spider(MilkSpider):
    name = "dangdang"
    allowed_domains = ["category.dangdang.com"]
    start_urls = [
        "http://category.dangdang.com/cid4001976.html",
    ]
    
    def __init__(self):
        super(DDMilk_Spider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        #sel = Selector(response)
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        listdata = sel.xpath('//ul[@class="list_aa bigimg"]/li')
        
        item = Milk()
        for prod in listdata:
            try:
                prod_inner_node = prod.xpath('div[@class="inner"]')
                title = prod_inner_node.xpath('a[@class="pic"]/@title').extract()[0]
                prod_link = prod_inner_node.xpath('a[@class="pic"]/@href').extract()[0]
                pic_link = prod_inner_node.xpath('a[@class="pic"]/img/@data-original').extract()[0]
                price = prod_inner_node.xpath('p[@class="price"]/span[@class="price_n"]/text()').extract()[0][1:]
                item["prod_link"] = self.transfer2mobile(prod_link)
                item["pic_link"] = pic_link
                item["price"] = float(price)
                dict = super(DDMilk_Spider, self).ParseTitleToDict(title)
                item["name"] = dict["name"]
                item["brand"] = dict["brand"]
                item["segment"] = dict["segment"]
                item["volume"] = dict["volume"]
                item["unitprice"] = item["price"] / dict["volume"] * 100.0
                if item["unitprice"] < 90 and item["unitprice"] > 10:
                    yield item
                    
            except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[dangdang_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg('[dangdang_milk] item : %s' % item, log.ERROR)
        
        nextpage_node = sel.xpath('//li[@class="next"]/a/@href')
        if not nextpage_node:
            return
        else:
            nextpage_link = "http://" + self.allowed_domains[0] + nextpage_node.extract()[0]
        
        yield Request(url=nextpage_link, callback=self.parse)
        
    def transfer2mobile(self, prod_link):
        m = re.match(ur".*?/(\d+)\.html", prod_link)
        if m:
            prod_id = m.group(1)
            return "http://m.dangdang.com/product.php?pid=%s" % prod_id
        else: 
            return prod_link
        
        
    def __unicode__(self):
        return unicode(self.name)