# -*- coding: utf-8 -*-
import scrapy
import re



class GarispiderSpider(scrapy.Spider):
    name = 'gariSpider'
    allowed_domains = ['www.gari.pk']
    start_urls = ['http://www.gari.pk/used-cars/honda/city']

    def parse(self, response):
        # scrape URLs
        URLs = response.xpath('//div[@id="cat-contents"]/div[2]/div[1]/a')
        # scrape Title
        titles = response.xpath('//div[@id="cat-contents"]/div[2]/div[1]/a/h3/span')
        # scrape prices
        prices = response.xpath('//div[@id="cat-contents"]/div[2]/div[2]/div[4]')
        # scrape Locations
        locations = response.xpath('//div[@id="cat-contents"]/div[2]/div[2]/div[2]')
        # scrape mileage
        mileage = response.xpath('//div[@id="cat-contents"]/div[2]/div[2]/div[3]')
        # scrape Model
        model = response.xpath('//div[@id="cat-contents"]/div[2]/div[2]/div[1]')
        # scrape fuel type
        fuel_type = response.xpath('//div[@id="cat-contents"]/div[2]/div[2]/div[5]')
        #scrape engine
        engine = response.xpath('//div[@id="cat-contents"]/div[2]/div[2]/div[6]')
        # scrape transmission
        transmission = response.xpath('//div[@id="cat-contents"]/div[2]/div[2]/div[7]')
        # scarpe Image URLs
        images = response.xpath('//div[@id="cat-contents"]/div[1]/span[1]/a[1]/img')

        # list of dictionaries each representing a vehicle
        items = []

        for i in range(len(URLs)):
            item = {}
            item["url"] = self.getUrl(URLs[i]) # get URL
            item["title"] = self.getTitle(titles[i]) # get title
            item["price"] = self.getPrice(prices[i]) # get price
            item["location"] = self.getLocation(locations[i]) # get location
            item["modelDate"] = self.getModel(model[i]) # get model year
            item["mileage"] = self.getMileage(mileage[i]) # get mileage
            item["fuelType"] = self.getFuel(fuel_type[i]) # get fuel type
            item["engine"] = self.getEngine(engine[i]) # get engine
            item["transmission"] = self.getTransmission(transmission[i]) # get transmission
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
        return self.allowed_domains[0] + item.xpath('@href').extract()[0]

    def getTitle(self, item):
        return item.xpath('text()').extract()[0]

    def getPrice(self, item):
        try:
            temp = item.xpath('text()').extract()[0]
            temp = temp.replace(" ", "")
            temp = temp.replace("\n", "")
            temp = temp.replace("Rs", "")
            temp = temp.replace("Lacs", "")
            temp = int(temp)*100000

            return temp
        except:
            return "Error at price"

        # if ("Call" in temp):
        #     return "Call for Price"
        # else:
        #     item = item.xpath('meta[1]')
        #     return item.xpath('@content').extract()[0]

    def getLocation(self, item):
        # strip whitespace and newline
        location = item.xpath('text()').extract()[0]

        return location

    def getModel(self, item):
        return int(item.xpath('text()').extract()[0])

    def getMileage(self, item):
        temp= item.xpath('text()').extract()[0]
        temp = int(temp.replace(" km",""))
        return temp

    def getFuel(self, item):
        return item.xpath('text()').extract()[0]

    def getEngine(self, item):
        return item.xpath('text()').extract()[0]

    def getTransmission(self, item):
        try:
            temp = item.xpath('text()').extract()[0]
            temp = temp.replace(" ", "")
            temp = temp.replace("\n", "")
            return temp
        except:
            return "Error at price"

    def getImages(self, item):
        return item.xpath('@src').extract()

        # final list of images
        # images = []
        #
        # # if (divClass):
        # #     return images
        # # else:
        # #     item = item.xpath('ul')
        # #     lst = item.xpath('@data-galleryinfo').extract()[0]
        # #     # convert string representing a list to an actual list
        # #     lst = ast.literal_eval(lst)
        # #
        # #     for i in range(len(lst)):
        # #         # scrapping image urls
        # #         images.append(lst[i]["src"])
        #
        #     return images
