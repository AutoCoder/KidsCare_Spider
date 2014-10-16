'''
Created on 2014.10.15

@author: HELI
'''
from scrapy.http import Request
from kidscare.items import Milk
from kidscare.spiders.basespider import MilkSpider
from scrapy import log

import json
import sys

class JDMilk_AJAX_Spider(MilkSpider):
    name = "jd_ajax"
    allowed_domains = ["m.jd.com"]
    start_urls = [
        "http://m.jd.com/products/1319-1523-7052-0-0-0-0-0-0-0-1-1-1.html?cid=7052&stock=&resourceType=&resourceValue=&sid=9313e530e292838dd414c53b28893fe3&_format_=json",
    ]
    
    def __init__(self):
        self.pageNum = 1
        super(JDMilk_AJAX_Spider, self).__init__()
    
    def get_next_url(self):
        self.pageNum += 1
        return "http://m.jd.com/products/1319-1523-7052-0-0-0-0-0-0-0-1-1-%d.html?cid=7052&stock=&resourceType=&resourceValue=&sid=9313e530e292838dd414c53b28893fe3&_format_=json" % self.pageNum
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        #sel = Selector(response)
        #sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        root_node = json.loads(response.body_as_unicode())
        
        
        listdata = root_node["wares"]
        
        if len(listdata) == 0:
            return
        
        item = Milk()
        for prod in listdata:
            try:
                title = prod["wname"]
                prod_id = prod["wareId"]
                item["price"] = float(prod["jdPrice"])
                item["pic_link"] = prod["imageurl"]
                item["prod_link"] = "http://m.jd.com/product/%s.html" % prod_id
                dict = super(JDMilk_AJAX_Spider, self).ParseTitleToDict(title)
                item["name"] = dict["name"]
                item["brand"] = dict["brand"]
                item["segment"] = dict["segment"]
                item["volume"] = dict["volume"]
                item["unitprice"] = item["price"] / dict["volume"] * 100.0
                if item["unitprice"] < 90 and item["unitprice"] > 10:
                    yield item
                
            except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[jd_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg('[jd_milk] item : %s' % item, log.ERROR)
                

        yield Request(url=self.get_next_url(), callback=self.parse)
            
    def __unicode__(self):
        return unicode(self.name)