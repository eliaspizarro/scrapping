from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import re

class AmazonProductSpider(scrapy.Spider):
    name = 'AmazonDeals'
    allowed_domains = ['amazon.com']
    search = 'trimmer'
    start_urls = [
        'https://www.amazon.com/s?k=' + search + '&ref=nb_sb_noss_2'
    ]
    custom_settings = {
            'FEED_URI' : 'Asin_Titles.json',
            'FEED_FORMAT' : 'json'
    }

    def parse(self, response):
        Link = response.css('.a-text-normal').css('a::attr(href)').extract()
        Title = response.css('span.a-text-normal').css('::text').extract()

        # para cada producto, crea un AmazonItem, llena los campos del item
        for result in zip(Link,Title):
            item = AmazonItem()
            item['title_Product'] = result[1]
            item['link_Product'] = result[0]
            # extrae el ASIN del link
            ASIN = re.findall(r"(?<=dp/)[A-Z0-9]{10}",result[0])[0]
            item['ASIN_Product'] = ASIN
            item['url_response'] = response.url
            yield item

class AmazonItem(scrapy.Item):
    # definir campos para el item aqui:
    title_Product = scrapy.Field()
    link_Product = scrapy.Field()
    ASIN_Product = scrapy.Field()
    url_response = scrapy.Field()


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(AmazonProductSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # el script se bloquea aqui hasta que el crawling termine