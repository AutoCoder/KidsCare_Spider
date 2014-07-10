# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Milk(Item):
    # define the fields for your item here like:
    name = Field()
    brand = Field()
    segment = Field()
    price = Field()
    unitprice = Field() # $?/100g
    volume = Field()
    packaging_type = Field() # canning bag
    sale_count = Field() # bi
    comments_count = Field()
    pic_link = Field()
    prod_link = Field()
    pass


class Diaper(Item):
    # define the fields for your item here like:
    # name = Field()
    pass