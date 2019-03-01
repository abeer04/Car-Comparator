# -*- coding: utf-8 -*-
import scrapy


class PakwheelsSpider(scrapy.Spider):
    name = 'pakWheels'
    allowed_domains = ['pakwheels.com']
    start_urls = ['https://www.pakwheels.com/used-cars/search/-/mk_honda/md_city/vr_i-vtec-prosmatec/ct_lahore/']

    def parse(self, response):
        print(response.xpath('//ul/li[@itemtype="https://schema.org/Vehicle"][@name=$li]/preceding-sibling::li[1]/meta[@itemprop="name"]/@content').get())

#
# //meta[@itemprop="name"]/@content
#
# //div[@id="images"]/a/text()'


# //meta[2][@itemprop="name"]/@content'
