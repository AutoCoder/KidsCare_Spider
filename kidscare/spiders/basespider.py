'''
Created on 2014.6.30

@author: HELI
'''

from scrapy.spider import Spider
from scrapy import log
from datetime import date
import json
import os

configdir = os.path.dirname(os.path.dirname(__file__)) + "\conf"

class MilkSpider(Spider):
	def __init__(self):
		log.start('E:\OpenSource\Spider_praitise\KidsCare_Spider\ScrapyHistory\%s\%s.log' % (self.name, str(date.today())), loglevel=log.INFO, logstdout=False)		
		configfile = open(configdir + "\dataconfig.json",'r')
		configdict = json.load(configfile, encoding='utf-8')
		self.milktree = configdict[u"MilkBrandTree"]
		
	def __extractNum(self, title, indexfrom, direction=True):
		"""
		Extract the num in title, like "1200g*3" 
		if direction=True will return the before number {1200}
		else return after number {3}
	"""

		if direction:
			temp = indexfrom
			while indexfrom!=0:
				if title[indexfrom-1].isdigit():
					indexfrom -= 1
				else:
					break
			return title[indexfrom:temp]
		else:
			indexfrom += 1
			temp = indexfrom
			while indexfrom!=len(title):
				if title[indexfrom].isdigit():
					indexfrom += 1
				else:
					break
			return title[temp:indexfrom]
		
	def ParseTitleToDict(self, title): #return {brand, name, volume, segment}
		dict = {}
		try:
			i_duan = title.find(u"\u6bb5")
			if i_duan != -1 :
				dict["segment"] = int(self.__extractNum(title, i_duan))
				
			i_ke = title.find(u"\u514b") # find ke
			if i_ke != -1:
				volume = int(self.__extractNum(title, i_ke))
			else:	
				i_g = title.find(u"g") # find ke
				if i_g != -1:
					volume = int(self.__extractNum(title, i_g))
				else:
					i_G = title.find(u"G") # find ke
					if i_G != -1:
						volume = int(self.__extractNum(title, i_G))
						
			i_mul = title.find(u"g*")
			if i_mul != -1:
				volume = int(self.__extractNum(title, i_mul, True)) * int(self.__extractNum(title, i_mul+1, False))

			dict["volume"] = volume
			
			brandlist = self.milktree.keys()
			
			found = False
			for brand in brandlist:
				if title.find(brand) != -1:
					dict["brand"] = brand
					found = True
					break
			if not found:
				log.msg('[jd_milk] parse brand failed', log.ERROR)
				raise IndexError
			
			namelist = self.milktree[dict["brand"]].keys()
			found = False
			for name in namelist:
				if title.find(name) != -1:
					dict["name"] = name
					found = True
					break
			if not found:
				log.msg('[jd_milk] parse name failed', log.ERROR)
				raise IndexError
			
		except Exception, info: 
			log.msg('[jd_milk] parse title:"%s" error:"%s"' % (title, info), log.ERROR)
			return {}  
		
		return dict