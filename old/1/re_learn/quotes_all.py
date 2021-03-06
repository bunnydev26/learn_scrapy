# -*- coding: utf-8 -*-
import scrapy


class QuotesAllSpider(scrapy.Spider):
    name = 'quotes_all'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes_list = response.css("div.quote")

        for quote in quotes_list:
            item = {
                'author': quote.css("small.author::text").extract_first(),
                'text': quote.css("span.text::text").extract_first(),
                'tags': quote.css("a.tag::text").extract(),
            }
            yield item

        # Follow Pagination Link..
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)