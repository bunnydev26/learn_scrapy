# -*- coding: utf-8 -*-
import scrapy


class QuotesJsSpider(scrapy.Spider):
    name = 'quotes_js'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js']

    def parse(self, response):
        pass
