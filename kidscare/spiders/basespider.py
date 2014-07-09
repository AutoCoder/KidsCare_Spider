'''
Created on 2014.6.30

@author: HELI
'''

from scrapy.spider import Spider
from scrapy import log
from datetime import date


class MilkSpider(Spider):
	def __init__(self):
		log.start('E:/OpenSource/Spider_praitise/KidsCare_Spider/ScrapyHistory/%s/%s.log' % (self.name, str(date.today())), loglevel=log.INFO, logstdout=False)
		
	
