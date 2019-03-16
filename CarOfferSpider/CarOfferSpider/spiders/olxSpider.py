# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs4
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from urllib.request import urlopen as uReq
import time

class OlxspiderSpider(scrapy.Spider):
    name = 'olxSpider'
    allowed_domains = ['www.olx.com.pk']
    start_urls = []
    items = []
    otherInfo = []
    start = time.time()

    def __init__(self, words, startUrl, *args, **kwargs):
        """
        Parameters
        ----------
        words : list (The list of keywords)
        startUrl : str (The url of the page to scrape data from)
        """
        super(OlxspiderSpider, self).__init__(*args, **kwargs)
        self.words = words
        self.start_urls = [startUrl]

    def parse(self, response):
        links = response.xpath('//li[@class="EIR5N "]/a')
        data = response.xpath('//li[@class="EIR5N "]/a/div')

        start = time.time()
        for i in range(len(links)):
            if (self.filterAd(self.words, self.getTitle(data[i]))):
                item = {}
                item["url"] = self.getUrl(links[i])
                item["title"] = self.getTitle(data[i])
                item["price"] = self.getPrice(data[i])
                item["location"] = self.getLocation(data[i])
                item["modelDate"] = self.getModel(data[i])
                item["mileage"] = self.getMileage(data[i])
                item["from"] = 'olx.com.pk'
                # item["other"] = response.follow(links[i], callback=self.getOther)
                # item.update(self.getFuelRegImage(item["url"]))
                # item["fuelType"]
                # item["engine"]
                # item["transmission"]
                # item["images"] = self.getImages(links[i])
                self.items.append(item)
                yield item
        # print(self.items)

        for i in range(len(self.items)):
            request = scrapy.Request(self.items[i]['url'], callback = self.getOther)
            request.meta['index'] = i
            yield request
        # print(f"Time Taken: {time.time()-start}")

    def getUrl(self, item):
        return 'http://' + self.allowed_domains[0] + item.xpath('@href').extract()[0]

    #Just gets the price in digits and strips off everything else
    def getPrice(self, item):
        try:
            return int(item.xpath('span[1]/text()').extract()[0].strip('Rs ').replace(',',''))
        except:
            return 'Error at Price'

    def getTitle(self, item):
        try:
            return item.xpath('span[3]/text()').extract()[0]
        except:
            return 'Error at Title'

    def getModel(self, item):
        try:
            return int(item.xpath('span[2]/text()').extract()[0][:4])
        except:
            return 'Error at Model'

    def getMileage(self, item):
        try:
            return int(item.xpath('span[2]/text()').extract()[0][7:].lower().strip('km').strip(' '))
        except:
            return 'Error at Mileage'

    def getLocation(self,item):
        try:
            return item.xpath('div/span[1]/text()').extract()[0]
        except:
            return 'Error at Mileage'

    #Error: Images are added using js, need to find some way else to extract their links
    def getOther(self, response):
        try:
            soup = bs4(response.text, "lxml")
            carDetails = soup.findAll("span",{"class": "_1GWCT"})
            image = soup.findAll("img",{"class": "_3DF4u"})
            ret = {"fuelType":carDetails[4].text, "registration":carDetails[6].text, "image":image[0]["src"]}
            index = response.meta['index']
            self.items[index].update(ret)
            # yield ret
        except:
            return None

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

class OlxAuxSpider(scrapy.Spider):
    """docstring for OlxAuxSpider."""
    name = 'olx_aux_spider'
    allowed_domains = ['olx.com.pk']
    start_urls = []

    def __init__(self, startUrl='', *arg, **kwargs):
        super(OlxAuxSpider, self).__init__()
        self.start_urls = [startUrl]

    def parse(self, response):
        soup = bs4(response.text, 'lxml')
        carDetails = soup.findAll("span",{"class": "_1GWCT"})
        image = soup.findAll("img",{"class": "_3DF4u"})
        # ret = {"fuelType":carDetails[4].text, "registration":carDetails[6].text, "image":image[0]["src"]}
        print(carDetails)
        # return ret

# def collect_items(item, response, spider):
#     items.append(item)

#
# crawler = Crawler(OlxspiderSpider)
# crawler.signals.connect(collect_items, signals.item_scraped)
#
# process = CrawlerProcess(get_project_settings())
# process.crawl(crawler, 'words', 'https://www.olx.com.pk/lahore_g4060673/q-city-2016')
# process.start()
