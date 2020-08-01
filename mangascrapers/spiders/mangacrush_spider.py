import re
import os
import urllib.request
import urllib.parse as urlparse
from pathlib import Path
from ..items import MangabookItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MangacrushSpider (CrawlSpider):
    name: 'mangacrush'
    allowed_domains = ['mangacrush.com']
    start_urls = ['https://mangacrush.com']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    rules = [
        # Rule(LinkExtractor(), callback='parse_link', follow=True)
    ]


    def parse (self, response):
        uri = urlparse.urlparse(response.url).path

        m1 = re.match(r"^/manga/([^/]+)/?$", uri)
        m2 = re.match(r"^/manga/[^/]+/([^/]+)/?$", uri)

        if m1:
            # Manga
            items = MangabookItem()
            uriname = m1.group(1)
            title = response.css('.post-title h1::text').extract()
            rating = response.css('.post-total-rating span.score.total_votes::text').extract()
            alternative_name = ''
            author = response.css('.post-content_item .summary-content .author-content::text').extract()
            genres = response.css('.post-content_item .summary-content .genres-content::text').extract()
            booktype = ''
            summary = response.css('.description-summary .summary__content > p::text').extract()

            items['source'] = self.name
            items['uri'] = uriname
            items['name'] = title
            items['alternative_name'] = alternative_name
            items['rating'] = rating
            items['author'] = author
            items['genres'] = genres
            items['booktype'] = booktype
            items['summary'] = summary
            
            yield items