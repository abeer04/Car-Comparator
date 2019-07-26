# -*- coding: utf-8 -*-
# import sys
# sys.path.insert(0, '/demoCode/TestComparator/DjangoTestTheodo/CarComparator/CarOfferSpider')
import scrapy
from bs4 import BeautifulSoup as bs4
import time
import json

class OlxspiderSpider(scrapy.Spider):
    name = 'olxSpider'
    allowed_domains = ['www.olx.com.pk']
    start_urls = []
    items = []
    otherInfo = []
    start = time.time()

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        words : list (The list of keywords)
        startUrl : str (The url of the page to scrape data from)
        """
        super(OlxspiderSpider, self).__init__(*args, **kwargs)
        # self.words = words
        # self.start_urls = [startUrl]
        self.words = kwargs.get('words')
        self.start_urls.append(kwargs.get('startUrl'))

    def parse(self, response):
        i = 1
        while i<=5:
            link = "https://www.olx.com.pk/api/relevance/search?facet_limit=100&location=4060673&location_facet_limit=6&page="+str(i)+"&query="+self.queryGen()+"&user=168fc2589a5x19e7ca7f"
            request = scrapy.Request(link, callback=self.parser)
            i+=1
            yield request

    def parser(self,response):
        soup = bs4(response.text,'lxml')
        soup = soup.__repr__()
        soup = soup.replace('<html><body><p>','')
        soup = soup.replace('</p></body></html>','')
        response_json = json.loads(soup)
        json_data = response_json['data']
        for i in range(len(json_data)):
            if (self.filterAd(self.words,json_data[i])):
                item = {}

                #car item
                carItem = {}
                carItem["url"] = self.getUrl(json_data[i])
                # carItem["keywords"] = ' '.join(word for word in self.words)
                carItem["title"] = json_data[i]['title']
                carItem["price"] = self.getPrice(json_data[i])
                carItem["location"] = json_data[i]['locations_resolved']['ADMIN_LEVEL_3_name']
                carItem["model"] = self.getModel(json_data[i])
                carItem["mileage"] = self.getMileage(json_data[i])
                # carItem["source"] = 'olx.com.pk'
                carItem["fuel"] = self.getFuel(json_data[i])
                # self.items.append(item)
                carItem["engine"] = 'NA'
                carItem["transmission"] = 'NA'
                
                #image item
                imageItem = {}
                imageItem["url"] = self.getImages(json_data[i]["images"])# get image URLs

                item["carItem"] = carItem
                item["imageItem"] = imageItem

                # print(item)
                yield item

    def getUrl(self, item):
        relative_url = item['title'].replace('/','')+' '+'iid'+' '+item['id']
        relative_url = relative_url.replace(' ', '-')
        return self.allowed_domains[0]+'/item/'+relative_url

    def getModel(self, item):
        rtVal = "NA"
        for model in filter(lambda y: y['key']=='year',item['parameters']):
            rtVal = int(model['value'])
        return rtVal

    def getMileage(self, item):
        rtVal = "NA"
        for mileage in filter(lambda y: y['key']=='mileage',item['parameters']):
            rtVal = int(mileage['value'])
        return rtVal

    def getFuel(self, item):
        rtVal = "NA"
        for fuel in filter(lambda y: y['key']=='petrol',item['parameters']):
            rtVal = fuel['value']
        return rtVal

    def getRegCity(self, item):
        rtVal = "NA"
        for city in filter(lambda y: y['key']=='registeration_city',item['parameters']):
            rtVal = city['value']
        return rtVal

    def getImages(self, item):
        listOfImages = []
        for image_dict in item:
            listOfImages.append(image_dict["full"]["url"])
        retStr = ", ".join(listOfImages)
        return retStr
        
    def getPrice(self,item):
        try:
            rtVal = int(item['price']['value']['raw'])
            return rtVal
        except:
            return "NA"

    def filterAd(self, words, item):
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
        title = item['title'].lower()

        for word in words:
            if word.lower() in title:
                count += 1

        if count == len(words):
            if self.getPrice(item)!="NA":
                if self.getMileage(item)!="NA":
                    if self.getModel(item)!="NA":
                        return True
        return False

    def queryGen(self):
        rtVal = ''
        listOfWords = self.words.split(' ')
        for i in range(len(listOfWords)):
            if i==0:
                rtVal += listOfWords[i]
            else:
                rtVal += "-"+listOfWords[i]
        return rtVal