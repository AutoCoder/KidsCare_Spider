'''
Created on 2014.6.30

@author: HELI
'''

from scrapy.spider import Spider
from scrapy import log
from datetime import date
import json
import os
import re

configdir = os.path.dirname(os.path.dirname(__file__)) + "\conf"
mappingnum = {u"\u4e00" : '1', u"\u4e8c" : '2', u"\u4e09": '3', u"\u56db": '4', u"\u4e94": '5', u"\u516d": '6', u"\u4e03": '7', u"\u516b": '8', u"\u4e5d": '9', u"\u5341": '1'}	

class MilkSpider(Spider):
	def __init__(self):
		log.start('E:\OpenSource\Spider_praitise\KidsCare_Spider\ScrapyHistory\%s\%s.log' % (self.name, str(date.today())), loglevel=log.INFO, logstdout=False)		
		configfile = open(configdir + "\dataconfig",'r')
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
		
	def __extractChineseNum(self, title, indexfrom, direction=True):
		"""
		Extract the ChineseNum in title, like "shierhe" 
		if direction=True will return the before number {1200}
		else return after number {3}
		"""
		str = u""
		if direction: 
			if indexfrom != 0:		  
				indexfrom -= 1
				while True:
					if indexfrom >= 0 and title[indexfrom] in mappingnum.keys():
						str = title[indexfrom] + str
						indexfrom -= 1
					else:
						break
		else:
			if indexfrom < len(title)-1:
				indexfrom += 1
				while True:
					if indexfrom < len(title) and title[indexfrom] in mappingnum.keys():
						str += title[indexfrom]
						indexfrom += 1
					else:
						break
		
		return self.__convertChinese(str)


	def __convertChinese(self, chinese):
		"""
			only for number from 1~100, the input argument must be chinese digit
		"""
		lens = len(chinese)
		if lens == 0:
			return ""
		elif lens == 1:
			return mappingnum[chinese]
		elif lens == 2:
			return mappingnum[chinese[0]] + mappingnum[chinese[1]]
		elif lens == 3:
			return mappingnum[chinese[0]] + mappingnum[chinese[2]]
		else:
			raise ValueError("convertChinese function is only available for 1 ~ 100")	
		
	def __regexNum(self, title):
		m = re.match(ur".*?(\d+)[gG\u514b]", title)
		if m:
			return m.group(1)
		else: 
			return ""
						
	def ParseTitleToDict(self, title): #return {brand, name, volume, segment}
		"""
		This function is to parse the unnormalized title to  {brand, name, volume, segment}
		"""
		title = title.lower()
		dict = {}
		try:
			i_duan = title.find(u"\u6bb5")
			segment = ''
			if i_duan is not -1 :
				segment = self.__extractNum(title, i_duan)
				if not segment.isdigit():
					segment = self.__extractChineseNum(title, i_duan)
					
			if not segment.isdigit():
				i_jie = title.find(u"\u9636")
				if i_jie is not -1 :
					segment = self.__extractNum(title, i_jie)
					if not segment.isdigit():
						segment = self.__extractChineseNum(title, i_jie)	
										
			dict["segment"] = int(segment)
			
			volume = int( self.__regexNum(title) )  
						
			i_mul = title.find(u"g*") 
			if i_mul is -1:
				i_mul = title.find(u"\u514b*")
			if i_mul is not -1:
				volume = int(self.__extractNum(title, i_mul, True)) * int(self.__extractNum(title, i_mul+1, False))
			
			if i_mul is -1:
				i_mul = title.find(u"\u76d2")
				if i_mul != -1:
					mul = self.__extractChineseNum(title, i_mul, True) + self.__extractNum(title, i_mul, True)
					if mul.isdigit():
						volume *=  int(mul)

			dict["volume"] = volume
			
			brandlist = self.milktree.keys()
			
			found = False
			for brand in brandlist:
				if title.find(brand) is not -1:
					dict["brand"] = brand
					found = True
					break
			if not found:
				log.msg('[milk] parse brand failed', log.ERROR)
				raise IndexError
			
			namelist = self.milktree[dict["brand"]].keys()
			found = False
			for name in namelist:
				if title.find(name.lower()) is not -1:
					dict["name"] = self.milktree[dict["brand"]][name]
					found = True
					break
			if not found:
				log.msg('[milk] parse name failed', log.ERROR)
				raise IndexError
			
		except Exception, info: 
			log.msg('[milk] parse title:"%s" error:"%s"' % (title, info), log.ERROR)
			return {}  
		
		return dict
