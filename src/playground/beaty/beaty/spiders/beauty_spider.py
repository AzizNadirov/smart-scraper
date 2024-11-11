import scrapy


class BeautySpider(scrapy.Spider):
    name = "emporium"
    allowed_domains = ["https://www.emporium.az/"]
    start_urls = allowed_domains[0]
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        pass