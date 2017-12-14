# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import csv

class CompanyListProPipeline(object):
    def open_spider(self, spider):
        strFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.csv'
        #self.f = open(strFileName, "w", encoding='utf8', newline='')
        self.f = open(strFileName, "w", encoding='gb2312', newline='')
        self.csvWriter = csv.writer(self.f, delimiter=',')
        #self.titles = ['Name', 'Bankaccount', 'PhoneNumber', 'Address']
        self.titles = ['Name', 'Bankaccount']
        self.csvWriter.writerow(self.titles)

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        row= []
        for title in self.titles:
            value = item[title]
            if value is None:
                return item
            if value.strip() == '':
                return item
            row.append(item[title])
        #self.f.write(str(item['name']) + '\n')
        self.csvWriter.writerow(row)
        return item
