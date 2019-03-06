# -*- coding: utf-8 -*-
import scrapy


class OlxspiderSpider(scrapy.Spider):
    name = 'olxSpider'
    allowed_domains = ['https://www.olx.com.pk/']
    start_urls = ['http://https://www.olx.com.pk//']

    def parse(self, response):
        pass
