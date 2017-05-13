# -*- coding: utf-8 -*-
import scrapy
from jasjoo.items import JasjooItem

class JasjooFSpider(scrapy.Spider):
    name = "jasjoo_d"
    allowed_domains = ["jasjoo.com"]
    start_urls = ['http://www.jasjoo.com/books/wordbook/dehkhoda/']

    def parse(self, response):
    	for href in response.xpath('//div[@class="bt_free"]//../@href'):
    		yield scrapy.Request(href.extract(), callback=self.parse_pages)

    def parse_pages(self,response):
    	pages = response.xpath('//td[@class="under_border_2"]/div/span/b[3]/text()').extract()[0].replace(',','')
    	for page in range(1,int(pages)/10+1):
    		url = "http://www.jasjoo.com/wordbook/dehkhoda/"+ response.url.split('/')[-1]+"/"+str(page)
    		yield scrapy.Request(url,callback=self.parse_words)

    def parse_words(self,response):
        words = response.xpath('//h2/a//text()')
        defins = response.xpath('//p[not(@class) and not(@style)]/text()')
    	for i in range(len(words)):
	        if len(words[i].extract()) >=1:
	        	item = JasjooItem()
		        item["word"]  = words[i].extract()
		        item["defin"] = defins[i].extract()
	        	yield item