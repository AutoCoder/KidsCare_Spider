# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from spiders.basespider import MilkSpider, PytesserDir, ImageDir
from pytesser.pytesser import Image, image_to_string
from settings import RunInCloud
from scrapy.exceptions import DropItem
from scrapy import log
import MySQLdb
import urllib2
import os
import shutil
import platform
milk_website = ('tmall','jd','yhd','suning','weiwei','sfbest')

DbHost = None
if RunInCloud:
    DbHost = 'alikidscare.mysql.rds.aliyuncs.com'
else:
    if platform.system() is 'Windows':
        DbHost = '127.0.0.1'
    elif platform.system() in ('Linux',):
        DbHost = '10.31.186.63'
    else:
        DbHost = '10.31.186.63'

class KidscarePreprocessPipeline(object):
    """
        if there are no database created, this pipeline will create the database
    """
    def process_item(self, item, spider):
        return item
    
    def open_spider(self, spider):
        try:
            self.conn=MySQLdb.connect(host=DbHost, user='spider',passwd='wodemima',port=3306, charset='utf8')
            cur=self.conn.cursor()
            cur.execute('create database if not exists Mom_Baby') 
            self.conn.commit()    
                 
        except MySQLdb.Error,e:
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]), log.ERROR)
              
    
class ImagePriceExtractPipeline(object):
    """
    this pipeline will extract the price from img link
    """
    def open_spider(self, spider):
        os.chdir(PytesserDir)
        
    def close_spider(self, spider):
        shutil.rmtree(ImageDir)
        os.mkdir(ImageDir)
        
    def __ImagePriceExtract(self, file):
        try:
            img = Image.open(file)
            r,g,b,a = img.split()
            img = Image.merge('RGB',(r,g,b))
            text = image_to_string(img)
            text = text.replace(" ",'').replace('\n','').replace('\r','')
            return float(text)
        except Exception,e:
            raise DropItem("item price can't not extracted successfully: %s" % e)
    
    def process_item(self, item, spider):
        if spider.name is "suning":
            item["price"] = self.__ImagePriceExtract(item["price"])
            item["unitprice"] = item["price"] / item["volume"] * 100
            if item["unitprice"] > 90 or item["unitprice"] < 10:
                raise DropItem("item price is not reasonable!" )
            else:
                return item#create the table of milk_prod
        else:
            return item      
        
class MilkProdStoreDbPipeline(object):
    def __init__(self):
        self.conn = None
            
    def open_spider(self, spider):
        try:
            self.conn=MySQLdb.connect(host=DbHost, user='spider',passwd='wodemima',port=3306, charset='utf8')
            self.conn.select_db('Mom_Baby')
            cur=self.conn.cursor()
            sql = """CREATE TABLE IF NOT EXISTS %s (Id INT PRIMARY KEY AUTO_INCREMENT,
                                                     tunnel varchar(20), 
                                                     brand TEXT, 
                                                     name TEXT, 
                                                     segment INT, 
                                                     price FLOAT, 
                                                     unitprice FLOAT, 
                                                     volume FLOAT, 
                                                     packaging_type ENUM("jar","box","suitcase") DEFAULT "jar",
                                                     pic_link TEXT, 
                                                     prod_link TEXT,
                                                     scrapy_time TIMESTAMP NOT NULL DEFAULT NOW())""" % "Milk_Prod"
            cur.execute(sql)           
        except MySQLdb.Error,e:
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]), log.ERROR)
    
    def process_item(self, item, spider):
        if not issubclass(type(spider), MilkSpider):
            return item#create the table of milk_prod
        
        if self.conn:
            cur = self.conn.cursor()

            #part = u"""INSERT INTO 123 ( title ) VALUES ("%s") """ % item["title"]
            #print part
            item["packaging_type"] = 'jar'
            insert_sql = u"""INSERT INTO Milk_Prod (tunnel,
                                                         brand,
                                                         name, 
                                                         segment, 
                                                         price, 
                                                         unitprice, 
                                                         volume, 
                                                         packaging_type, 
                                                         pic_link, 
                                                         prod_link) VALUES ("%s", "%s", "%s", %d, %f, %f, %f, "%s", "%s", "%s")
            """ % (spider.name, item["brand"], item["name"], item["segment"], item["price"], item["unitprice"], item["volume"], item["packaging_type"]\
                , (item["pic_link"]), item["prod_link"])
            
            cur.execute(insert_sql)
            self.conn.commit()#print insert_sql
            return item
        else:
            return item        
          
        return item     
     
    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
