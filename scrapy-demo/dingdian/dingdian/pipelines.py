# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DingdianPipeline(object):
    def print_item(self, item):
        for field in item.fields:
            print('[%s]%s' % (field, item[field]))

    def process_item(self, item, spider):
        self.print_item(item)
        return item
