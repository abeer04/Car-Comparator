# -*- coding: utf-8 -*-
import scrapy
# for string to list conversion
import ast
# to use infinity
import math

# TODO: comments

class PakwheelsSpiderSpider(scrapy.Spider):
    name = 'pakwheelsSpider'
    allowed_domains = ['www.pakwheels.com']
    vehicles = [] # list of dictionaries each representing a vehicle

    def __init__(self, words, startUrl, *args, **kwargs):
        """
        Parameters
        ----------
        words : list (The list of keywords)
        startUrl : str (The url of the page to scrape data from)
        """
        super(PakwheelsSpiderSpider, self).__init__(*args, **kwargs)
        self.words = words
        self.start_urls = [startUrl]

    def parse(self, response):
        # scrape URLs and Titles // div[@class="well search-list clearfix ad-container page-"]
        data = response.xpath('//li[@itemtype="https://schema.org/Vehicle"]/div/div[2]/div[1]/div/div/a')
        # scrape prices
        prices = response.xpath('//li[@itemtype="https://schema.org/Vehicle"]/div/div[2]/div[1]/div/div/div/div')
        # scrape Locations
        locations = response.xpath('//li[@itemtype="https://schema.org/Vehicle"]/div/div[2]/div[2]/div/ul[1]')
        # scrape other data (model, mileage, fuel type, engine, transmission)
        data1 = response.xpath('//li[@itemtype="https://schema.org/Vehicle"]/div/div[2]/div[2]/div/ul[2]')
        # scarpe Image URLs
        images = response.xpath('//li[@itemtype="https://schema.org/Vehicle"]/div/div[1]/div[1]/div')

        for i in range(len(data)):
            if (self.filterAd(self.words, self.getTitle(data[i]))):
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

                if (item not in self.vehicles):
                    self.vehicles.append(item)
                    yield item

        # handling pagination
        next_page_url = response.xpath("//li[@class='next_page']//a/@href").extract_first()
        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url)

    # def closed(self, reason):
    #     # will be called when the crawler process ends

    #     # write data in a file to view the data scraped
    #     with open('file.txt', 'a+') as f:
    #         for item in self.vehicles:
    #             f.write("%s\n" % item)

    #     sortedItems = sorted(self.vehicles, key = lambda i: (i["price"], i["mileage"], -i["modelDate"]))

    #     # write sorted data in a file to view the data scraped
    #     with open('sortedFile.txt', 'a+') as f:
    #         for item in sortedItems:
    #             f.write("%s\n" % item)

    def getUrl(self, item):
        # concatenating domain name with the path of the ad
        return self.allowed_domains[0] + item.xpath('@href').extract()[0]

    def getTitle(self, item):
        return item.xpath('@title').extract()[0]

    def getPrice(self, item):
        # if there is Call in the string, then return Call for Price, else return Price
        temp = item.xpath('text()').extract()[0]

        if ("Call" in temp):
            return math.inf
        else:
            item = item.xpath('meta[1]')
            return int(item.xpath('@content').extract()[0])

    def getLocation(self, item):
        # strip whitespace and newline
        location = item.xpath('li/text()').extract()[0]
        location = location.replace(" ", "")
        location = location.replace("\n", "")
        return location

    def getModel(self, item):
        return int(item.xpath('li[1]/text()').extract()[0])

    def getMileage(self, item):
        temp = item.xpath('li[2]/text()').extract()[0]
        temp = temp.replace(",", "")
        temp = temp.replace(" ", "")
        temp = temp.replace("km", "")
        return int(temp)

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

    def filterAd(self, words, title):
        """
        Parameters
        ----------
        words : list (The list of keywords)
        title : str (The title of an ad)

        Returns
        -------
        boolean (a boolean representing if all keywords are in ad title)
        """
        count = 0
        title = title.lower()

        for word in words:
            if word.lower() in title:
                count += 1

        if count == len(words):
            return True

        return False