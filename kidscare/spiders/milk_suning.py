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

class SUNINGMilk_Spider(MilkSpider):
    name = "suning"
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
        pass
        
    
    def __unicode__(self):
        return unicode(self.name)