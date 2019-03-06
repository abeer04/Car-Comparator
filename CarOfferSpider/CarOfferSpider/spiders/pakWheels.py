# -*- coding: utf-8 -*-
import scrapy
# for string to list conversion
import ast

# TODO: check keyword in Title

class PakwheelsSpiderSpider(scrapy.Spider):
    name = 'pakwheels_spider'
    allowed_domains = ['www.pakwheels.com']
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/?q=city+2016']

    def parse(self, response):
        # scrape URLs and Titles
        data = response.xpath('//div[@class="well search-list clearfix ad-container page-"]/div[2]/div[1]/div/div/a')
        # scrape prices
        prices = response.xpath('//div[@class="well search-list clearfix ad-container page-"]/div[2]/div[1]/div/div/div/div')
        # scrape Locations
        locations = response.xpath('//div[@class="well search-list clearfix ad-container page-"]/div[2]/div[2]/div/ul[1]')
        # scrape other data (model, mileage, fuel type, engine, transmission)
        data1 = response.xpath('//div[@class="well search-list clearfix ad-container page-"]/div[2]/div[2]/div/ul[2]')
        # scarpe Image URLs
        images = response.xpath('//div[@class="well search-list clearfix ad-container page-"]/div[1]/div[1]/div')

        # list of dictionaries each representing a vehicle
        items = []

        for i in range(len(data)):
            item = {}
            item["url"] = self.getUrl(data[i]) # get URL
            item["title"] = self.getTitle(data[i]) # get title
            item["price"] = self.getPrice(prices[i]) # get price
            item["location"] = self.getLocation(locations[i]) # get location
            item["modelDate"] = self.getModel(data1[i]) # get model year
            item["mileage"] = self.getMileage(data1[i]) # get mileage
            item["fuelType"] = self.getFuel(data1[i]) # get fuel type
            item["engine"] = self.getEngine(data1[i]) # get engine
            item["transmission"] = self.getTransmission(data1[i]) # get transmission
            item["images"] = self.getImages(images[i]) # get image URLs
            items.append(item)
            # yield item

        # print(items)

        # write data in a file to view the data scraped
        with open('file.txt', 'w') as f:
            for item in items:
                f.write("%s\n" % item)

    def getUrl(self, item):
        # concatenating domain name with the path of the ad
        return self.allowed_domains[0] + "/" + item.xpath('@href').extract()[0]

    def getTitle(self, item):
        return item.xpath('@title').extract()[0]

    def getPrice(self, item):
        # if there is Call in the string, then return Call for Price, else return Price
        temp = item.xpath('text()').extract()[0]
        
        if ("Call" in temp):
            return "Call for Price"
        else:
            item = item.xpath('meta[1]')
            return item.xpath('@content').extract()[0]

    def getLocation(self, item):
        # strip whitespace and newline
        location = item.xpath('li/text()').extract()[0]
        location = location.replace(" ", "")
        location = location.replace("\n", "")
        return location

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

    def getImages(self, item):
        divClass = item.xpath('@class').extract()

        # final list of images
        images = []

        if (divClass):
            return images
        else:
            item = item.xpath('ul')
            lst = item.xpath('@data-galleryinfo').extract()[0]
            # convert string representing a list to an actual list
            lst = ast.literal_eval(lst)

            for i in range(len(lst)):
                # scrapping image urls
                images.append(lst[i]["src"])

            return images
