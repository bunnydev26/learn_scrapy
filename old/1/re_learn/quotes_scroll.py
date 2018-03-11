# -*- coding: utf-8 -*-
import scrapy
import json

class QuotesScrollSpider(scrapy.Spider):
    name = 'quotes_scroll'
    allowed_domains = ['quotes.toscrape.com']
    api_url = "http://quotes.toscrape.com/api/quotes?page={}"
    start_urls = [api_url.format(1)]

    def parse(self, response):
        data = json.loads(response.text)

        for quote in data["quotes"]:
            yield {
                "author_name": quote["author"]["name"],
                "text": quote["text"],
                "tags": quote["tags"],
            }
 

        if data['has_next']:
            next_page = data['page'] + 1
            # import pdb; pdb.set_trace()
            self.log(self.api_url.format(next_page))
            yield scrapy.Request(url=self.api_url.format(next_page), callback=self.parse)
            # yield scrapy.Request(url=next_url, callback=self.parse)
