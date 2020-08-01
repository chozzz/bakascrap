import re
import urllib.parse as urlparse
from ..items import MangabookItem, MangapageItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MangacrushSpider (CrawlSpider):
    name = 'mangacrush'
    allowed_domains = ['mangacrush.com']
    start_urls = ['https://mangacrush.com/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    rules = [
        Rule(LinkExtractor(), callback='parse_link', follow=True)
    ]

    def parse_link (self, response):
        uri = urlparse.urlparse(response.url).path

        m1 = re.match(r"^/manga/([^/]+)/?$", uri)
        m2 = re.match(r"^/manga/([^/]+)/([^/]+)/?$", uri)

        if m1:
            # Manga
            items = MangabookItem()
            uriname = m1.group(1)
            title = response.css('.post-title h1::text').extract_first()
            rating = response.css('.post-total-rating span.score.total_votes::text').extract_first()
            author = response.css('.post-content_item .summary-content .author-content > a::text').extract_first()
            genres = response.css('.post-content_item .summary-content .genres-content a::text').extract()
            booktype = ''
            summary = response.css('.description-summary .summary__content > p:first-child::text').extract_first()

            items['source'] = self.name
            items['uri'] = uriname
            items['name'] = title.strip()
            items['rating'] = float(rating)
            items['author'] = author.strip()
            items['genres'] = ','.join(genres)
            items['booktype'] = booktype
            items['summary'] = summary.replace('\n', ' ').replace('\r', '')
            
            yield items

        elif m2:
            # Mangapage
            items = MangapageItem()
            uriname = m2.group(1)
            pagename = m2.group(2)
            imageList = response.css('.reading-content div.page-break > img::attr(src)').extract()

            if imageList is not None:
                images = ' '.join(imageList).strip()
                items['source'] = self.name
                items['uri'] = uriname
                items['page'] = pagename
                items['images'] = re.sub(r"\t|\n|\r", "", images)

            yield items