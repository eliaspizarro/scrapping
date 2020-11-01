from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import re

class AmazonProductSpider(scrapy.Spider):
	name = "AmazonDeals"
	allowed_domains = ["amazon.com"]

	#Use working product URL below
	start_urls = [
		 "https://www.amazon.com/s?k=trimmer&ref=nb_sb_noss_2"	 
	]
	custom_settings = {
			'FEED_URI' : 'Asin_Titles.json',
			'FEED_FORMAT' : 'json'
	}

	def parse(self, response):
		Link = response.css('.a-text-normal').css('a::attr(href)').extract()
		Title = response.css('span.a-text-normal').css('::text').extract()

		# for each product, create an AmazonItem, populate the fields and yield the item
		for result in zip(Link,Title):
			item = AmazonItem()
			item['title_Product'] = result[1]
			item['link_Product'] = result[0]
			# extract ASIN from link
			ASIN = re.findall(r"(?<=dp/)[A-Z0-9]{10}",result[0])[0]
			item['ASIN_Product'] = ASIN
			item['url_response'] = response.url
			yield item

class AmazonItem(scrapy.Item):
	# define the fields for your item here like:
	title_Product = scrapy.Field()
	link_Product = scrapy.Field()
	ASIN_Product = scrapy.Field()
	url_response = scrapy.Field()


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(AmazonProductSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished