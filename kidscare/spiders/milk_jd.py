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
    #allowed_domains = ["http://www.qunar.com/"]
    start_urls = [
        "http://dujia.qunar.com/tejia",
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
        listdata = sel.xpath('//div[@id="jptj"]/div')
        
        for ticket in listdata:
            try:
                detail_url = ticket.xpath('div[@class="cont"]/dl/dt/a/@href').extract()[0]
                yield Request(detail_url, callback=self.parse_ticket)
                
            except Exception, info: #IndexError
                s=sys.exc_info()             
                log.msg('[qunar] detail_url : %s' % detail_url, log.ERROR)
                log.msg("[qunar] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                log.msg('[qunar] Ticket : %s' % ticket, log.ERROR)
        
    
    def parse_ticket(self, response):
        """
        This Function parse the travel_product_page to items
        """
        item = Milk()
        try:     
            for key, value in item.get_default_item_dict().iteritems():
                item[key] = value
 
        except Exception, info: #IndexError
            s=sys.exc_info()
            log.msg('[qunar] item : %s' % item, log.ERROR)
            log.msg("[qunar] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
            
        return item
    
    def __unicode__(self):
        return unicode(self.name)