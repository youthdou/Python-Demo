from scrapy.spider import Spider
from company_list_pro.items import CompanyItem
from scrapy.http import Request

from faker import Factory
f = Factory.create()

import json

from company_list_pro.spiders.cookies import Cookie
from company_list_pro import settings

cookies = Cookie(settings.COOKIES)


class CompanySpider(Spider):
    name = 'Company'
    allowd_domains = ['gongshang.mingluji.com']
    start_urls = [
        'https://gongshang.mingluji.com/jiangsu/%E7%94%B5%E5%AD%90'
    ]

    headers = {
        'User-Agent': f.user_agent()
    }

    def start_requests(self):
        print(cookies.get())
        print("Existing settings: %s" % self.settings.attributes.keys())
        print(self.headers)

        listRequest = [Request('https://gongshang.mingluji.com/jiangsu/%E7%94%B5%E5%AD%90', headers=self.headers,
                               callback=self.get_company_name)]
        for i in range(1, 21):
            strUrl = 'https://gongshang.mingluji.com/jiangsu/电子?page=%d' % i
            listRequest.append(Request(strUrl, headers=self.headers, callback=self.get_company_name))
        return listRequest

    def get_company_name(self, response):
        print("[%s]%s" % (response.url, response.status))
        #print(response.status)
        #print(response.headers)
        for item in response.xpath("//div[@class='view-content']/div[@class='item-list']/ul/li"):
            #print(item.xpath("span/span/a/text()").extract()[0])
            #companyItem = CompanyItem()
            #companyItem['name'] = item.xpath("span/span/a/text()").extract()[0]
            #yield  companyItem
            strName = item.xpath("span/span/a/text()").extract()[0]
            strUrl = 'https://www.qichacha.com/search?key=' + strName
            yield Request(strUrl, headers=self.headers, cookies=cookies.get(), callback=self.get_company_url)

    def get_company_url(self, response):
        print("[%s]%s" % (response.url, response.status))
        #print(response.body)
        listHref = response.xpath("//table/tbody/tr/td[2]/a/@href").extract()
        if len(listHref) > 0:
            #print(listHref[0])
            strID = listHref[0].lstrip('/firm_')
            strID = strID.rstrip('.html')
            strUrl = "https://www.qichacha.com/tax_view?keyno=%s&ajaxflag=1" % strID
            print(strUrl)
            yield Request(strUrl, headers=self.headers, cookies=cookies.get(), callback=self.get_company_tax)

    def get_company_tax(self, response):
        print("[%s]%s" % (response.url, response.status))
        #print(str(response.body, encoding='gb2312'))
        jsonr = json.loads(response.body)
        #data = jsonr['data']
        #print(type(data))
        #print(data.keys())
        #print(jsonr['data']['Name'])
        item = CompanyItem()
        for key in jsonr['data'].keys():
            item[key] = jsonr['data'][key]
        #print(item)
        yield item
