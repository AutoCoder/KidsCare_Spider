

'''
Created on 2014.6.12

@author: HELI
'''
from scrapy.selector import Selector
from scrapy.http import Request
from kidscare.items import Milk
from kidscare.spiders.basespider import MilkSpider
from scrapy import log

import sys

class TmallMilk_Spider(MilkSpider):
    name = "tmall"
    allowed_domains = ["list.tmall.com"]
    start_urls = [
        "http://list.tmall.com/search_product.htm?cat=51234037",
    ]
    
    def __init__(self):
        super(TmallMilk_Spider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the travel_product_page's link to extract
        @url http://dujia.qunar.com/tejia
        @scrapes name
        """
        #sel = Selector(response)
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        listdata = sel.xpath('//div[@class="product"]')
        
        item = Milk()
        for prod in listdata:
            try:
                node = prod.xpath('div[@class="product-iWrap"]')
                title = node.xpath('p[@class="productTitle"]/a/text()').extract()[0].strip()
                prod_link = "http:"+ node.xpath('p[@class="productTitle"]/a/@href').extract()[0].strip()
                pic_link_node = node.xpath('div[@class="productImg-wrap"]/a[@class="productImg"]/img/@src')
                if len(pic_link_node) == 0:
                    pic_link_node = node.xpath('div[@class="productImg-wrap"]/a[@class="productImg"]/img/@data-ks-lazyload')
                pic_link = pic_link_node.extract()[0].strip()
                price_node = node.xpath('p[@class="productPrice"]')
                price = price_node.xpath('em/@title').extract()[0].strip()
                price_ave_node = price_node.xpath('span[@class="productPrice-ave"]/text()')
                if len(price_ave_node) == 0:
                    continue
                else:
                    price_ave = price_ave_node.extract()[0].split(u"\u5143")[0]
                item["price"] = float(price)
                item["pic_link"] = str(pic_link)
                item["prod_link"] = str(prod_link)
                item["unitprice"] = float(price_ave) / 5.0
                item["volume"] = int( item["price"] / item["unitprice"] * 100)
                dict = super(TmallMilk_Spider, self).ParseTitleToDict(title)
                item["name"] = dict["name"]
                item["brand"] = dict["brand"]
                item["segment"] = dict["segment"]
                if item["unitprice"] < 90 and item["unitprice"] > 10:
                    yield item
                
            except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[tmall_milk] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                log.msg('[tmall_milk] item : %s' % item, log.ERROR)
                
        nextpage_node = sel.xpath(u'//a[@class="ui-page-next"]')
        if len(nextpage_node) == 0:
            return 
        nextpage_link = "http://list.tmall.com/search_product.htm" + str(nextpage_node.xpath(u'@href').extract()[0].strip())
        
        yield Request(url=nextpage_link, callback=self.parse)
            
    def __unicode__(self):
        return unicode(self.name)