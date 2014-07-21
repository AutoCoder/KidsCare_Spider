'''
Created on 2014.6.12

@author: HELI
'''
from scrapy.selector import Selector
from scrapy.http import Request

#from spiderutility import SpiderUtility
from kidscare.items import Milk
from kidscare.spiders.basespider import MilkSpider, ImageDir
from scrapy import log
import urllib2
import sys
import time
import os
#import re
#import json

def downLoadImg(url,location):
    try:
        req=urllib2.Request(url)
        u=urllib2.urlopen(req)
        content=u.read()
        f = open(location, "w+b")
        f.write(content)
        f.close()
    except Exception,e:
        log.msg('download price image fail : %s' % e, log.ERROR)
                
class SUNINGMilk_Spider(MilkSpider):
    name = "suning"
    #allowed_domains = ["http://www.qunar.com/"]
    start_urls = [
        "http://list.suning.com/0-313006-0-1-0-9264.html",
        "http://list.suning.com/0-313007-0-1-0-9264.html",
        "http://list.suning.com/0-313008-0-1-0-9264.html",
        "http://list.suning.com/0-313009-0-1-0-9264.html",
    ]
    
    def __init__(self):
        super(SUNINGMilk_Spider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        #sel = Selector(response)
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        prodlist_node = sel.xpath('//div[@id="proShow"]')
        listdata = prodlist_node.xpath('ul/li')
        
        item = Milk()
        for prod in listdata:
            try:
                prod_link = prod.xpath('a/@href').extract()[0]
                pic_link = prod.xpath('a/img/@src | a/img/@src2').extract()[0]
                info_node = prod.xpath('div[@class="inforBg"]')
                price_link = info_node.xpath('p[@class="price"]/img/@src | p[@class="price"]/img/@src2').extract()[0] #price image link
                #fp = urllib2.urlopen(price, timeout=5)
                location = "".join([ImageDir, '/', str(int(time.time())), '.png'])
                downLoadImg(price_link, location)
                item["prod_link"] = prod_link
                item["pic_link"] = pic_link
                item["price"] = location
                title = info_node.xpath('span/a/p/text()').extract()[0]
                dict = super(SUNINGMilk_Spider, self).ParseTitleToDict(title)
                item["name"] = dict["name"]
                item["brand"] = dict["brand"]
                item["segment"] = dict["segment"]
                item["volume"] = dict["volume"]
                #item["unitprice"] = item["price"] / dict["volume"] * 100.0
                #if item["unitprice"] < 90 and item["unitprice"] > 10:
                yield item
                    
            except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[suning_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg('[suning_milk] item : %s' % item, log.ERROR)
        
        nextpage_node = sel.xpath('//a[@id="nextPage"]/@href')
        if not nextpage_node:
            return
        else:
            nextpage_link = "http://list.suning.com" + nextpage_node.extract()[0]
        
        yield Request(url=nextpage_link, callback=self.parse)
        
    
    def __unicode__(self):
        return unicode(self.name)