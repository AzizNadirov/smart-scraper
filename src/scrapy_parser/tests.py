from scrapy.crawler import CrawlerProcess

from scrapy_parser.spiders import ScrapyRandomisedCrawlerSpider



def start_scrapy_randomised_crawler(base_url: str, 
                                    random_links_per_page: int):
    process = CrawlerProcess()
    process.crawl(ScrapyRandomisedCrawlerSpider,
                    base_url=base_url,
                    random_links_per_page=random_links_per_page)
    process.start()


if __name__ == '__main__':
    start_scrapy_randomised_crawler(base_url="https://kontakt.az/", 
                                    random_links_per_page=5)