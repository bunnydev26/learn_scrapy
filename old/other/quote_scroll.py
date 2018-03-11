# -*- coding: utf-8 -*-
import scrapy
import json

class QuoteScrollSpider(scrapy.Spider):
    """
        This spider fetches the data from the infinite scroll page.
    """
    name = 'quote_scroll'
    allowed_domains = ['quotes.toscrape.com']
    api_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [api_url.format(1)]

    def parse(self, response):
        #dict_keys(['has_next', 'page', 'quotes', 'tag', 'top_ten_tags'])
        quotes_dict = json.loads(response.text)

        for quotes in quotes_dict["quotes"]:
            yield {
                'author': quotes['author']['name'],
                'text': quotes['text'],
                'tags': quotes['tags'],
            }

        if quotes_dict['has_next']:
            next_page = quotes_dict['page']+1
            yield scrapy.Request(url=self.api_url.format(next_page), callback=self.parse)
