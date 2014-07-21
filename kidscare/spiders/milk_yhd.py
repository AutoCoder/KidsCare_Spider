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

class YHDMilk_Spider(MilkSpider):
    name = "yhd"
    #allowed_domains = ["http://www.qunar.com/"]
    start_urls = [
        "http://www.yhd.com/ctg/s2/vc1242/",
    ]
    
    def __init__(self):
        super(YHDMilk_Spider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        #sel = Selector(response)
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        listdata = sel.xpath('//li[@class="search_item"]')
        
        item = Milk()
        for prod in listdata:
            try:
                for sub_prod in prod.xpath('div'):
                    prodsize_attr = sub_prod.xpath('@productsize')
                    if len(prodsize_attr):
                        mul = int(prodsize_attr.extract()[0])
                    else:
                        mul = 1
                    
                    lazyload_attr = sub_prod.xpath('@lazyload_textarea')
                    if len(lazyload_attr) and lazyload_attr.extract()[0] != "":
                        subnode = sub_prod.xpath('textarea')
                        price = subnode.xpath('div[@class="pricebox clearfix"]/span[@class="color_red price"]/text()').extract()[0].strip()[1:]
                        title = subnode.xpath('p[@class="title"]/a/@title').extract()[0]
                        prod_lick = subnode.xpath('p[@class="title"]/a/@href').extract()[0]
                        pic_link = subnode.xpath('a[@class="search_prod_img"]/img/@src').extract()[0]
                        if not pic_link:
                            pic_link_node = sub_prod.xpath('a[@class="search_prod_img"]/img/@original')
                            if pic_link_node:
                                pic_link = pic_link_node.extract()[0]                        
                    else:
                        price = sub_prod.xpath('div[@class="pricebox clearfix"]/span[@class="color_red price"]/text()').extract()[0].strip()[1:]
                        title = sub_prod.xpath('p[@class="title"]/a/@title').extract()[0]
                        prod_lick = sub_prod.xpath('p[@class="title"]/a/@href').extract()[0]
                        pic_link = sub_prod.xpath('a[@class="search_prod_img"]/img/@src').extract()[0]
                        if not pic_link:
                            pic_link_node = sub_prod.xpath('a[@class="search_prod_img"]/img/@original')
                            if pic_link_node:
                                pic_link = pic_link_node.extract()[0]
                    dict = super(YHDMilk_Spider, self).ParseTitleToDict(title)    
                    item["name"] = dict["name"]
                    item["brand"] = dict["brand"]
                    item["segment"] = dict["segment"]
                    item["prod_link"] = prod_lick
                    item["pic_link"] = pic_link
                    item["volume"] = dict["volume"] * mul
                    item["price"] = float(price)
                    item["unitprice"] = item["price"] / item["volume"] * 100.0
                    if item["unitprice"] < 90 and item["unitprice"] > 10:
                        yield item
                    
            except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[yhd_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                log.msg('[yhd_milk] item : %s' % item, log.ERROR)
                
        nextpage_node = sel.xpath(u'//a[@class="page_next"]')
        if len(nextpage_node) == 0:
            return 
        nextpage_link = str(nextpage_node.xpath(u'@href').extract()[0].strip())
        
        yield Request(url=nextpage_link, callback=self.parse)
            
    def __unicode__(self):
        return unicode(self.name)
