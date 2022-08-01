# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MajeClearItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class prodFrToCn(scrapy.Item):
    prodSku = scrapy.Field()
    frWord = scrapy.Field()
    cnTrans = scrapy.Field()
    frName = scrapy.Field()
    cnName = scrapy.Field()
    marque = scrapy.Field()
    mainsite = scrapy.Field()
    fromWhere = scrapy.Field()
    whetherTrans = scrapy.Field()
    category = scrapy.Field()

class dict(scrapy.Item):
    wordFr = scrapy.Field()
    wordCn = scrapy.Field()