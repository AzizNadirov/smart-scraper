from pathlib import Path

BOT_NAME = "scrapy_parser"

SPIDER_MODULES = ["scrapy_parser.spiders"]
NEWSPIDER_MODULE = "scrapy_parser.spiders"


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
   "scrapy_parser.middlewares.ScrapyParserDownloaderMiddleware": 543,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
