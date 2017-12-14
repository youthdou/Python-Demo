# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class CompanyListProItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CompanyItem(Item):
    Name = Field()
    CreditCode = Field()
    Address = Field()
    PhoneNumber = Field()
    Bank = Field()
    Bankaccount = Field()