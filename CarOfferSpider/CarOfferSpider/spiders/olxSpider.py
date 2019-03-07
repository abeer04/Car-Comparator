# -*- coding: utf-8 -*-
import scrapy


class OlxspiderSpider(scrapy.Spider):
    name = 'olxSpider'
    allowed_domains = ['olx.com.pk']
    start_urls = ['https://www.olx.com.pk/lahore_g4060673/q-city-2016']

    def parse(self, response):
        links = response.xpath('//li[@class="EIR5N "]/a')
        data = response.xpath('//li[@class="EIR5N "]/a/div')

        items = []
        for i in range(len(links)):
            item = {}
            item["url"] = self.getUrl(links[i])
            item["title"] = self.getTitle(data[i])
            item["price"] = self.getPrice(data[i])
            item["location"] = self.getLocation(data[i])
            item["modelDate"] = self.getModel(data[i])
            item["mileage"] = self.getMileage(data[i])
            # item["fuelType"]
            # item["engine"]
            # item["transmission"]
            item["images"] = self.getImages(links[i])
            items.append(item)
            print(item)

    def getUrl(self, item):
        return self.allowed_domains[0] + item.xpath('@href').extract()[0]

    #Just gets the price in digits and strips off everything else
    def getPrice(self, item):
        try:
            return item.xpath('span[1]/text()').extract()[0].strip('Rs ').replace(',','')
        except:
            return 'Error at Price'

    def getTitle(self, item):
        try:
            return item.xpath('span[3]/text()').extract()[0]
        except:
            return 'Error at Title'

    def getModel(self, item):
        try:
            return item.xpath('span[2]/text()').extract()[0][:4]
        except:
            return 'Error at Model'

    def getMileage(self, item):
        try:
            return item.xpath('span[2]/text()').extract()[0][7:]
        except:
            return 'Error at Mileage'

    def getLocation(self,item):
        try:
            return item.xpath('div/span[1]/text()').extract()[0]
        except:
            return 'Error at Mileage'

    #Error: Images are added using js, need to find some way else to extract their links
    def getImages(self,item):
        try:
            return item.xpath('figure/div[@class="LazyLoad is-visible"]')#.xpath('@src').extract()
        except:
            return 'Error at Images'
