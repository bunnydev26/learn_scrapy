# -*- coding: utf-8 -*-
import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # Scrape the author details
        author_details_url_list = response.css("div.quote > span  > a::attr(href)").extract()

        for author_details_url in author_details_url_list:
            url = response.urljoin(author_details_url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        # Follow pagination link
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        next_page_url = response.urljoin(next_page_url)

        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):

        yield {
            "author_name": response.css("h3.author-title::text").extract_first(),
            "author_birth_date": response.css("span.author-born-date::text").extract_first()
        }
