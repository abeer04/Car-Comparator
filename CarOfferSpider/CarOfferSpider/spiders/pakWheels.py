# -*- coding: utf-8 -*-
import scrapy


class PakwheelsSpider(scrapy.Spider):
    name = 'pakWheels'
    allowed_domains = ['pakwheels.com']
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/mk_honda/md_city/vr_i-vtec-prosmatec/ct_lahore/']

    def parse(self, response):
        # //*[@id="main_ad_3155615"]/div/div[2]/div[1]/div/div
        data = response.xpath('//div[@class="well search-list clearfix ad-container page-"]/div[2]/div[1]/div/div/a')
        # //*[@id="main_ad_3155615"]/div/div[2]/div[2]/div/ul[2]
        data1 = response.xpath('//div[@class="well search-list clearfix ad-container page-"]/div[2]/div[2]/div/ul[2]')

        items = []

        for i in range(len(data)):
            item = {}
            item["url"] = self.getUrl(data[i])
            item["title"] = self.getTitle(data[i])
            item["modelDate"] = self.getModel(data1[i])
            item["mileage"] = self.getMileage(data1[i])
            item["fuelType"] = self.getFuel(data1[i])
            item["engine"] = self.getEngine(data1[i])
            item["transmission"] = self.getTransmission(data1[i])
            items.append(item)
            # yield item

        print(items)

    def getUrl(self, item):
        return self.allowed_domains[0] + "/" + item.xpath('@href').extract()[0]

    def getTitle(self, item):
        return item.xpath('@title').extract()[0]

    def getModel(self, item):
        return item.xpath('li[1]/text()').extract()[0]

    def getMileage(self, item):
        return item.xpath('li[2]/text()').extract()[0]

    def getFuel(self, item):
        return item.xpath('li[3]/text()').extract()[0]

    def getEngine(self, item):
        return item.xpath('li[4]/text()').extract()[0]

    def getTransmission(self, item):
        return item.xpath('li[5]/text()').extract()[0]

    # def parse(self, response):
    #     print(response.xpath('//ul/li[@itemtype="https://schema.org/Vehicle"][@name=$li]/preceding-sibling::li[1]/meta[@itemprop="name"]/@content').get())

#
# //meta[@itemprop="name"]/@content
#
# //div[@id="images"]/a/text()'


# //meta[2][@itemprop="name"]/@content'
