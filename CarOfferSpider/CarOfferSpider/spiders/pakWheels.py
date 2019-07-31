# -*- coding: utf-8 -*-
import scrapy
# for string to list conversion
import ast
# to use infinity
import math
from time import time

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

import io

# TODO: comments

def pakURLs(keyword):
    prefix = 'https://www.pakwheels.com/used-cars/search/-/?q='

    link_friendly = '+'.join((keyword.split(' ')))

    my_url = prefix + link_friendly

    uClient = uReq(my_url)

    # ofloading the content into a variable
    page_html = uClient.read()

    # closing connection
    uClient.close()

    # makes a soup object of the html page by parsing it
    page_soup = soup(page_html, "html.parser")

    container = page_soup.findAll("li", {"class":"last next"})

    if len(container) == 0:
        return [my_url]

    last_page_link = container[0].a["href"]

    pattern = re.compile("/?page=(.*)&q=")

    last_page = int(pattern.search(last_page_link).group(1))

    all_urls = [my_url + "&page=" + str(i) for i in range(1, last_page + 1)]
    # print(all_urls)

    all_url_string = ' '.join(all_urls)

    return all_urls

class PakwheelsSpiderSpider(scrapy.Spider):
    name = 'pakwheelsSpider'
    allowed_domains = ['www.pakwheels.com']
    # start_urls = ['http://www.pakwheels.com/']
    words=[]
    # words = ['city', '2016']
    start_urls = []

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        words : list (The list of keywords)
        startUrl : str (The url of the page to scrape data from)
        """
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.words = kwargs.get('words')
        # self.start_urls = kwargs.get('startUrl').split(' ')
        # self.words = ['city', '2009']
        urls = pakURLs(self.words)
        for url in urls:
            self.start_urls.append(url)
        # print(self.start_urls)
        super(PakwheelsSpiderSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        with io.open("pk.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        # scrape URLs and Titles
        data = response.xpath('//li[@class="classified-listing  "]/div/div[2]/div[1]/div/div/a')
        # scrape prices
        prices = response.xpath('//li[@class="classified-listing  "]/div/div[2]/div[1]/div/div/div/div')
        # scrape Locations
        locations = response.xpath('//li[@class="classified-listing  "]/div/div[2]/div[2]/div/ul[1]')
        # scrape other data (model, mileage, fuel type, engine, transmission)
        data1 = response.xpath('//li[@class="classified-listing  "]/div/div[2]/div[2]/div/ul[2]')
        # scrape Image URLs
        images = response.xpath('//li[@class="classified-listing  "]/div/div[1]/div[1]/div')

        for i in range(len(data)):
            if (self.filterAd(self.words, self.getTitle(data[i]), self.getPrice(prices[i]))):
                item = {}
                
                # car item
                carItem = {}
                carItem["url"] = self.getUrl(data[i]) # get URL
                carItem["title"] = self.getTitle(data[i]) # get title
                carItem["price"] = self.getPrice(prices[i]) # get price
                carItem["location"] = self.getLocation(locations[i]) # get location
                carItem["model"] = self.getModel(data1[i]) # get model year
                carItem["mileage"] = self.getMileage(data1[i]) # get mileage
                carItem["fuel"] = self.getFuel(data1[i]) # get fuel type
                carItem["engine"] = self.getEngine(data1[i]) # get engine
                carItem["transmission"] = self.getTransmission(data1[i]) # get transmission

                # image item
                imageItem = {}
                imageItem["url"] = ", ".join(self.getImages(images[i])) # get image URLs

                item["carItem"] = carItem
                item["imageItem"] = imageItem
                yield item

                # checking for duplicates
                # if (item not in self.vehicles):
                #     self.vehicles.append(item)
                #     yield item

        # handling pagination
        # next_page_url = response.xpath("//li[@class='next_page']//a/@href").extract_first()
        # if next_page_url:
        #     absolute_next_page_url = response.urljoin(next_page_url)
        #     yield scrapy.Request(absolute_next_page_url)

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
        temp = item.xpath('text()').extract()
        if (len(temp) == 1):
            temp = temp[0]
        else:
            temp = temp[1]

        if ("Call" in temp):
            return 0
            # return math.inf
        else:
            temp = temp.replace(" ", "")
            temp = temp.replace("\n", "")
            # item = item.xpath('meta[1]')
            # return int(item.xpath('@content').extract()[0])
            return int(round(float(temp)))

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

    def filterAd(self, words, title, price):
        """
        Parameters
        ----------
        words : list (The list of keywords)
        title : str (The title of an ad)
        price : int (The price of an ad)

        Returns
        -------
        boolean (a boolean representing if ad is appropriate)
        """
        count = 0
        title = title.lower()

        if not price:
            return False

        for word in words:
            if word.lower() in title:
                count += 1

        if count == len(words):
            return True

        return False