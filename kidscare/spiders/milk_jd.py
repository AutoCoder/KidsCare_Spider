'''
Created on 2014.6.12

@author: HELI
'''
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import DropItem
#from spiderutility import SpiderUtility
from kidscare.items import Milk
from kidscare.spiders.basespider import MilkSpider
from scrapy import log

import sys

class JDMilk_Spider(MilkSpider):
    name = "jd"
    allowed_domains = ["m.jd.com"]
    start_urls = [
        "http://m.jd.com/products/1319-1523-7052.html",
    ]
    
    def __init__(self):
        super(JDMilk_Spider, self).__init__()
    
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
                title = prod.xpath('div[@class="title"]/a/text()').extract()[0].strip()
                prod_link = "http://" + self.allowed_domains[0] + prod.xpath('div[@class="title"]/a/@href').extract()[0].strip()
                pic_link = prod.xpath('div[@class="pic"]/a/img/@src').extract()[0].strip()
                price = prod.xpath('div[@class="price"]/font/text()').extract()[0].strip()[1:]
                item["price"] = float(price)
                item["pic_link"] = str(pic_link)
                item["prod_link"] = str(prod_link)
                dict = super(JDMilk_Spider, self).ParseTitleToDict(title)
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
                
        nextpage_node = sel.xpath(u'//div[@class="page"]/a[text()[contains(., "\u4e0b\u4e00\u9875")]]')
        if len(nextpage_node) == 0:
            return 
        nextpage_link = "http://" + self.allowed_domains[0] + str(nextpage_node.xpath(u'@href').extract()[0].strip())
        
        yield Request(url=nextpage_link, callback=self.parse)
            
    def __unicode__(self):
        return unicode(self.name)