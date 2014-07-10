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

class JDMilk_Spider(MilkSpider):
    name = "jd"
    allowed_domains = ["http://m.jd.com"]
    start_urls = [
        "http://m.jd.com/products/1319-1523-7052.html",
    ]
    
    def __init__(self):
        super(MilkSpider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        #sel = Selector(response)
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        listdata = sel.xpath('//div[@class="pmc"]')
        
        item = Milk()
        for prod in listdata:
            try:
                title = prod.xpath('div[@class="title"]/text()').extract()[0].strip()
                prod_link = self.allowed_domains[0] + prod.xpath('div[@class="title"]/a/@href').extract()[0].strip()
                pic_link = prod.xpath('div[@class="pic"]/a/img/@src').extract()[0].strip()
                price = prod.xpath('div[@class="price"]/Font/text()').extract()[0].strip()[1:]
                item["price"] = float(price)
                item["pic_link"] = str(pic_link)
                item["prod_link"] = str(prod_link)
                dict = self.__ParseTitleToDict(title)
                item["name"] = dict["name"]
                item["brand"] = dict["brand"]
                item["segment"] = dict["segment"]
                item["volume"] = dict["volume"]  
                yield item
                
            except Exception, info: #IndexError
                s=sys.exc_info()             
                log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg("[jd_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                log.msg('[jd_milk] item : %s' % item, log.ERROR)
                
        nextpage_node = sel.xpath('//div[@class="page"]/a')[0]
        nextpage_link = self.allowed_domains[0] + nextpage_node.xpath('@herf').extract()[0].strip()
        
        yield Request(nextpage_link, callback=self.parse)
    
    def __ParseTitleToDict(self, title):
        dict = {}
        
        i_duan = title.find(u"\u6bb5")
        if i_duan != -1 :
            dict["segment"] = int(title[i_duan-1])
            
        i_ke = title.find(u"\u514b") # find ke
        if i_ke != -1:
            volume = int(title[i_ke-3:i_ke])
            
        i_g = title.find(u"g") # find ke
        if i_g != -1:
            volume = int(title[i_g-3:i_g])
            
        i_G = title.find(u"G") # find ke
        if i_G != -1:
            volume = int(title[i_G-3:i_G])
                    
        i_mul = title.find(u"g*")
        if i_mul != -1:
            volume = int(title[i_mul-3:i_mul]) * int(title[i_mul+1])
        
        dict["volume"] = volume   
        return dict
    
    def __unicode__(self):
        return unicode(self.name)