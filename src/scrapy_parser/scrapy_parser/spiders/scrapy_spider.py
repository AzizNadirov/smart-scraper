from typing import Any, Iterable
import uuid
import random
from collections import deque
from pathlib import Path
import scrapy
from w3lib.url import canonicalize_url
from slugify import slugify
from IPython.display import display

from scrapy_parser.configs import configs


class ScrapyRandomisedCrawlerSpider(scrapy.Spider):
    name = "ScrapyRandomisedCrawlerSpider"
    DOWNLOAD_DELAY: float = 0.0
    run_id = slugify(f"{uuid.uuid4().hex}")
    
    def __init__(self,
                 base_url: str,
                 random_links_per_page: int | None = 5,
                 *args: Any,
                 **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.random_links_per_page = random_links_per_page
        self.base_url = canonicalize_url(base_url)
        
        
        # Track URLs
        self._seen_urls = set()  # URLs we've already processed
        self._queued_urls = deque([self.base_url])  # URLs waiting to be processed
        
        # Create directory for saved pages
        self.feeds_dir: Path = configs.TMP_PAGES_DIR / f"{self.run_id}" 
        self.feeds_dir.mkdir(exist_ok=True, parents=True)

    def start_requests(self) -> Iterable[scrapy.Request]:
        """Start the crawling process with the base URL"""
        self.logger.info(f"Starting crawl from: {self.base_url}")
        return self._make_next_request()

    def _make_next_request(self) -> Iterable[scrapy.Request]:
        """Generate requests for URLs in the queue"""
        while self._queued_urls:
            next_url = self._queued_urls.popleft()
            if next_url not in self._seen_urls:
                self.logger.info(f"Requesting URL: {next_url}")
                self.logger.info(f"Queue size: {len(self._queued_urls)}")
                yield scrapy.Request(url=next_url, callback=self.parse)

    def parse(self, response: scrapy.http.Response) -> Iterable[scrapy.Request]:
        """Process each page and queue new URLs"""
        current_url = response.url
        self.logger.info(f"Parsing page: {current_url}")
        
        self._seen_urls.add(current_url)
        all_links = self._select_links(response)
        selected_links = random.sample(all_links, min(self.random_links_per_page, len(all_links)))
        # add parsed and not selected links to seen
        self._seen_urls.update(set(all_links) - set(selected_links))
        self._queued_urls.extend(selected_links)
        self.logger.info(f"Added {len(selected_links)} new URLs to queue. Queue size: {len(self._queued_urls)} Seen Size: {len(self._seen_urls)}")
        feed_path = self.feed_page(response)
        yield {
            'url': current_url,
            'feed_path': feed_path
        }
        yield from self._make_next_request()
        
        
    def _select_links(self, response: scrapy.http.Response) -> list[str]:
        all_links = response.css('a::attr(href)').extract()
        all_links = [f"{self.base_url}{link[1:]}" if link.startswith('/') else link for link in all_links]
        all_links = [link for link in all_links
                        if (
                        '.' not in link.split('/')[-1]
                        and link.startswith(self.base_url)
                        and link not in self._seen_urls
                        and link not in self._queued_urls)
                        ]
        return all_links
    

    def feed_page(self, response: scrapy.http.Response) -> str:
        """Save the page content to a file"""
        feed: Path = self.feeds_dir / f"{slugify(response.url)}.html"
        with feed.open('w', encoding='utf-8') as f:
            f.write(response.text)
        self.logger.info(f"Saved page: {response.url} into: {feed}")
        return feed.as_posix()
    

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            {
            "DOWNLOAD_DELAY": cls.DOWNLOAD_DELAY,
            "DOWNLOADER_MIDDLEWARES": {
                'scrapy_parser.middlewares.ScrapyParserDownloaderMiddleware': 543,
            },
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "FEEDS": {f'{configs.TMP_DIR / cls.run_id}.json':{
             'format': 'json',
             'encoding': 'utf-8'
         },
        }}, priority='spider')
        super().update_settings(settings)