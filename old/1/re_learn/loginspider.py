# -*- coding: utf-8 -*-
import scrapy


class LoginspiderSpider(scrapy.Spider):
    name = 'loginspider'
    login_url = "http://quotes.toscrape.com/login"
    start_urls = [login_url]

    def parse(self, response):
        # Extract the csrf_token
        token = response.css("input[name='csrf_token']::attr(value)").extract_first()
        # create a python dictionary with the form values
        data = {
        	"csrf_token": token,
        	"username": "abc",
        	"password": "abc",
        }
        # submit a Post request to it
        # yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_quotes)
        yield scrapy.FormRequest.from_response(response, formdata=data, callback=self.parse_quotes)

    def parse_quotes(self, response):
    	# import pdb; pdb.set_trace()
    	for quote in response.css("div.quote"):
    		yield {
    			"author" : quote.css("small.author::text").extract_first(),
    			"author_url": quote.css(
    				"small.author ~ a[href*='goodreads.com']::attr(href)"
    			).extract_first(),
    		}
