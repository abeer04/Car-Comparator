# -*- coding: utf-8 -*-

# Define your item pipelines here
import io
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from main.models import Keyword, Car, Image, KeywordCar

class CarofferspiderPipeline(object):
    def __init__(self, unique_id, words, *args, **kwargs):
        # pass
        keyword = Keyword()
        keyword.keyword = words
        keyword.save()
        self.keyword = keyword
        self.keyword_id = keyword.keyword_id
        self.unique_id = unique_id
        # self.words = words
        # self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        # pass
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
            words=crawler.settings.get('words'), # this will be passed from django view
        )

    def close_spider(self, spider):
        # pass
        keyword = Keyword.objects.get(keyword_id=self.keyword_id)
        keyword.unique_id = self.unique_id
        keyword.save()
        # self.keyword["unique_id"] = self.unique_id
        # self.keyword.save()

# # example
# # item = {'keywordItem': {'keyword': 'city, 2016'}, 'carItem': {'url': 'www.pakwheels.com/used-cars/honda-city-2016-for-sale-in-multan-3052872', 'title': 'Honda City  2016 Aspire Prosmatec 1.3 i-VTEC', 'price': 1875000, 'location': 'Multan', 'model': 2016, 'mileage': 39000, 'fuel': 'Petrol', 'engine': '1300 cc', 'transmission': 'Automatic'}, 'imageItem': {'url': 'https://cache4.pakwheels.com/ad_pictures/2679/honda-city-aspire-prosmatec-2016-26796065.jpg, https://cache1.pakwheels.com/ad_pictures/2679/honda-city-aspire-prosmatec-2016-26796066.jpg, https://cache2.pakwheels.com/ad_pictures/2679/honda-city-aspire-prosmatec-2016-26796060.jpg, https://cache1.pakwheels.com/ad_pictures/2679/honda-city-aspire-prosmatec-2016-26796063.jpg'}}
    def process_item(self, item, spider):
        # pass
        # self.items.append(item['url'])
        # with open('file.txt', 'a+') as f:
        #     f.write("%s\n" % item)

        carItem = item["carItem"]
        car = Car()
        print("================="+carItem["url"])
        car.url = carItem["url"] # get URL
        car.title = carItem["title"] # get title
        car.price = carItem["price"] # get price
        car.location = carItem["location"] # get location
        car.model = carItem["model"] # get model year
        car.mileage = carItem["mileage"] # get mileage
        car.fuel = carItem["fuel"] # get fuel type
        car.engine = carItem["engine"] # get engine
        car.transmission = carItem["transmission"] # get transmission
        car.save()

        imageItem = item["imageItem"]["url"]
        if (len(imageItem) > 1):
            for imageUrl in imageItem.split(", "):
                image = Image()
                image.url = imageUrl
                image.car_id = car
                image.save()
        else:
            image = Image()
            image.url = imageItem
            image.car_id = car
            image.save()

        keywordCar = KeywordCar()
        keywordCar.keyword_id = self.keyword
        keywordCar.car_id = car
        keywordCar.save()
        # with io.open("items.txt", "a", encoding="utf-8") as f:
        #     f.write(str(item))
        return item