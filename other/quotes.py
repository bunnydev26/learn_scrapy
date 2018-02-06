# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.log("Testing a new scrapy framework")
        for quote in response.css('div.quote'):
            item = {
            'author': quote.css('small.author::text').extract_first(),
            'text': quote.css('span.text::text').extract_first(),
            'tags': quote.css('a.tag::text').extract()
            }
            yield item
            # Follow pagination link
            next_page_url = response.css("li.next > a::attr(href)").extract_first()
            next_page_url = response.urljoin(next_page_url)

            if next_page_url:
                yield scrapy.Request(url=next_page_url, callback=self.parse)
