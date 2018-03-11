# -*- coding: utf-8 -*-
import scrapy


class QuotesDetailSpider(scrapy.Spider):
    name = 'quotes_detail'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes_list = response.css("div.quote")

        for quote in quotes_list:
            author_link = quote.css("small.author + a::attr(href)").extract_first()
            author_link = response.urljoin(author_link)
            yield scrapy.Request(url=author_link, callback=self.parse_author_info)

        # Follow pagination Link
        next_url = response.css("li.next > a::attr(href)").extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_author_info(self, response):
        item = {
                "author": response.css("h3.author-title::text").extract_first().strip(),
                "date_of_birth": response.css("span.author-born-date::text").extract_first()
        }
        yield item
